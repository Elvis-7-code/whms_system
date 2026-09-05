from datetime import date, timedelta
from functools import wraps

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Sum, Avg, Q, Count

import csv
from io import BytesIO

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    UserCreationForm,
)
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import Group, User

from .models import (
    Animal,
    HealthRecord,
    BreedingRecord,
    ProductionRecord,
    FinancialRecord,
    FarmSettings,
    ActivityLog,
)


# ============================================================
# ROLE MANAGEMENT
# ============================================================

ADMINISTRATOR = 'Administrator'
FARM_MANAGER = 'Farm Manager'
FARM_WORKER = 'Farm Worker'


def get_user_role(user):
    """
    Return the user's primary WAHOME HERD role.
    Superusers are always Administrators.
    """

    if user.is_superuser:
        return ADMINISTRATOR

    role_names = [
        ADMINISTRATOR,
        FARM_MANAGER,
        FARM_WORKER,
    ]

    for role_name in role_names:
        if user.groups.filter(name=role_name).exists():
            return role_name

    return None


def user_has_role(user, *roles):
    """
    Check whether a user has one of the supplied roles.
    Superusers always have full access.
    """

    if user.is_superuser:
        return True

    user_groups = set(
        user.groups.values_list(
            'name',
            flat=True
        )
    )

    return bool(
        user_groups.intersection(roles)
    )


def role_required(*roles):
    """
    Restrict a view to selected WAHOME HERD roles.

    Users without permission are shown the custom
    WAHOME HERD 403 page.
    """

    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:
                return redirect('login')

            if not user_has_role(
                request.user,
                *roles
            ):
                return render(
                    request,
                    '403.html',
                    {
                        'user_role': get_user_role(
                            request.user
                        ),
                    },
                    status=403
                )

            return view_func(
                request,
                *args,
                **kwargs
            )

        return wrapper

    return decorator


def log_activity(user, action, module, description):
    """Create an audit-log entry for a user action."""

    ActivityLog.objects.create(
        user=user,
        action=action,
        module=module,
        description=description,
    )


# ============================================================
# AUTHENTICATION
# ============================================================

def login_view(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':

        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            user = form.get_user()

            login(
                request,
                user
            )

            log_activity(
                user,
                'LOGIN',
                'Authentication',
                f'{user.username} logged in.'
            )

            return redirect('dashboard')

    else:

        form = AuthenticationForm()

    return render(
        request,
        'registration/login.html',
        {
            'form': form,
        }
    )


@login_required(login_url='login')
def profile(request):

    return render(
        request,
        'livestock/profile.html',
        {
            'user': request.user,
            'role': get_user_role(request.user),
        }
    )


@login_required(login_url='login')
def change_password(request):

    if request.method == 'POST':

        form = PasswordChangeForm(
            request.user,
            request.POST
        )

        if form.is_valid():

            user = form.save()

            update_session_auth_hash(
                request,
                user
            )

            log_activity(
                request.user,
                'UPDATE',
                'Authentication',
                'Password was changed.'
            )

            return redirect(
                'password_change_done'
            )

    else:

        form = PasswordChangeForm(
            request.user
        )

    return render(
        request,
        'registration/password_change_form.html',
        {
            'form': form,
        }
    )


# ============================================================
# DASHBOARD
# ============================================================

@login_required(login_url='login')
def dashboard(request):

    today = date.today()

    # ========================================================
    # LIVESTOCK OVERVIEW
    # ========================================================

    total_animals = Animal.objects.count()

    active_animals = Animal.objects.filter(
        status='ACTIVE'
    ).count()

    total_livestock = active_animals

    sold_animals = Animal.objects.filter(
        status='SOLD'
    ).count()

    deceased_animals = Animal.objects.filter(
        status='DECEASED'
    ).count()

    total_cows = Animal.objects.filter(
        species='COW',
        status='ACTIVE'
    ).count()

    total_sheep = Animal.objects.filter(
        species='SHEEP',
        status='ACTIVE'
    ).count()

    total_goats = Animal.objects.filter(
        species='GOAT',
        status='ACTIVE'
    ).count()

    total_males = Animal.objects.filter(
        sex='MALE',
        status='ACTIVE'
    ).count()

    total_females = Animal.objects.filter(
        sex='FEMALE',
        status='ACTIVE'
    ).count()

    average_weight = Animal.objects.filter(
        weight__isnull=False,
        status='ACTIVE'
    ).aggregate(
        average=Avg('weight')
    )['average']

    recent_animals = Animal.objects.select_related().order_by(
        '-created_at'
    )[:5]

    # Dashboard chart data
    species_labels = ['Cows', 'Goats', 'Sheep']
    species_values = [
        total_cows,
        total_goats,
        total_sheep,
    ]

    livestock_status_labels = [
        'Active',
        'Sold',
        'Deceased',
    ]
    livestock_status_values = [
        active_animals,
        sold_animals,
        deceased_animals,
    ]

    sex_labels = ['Male', 'Female']
    sex_values = [
        total_males,
        total_females,
    ]

    if total_animals > 0:
        active_percentage = round(
            (active_animals / total_animals) * 100,
            1
        )
    else:
        active_percentage = 0

    # ========================================================
    # PRODUCTION
    # ========================================================

    production_count = ProductionRecord.objects.count()

    milk_production = ProductionRecord.objects.filter(
        production_type='MILK'
    ).aggregate(
        total=Sum('quantity')
    )['total'] or 0

    meat_production = ProductionRecord.objects.filter(
        production_type='MEAT'
    ).aggregate(
        total=Sum('quantity')
    )['total'] or 0

    weight_production = ProductionRecord.objects.filter(
        production_type='WEIGHT'
    ).aggregate(
        total=Sum('quantity')
    )['total'] or 0

    recent_production = ProductionRecord.objects.select_related(
        'animal'
    ).order_by(
        '-date',
        '-created_at'
    )[:5]

    # Last 30 days production trend
    production_trend_labels = []
    production_trend_milk = []
    production_trend_meat = []
    production_trend_weight = []

    production_trend_start = today - timedelta(days=29)

    for day_offset in range(30):

        current_day = (
            production_trend_start +
            timedelta(days=day_offset)
        )

        daily_milk = ProductionRecord.objects.filter(
            date=current_day,
            production_type='MILK'
        ).aggregate(
            total=Sum('quantity')
        )['total'] or 0

        daily_meat = ProductionRecord.objects.filter(
            date=current_day,
            production_type='MEAT'
        ).aggregate(
            total=Sum('quantity')
        )['total'] or 0

        daily_weight = ProductionRecord.objects.filter(
            date=current_day,
            production_type='WEIGHT'
        ).aggregate(
            total=Sum('quantity')
        )['total'] or 0

        production_trend_labels.append(
            current_day.strftime('%d %b')
        )

        production_trend_milk.append(
            float(daily_milk)
        )

        production_trend_meat.append(
            float(daily_meat)
        )

        production_trend_weight.append(
            float(daily_weight)
        )

    # ========================================================
    # HEALTH
    # ========================================================

    health_count = HealthRecord.objects.count()

    vaccination_count = HealthRecord.objects.filter(
        record_type='VACCINATION'
    ).count()

    treatment_count = HealthRecord.objects.filter(
        record_type='TREATMENT'
    ).count()

    illness_count = HealthRecord.objects.filter(
        record_type='ILLNESS'
    ).count()

    vet_visit_count = HealthRecord.objects.filter(
        record_type='VET_VISIT'
    ).count()

    recent_health = HealthRecord.objects.select_related(
        'animal'
    ).order_by(
        '-date',
        '-created_at'
    )[:5]

    # ========================================================
    # BREEDING
    # ========================================================

    breeding_count = BreedingRecord.objects.count()

    planned_breeding = BreedingRecord.objects.filter(
        status='PLANNED'
    ).count()

    pregnant_count = BreedingRecord.objects.filter(
        status='PREGNANT'
    ).count()

    successful_breeding = BreedingRecord.objects.filter(
        status='SUCCESSFUL'
    ).count()

    failed_breeding = BreedingRecord.objects.filter(
        status='FAILED'
    ).count()

    births_recorded = BreedingRecord.objects.filter(
        status='BORN'
    ).count()

    total_offspring = BreedingRecord.objects.filter(
        offspring_count__isnull=False
    ).aggregate(
        total=Sum('offspring_count')
    )['total'] or 0

    recent_breeding = BreedingRecord.objects.select_related(
        'female',
        'male'
    ).order_by(
        '-breeding_date',
        '-created_at'
    )[:5]

    if breeding_count > 0:
        breeding_success_rate = round(
            (
                (successful_breeding + births_recorded)
                / breeding_count
            ) * 100,
            1
        )
    else:
        breeding_success_rate = 0

    # ========================================================
    # FINANCE
    # ========================================================

    total_income = FinancialRecord.objects.filter(
        record_type='INCOME'
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    total_expenses = FinancialRecord.objects.filter(
        record_type='EXPENSE'
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    net_profit = total_income - total_expenses

    income_count = FinancialRecord.objects.filter(
        record_type='INCOME'
    ).count()

    expense_count = FinancialRecord.objects.filter(
        record_type='EXPENSE'
    ).count()

    # Recent 6-month financial trend
    financial_trend_labels = []
    financial_trend_income = []
    financial_trend_expenses = []
    financial_trend_profit = []

    for month_offset in range(5, -1, -1):

        month_number = today.month - month_offset
        year = today.year

        while month_number <= 0:
            month_number += 12
            year -= 1

        month_start = date(
            year,
            month_number,
            1
        )

        if month_number == 12:
            next_month = date(
                year + 1,
                1,
                1
            )
        else:
            next_month = date(
                year,
                month_number + 1,
                1
            )

        month_income = FinancialRecord.objects.filter(
            record_type='INCOME',
            date__gte=month_start,
            date__lt=next_month
        ).aggregate(
            total=Sum('amount')
        )['total'] or 0

        month_expenses = FinancialRecord.objects.filter(
            record_type='EXPENSE',
            date__gte=month_start,
            date__lt=next_month
        ).aggregate(
            total=Sum('amount')
        )['total'] or 0

        financial_trend_labels.append(
            month_start.strftime('%b %Y')
        )

        financial_trend_income.append(
            float(month_income)
        )

        financial_trend_expenses.append(
            float(month_expenses)
        )

        financial_trend_profit.append(
            float(month_income - month_expenses)
        )

    # ========================================================
    # FARM SETTINGS
    # ========================================================

    farm = FarmSettings.objects.first()

    # ========================================================
    # ALERTS & NOTIFICATIONS
    # ========================================================

    alerts = []

    alert_limit = today + timedelta(days=30)

    # Overdue births
    overdue_births = BreedingRecord.objects.filter(
        status='PREGNANT',
        expected_birth_date__isnull=False,
        expected_birth_date__lt=today
    ).select_related(
        'female'
    ).order_by(
        'expected_birth_date'
    )

    for record in overdue_births:

        alerts.append({
            'type': 'danger',
            'icon': '🚨',
            'title': 'Overdue Birth',
            'message': (
                f'{record.female.animal_id} has an expected '
                f'birth date of {record.expected_birth_date}.'
            ),
            'date': record.expected_birth_date,
            'animal_id': record.female.animal_id,
        })

    # Upcoming births
    upcoming_births = BreedingRecord.objects.filter(
        status='PREGNANT',
        expected_birth_date__isnull=False,
        expected_birth_date__gte=today,
        expected_birth_date__lte=alert_limit
    ).select_related(
        'female'
    ).order_by(
        'expected_birth_date'
    )

    for record in upcoming_births:

        days_remaining = (
            record.expected_birth_date - today
        ).days

        if days_remaining == 0:
            message = (
                f'{record.female.animal_id} is expected '
                f'to give birth today.'
            )

        elif days_remaining == 1:
            message = (
                f'{record.female.animal_id} is expected '
                f'to give birth tomorrow.'
            )

        else:
            message = (
                f'{record.female.animal_id} is expected '
                f'to give birth in {days_remaining} days.'
            )

        alerts.append({
            'type': 'warning',
            'icon': '🐄',
            'title': 'Upcoming Birth',
            'message': message,
            'date': record.expected_birth_date,
            'animal_id': record.female.animal_id,
        })

    # Overdue health
    overdue_health = HealthRecord.objects.filter(
        next_due_date__isnull=False,
        next_due_date__lt=today
    ).select_related(
        'animal'
    ).order_by(
        'next_due_date'
    )

    for record in overdue_health:

        if record.record_type == 'VACCINATION':
            title = 'Overdue Vaccination'
            icon = '💉'
        else:
            title = 'Overdue Health Follow-up'
            icon = '🩺'

        alerts.append({
            'type': 'danger',
            'icon': icon,
            'title': title,
            'message': (
                f'{record.animal.animal_id} has a health '
                f'follow-up due date of {record.next_due_date}.'
            ),
            'date': record.next_due_date,
            'animal_id': record.animal.animal_id,
        })

    # Upcoming health
    upcoming_health = HealthRecord.objects.filter(
        next_due_date__isnull=False,
        next_due_date__gte=today,
        next_due_date__lte=alert_limit
    ).select_related(
        'animal'
    ).order_by(
        'next_due_date'
    )

    for record in upcoming_health:

        days_remaining = (
            record.next_due_date - today
        ).days

        if record.record_type == 'VACCINATION':
            title = 'Vaccination Due'
            icon = '💉'
        else:
            title = 'Health Follow-up Due'
            icon = '🩺'

        if days_remaining == 0:
            message = (
                f'{record.animal.animal_id} has a '
                f'{record.record_type.lower()} due today.'
            )

        elif days_remaining == 1:
            message = (
                f'{record.animal.animal_id} has a '
                f'{record.record_type.lower()} due tomorrow.'
            )

        else:
            message = (
                f'{record.animal.animal_id} has a '
                f'{record.record_type.lower()} due in '
                f'{days_remaining} days.'
            )

        alerts.append({
            'type': 'warning',
            'icon': icon,
            'title': title,
            'message': message,
            'date': record.next_due_date,
            'animal_id': record.animal.animal_id,
        })

    # Recent illnesses
    illness_limit = today - timedelta(days=14)

    recent_illnesses = HealthRecord.objects.filter(
        record_type='ILLNESS',
        date__gte=illness_limit
    ).select_related(
        'animal'
    ).order_by(
        '-date',
        '-created_at'
    )

    for record in recent_illnesses:

        alerts.append({
            'type': 'health',
            'icon': '🩺',
            'title': 'Recent Illness',
            'message': (
                f'{record.animal.animal_id} has a recent '
                f'illness record.'
            ),
            'date': record.date,
            'animal_id': record.animal.animal_id,
        })

    # Planned breeding
    planned_records = BreedingRecord.objects.filter(
        status='PLANNED'
    ).select_related(
        'female',
        'male'
    ).order_by(
        '-breeding_date'
    )

    for record in planned_records:

        alerts.append({
            'type': 'info',
            'icon': '🐑',
            'title': 'Planned Breeding',
            'message': (
                f'Breeding is planned for '
                f'{record.female.animal_id}.'
            ),
            'date': record.breeding_date,
            'animal_id': record.female.animal_id,
        })

    alerts = sorted(
        alerts,
        key=lambda alert: (
            0 if alert['type'] == 'danger'
            else 1 if alert['type'] == 'warning'
            else 2 if alert['type'] == 'health'
            else 3
        )
    )

    alert_count = len(alerts)

    # Keep the dashboard compact while retaining the most
    # important alerts first.
    alerts = alerts[:10]

    # Separate alert totals are useful for dashboard badges.
    overdue_alert_count = sum(
        1
        for alert in alerts
        if alert['type'] == 'danger'
    )

    warning_alert_count = sum(
        1
        for alert in alerts
        if alert['type'] == 'warning'
    )

    health_alert_count = sum(
        1
        for alert in alerts
        if alert['type'] == 'health'
    )

    # ========================================================
    # DASHBOARD CONTEXT
    # ========================================================

    context = {
        'total_animals': total_animals,
        'total_livestock': total_livestock,
        'active_animals': active_animals,
        'sold_animals': sold_animals,
        'deceased_animals': deceased_animals,

        'total_cows': total_cows,
        'total_sheep': total_sheep,
        'total_goats': total_goats,

        'total_males': total_males,
        'total_females': total_females,
        'average_weight': average_weight,
        'active_percentage': active_percentage,

        'species_labels': species_labels,
        'species_values': species_values,
        'livestock_status_labels': livestock_status_labels,
        'livestock_status_values': livestock_status_values,
        'sex_labels': sex_labels,
        'sex_values': sex_values,

        'recent_animals': recent_animals,

        'production_count': production_count,
        'milk_production': milk_production,
        'meat_production': meat_production,
        'weight_production': weight_production,
        'recent_production': recent_production,

        'production_trend_labels': production_trend_labels,
        'production_trend_milk': production_trend_milk,
        'production_trend_meat': production_trend_meat,
        'production_trend_weight': production_trend_weight,

        'health_count': health_count,
        'vaccination_count': vaccination_count,
        'treatment_count': treatment_count,
        'illness_count': illness_count,
        'vet_visit_count': vet_visit_count,
        'recent_health': recent_health,

        'breeding_count': breeding_count,
        'planned_breeding': planned_breeding,
        'pregnant_count': pregnant_count,
        'successful_breeding': successful_breeding,
        'failed_breeding': failed_breeding,
        'births_recorded': births_recorded,
        'total_offspring': total_offspring,
        'breeding_success_rate': breeding_success_rate,
        'recent_breeding': recent_breeding,

        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_profit': net_profit,
        'income_count': income_count,
        'expense_count': expense_count,

        'financial_trend_labels': financial_trend_labels,
        'financial_trend_income': financial_trend_income,
        'financial_trend_expenses': financial_trend_expenses,
        'financial_trend_profit': financial_trend_profit,

        'farm': farm,

        'alerts': alerts,
        'alert_count': alert_count,
        'overdue_alert_count': overdue_alert_count,
        'warning_alert_count': warning_alert_count,
        'health_alert_count': health_alert_count,

        'user_role': get_user_role(request.user),
    }

    return render(
        request,
        'livestock/dashboard.html',
        context
    )


# ============================================================
# LIVESTOCK
# ============================================================

@login_required(login_url='login')
def livestock_list(request):

    animals = Animal.objects.all().order_by('-created_at')

    q = request.GET.get('q', '').strip()
    species = request.GET.get('species', '').strip()
    sex = request.GET.get('sex', '').strip()
    status = request.GET.get('status', '').strip()

    if q:
        animals = animals.filter(
            Q(animal_id__icontains=q) |
            Q(breed__icontains=q)
        )

    if species:
        animals = animals.filter(
            species=species
        )

    if sex:
        animals = animals.filter(
            sex=sex
        )

    if status:
        animals = animals.filter(
            status=status
        )

    active_count = Animal.objects.filter(
        status='ACTIVE'
    ).count()

    cow_count = Animal.objects.filter(
        species='COW',
        status='ACTIVE'
    ).count()

    goat_count = Animal.objects.filter(
        species='GOAT',
        status='ACTIVE'
    ).count()

    sheep_count = Animal.objects.filter(
        species='SHEEP',
        status='ACTIVE'
    ).count()

    male_count = Animal.objects.filter(
        sex='MALE',
        status='ACTIVE'
    ).count()

    female_count = Animal.objects.filter(
        sex='FEMALE',
        status='ACTIVE'
    ).count()

    context = {
        'animals': animals,
        'active_count': active_count,
        'cow_count': cow_count,
        'goat_count': goat_count,
        'sheep_count': sheep_count,
        'male_count': male_count,
        'female_count': female_count,
    }

    return render(
        request,
        'livestock/livestock_list.html',
        context
    )


# ============================================================
# ADD ANIMAL
# ============================================================

@login_required(login_url='login')
@role_required(ADMINISTRATOR, FARM_MANAGER)
def add_animal(request):

    if request.method == 'POST':

        animal_id = request.POST.get('animal_id')
        species = request.POST.get('species')
        breed = request.POST.get('breed')
        sex = request.POST.get('sex')
        date_of_birth = request.POST.get('date_of_birth') or None
        colour = request.POST.get('colour')
        weight = request.POST.get('weight') or None
        date_acquired = request.POST.get('date_acquired') or None
        status = request.POST.get('status')
        notes = request.POST.get('notes')

        animal = Animal.objects.create(
            animal_id=animal_id,
            species=species,
            breed=breed,
            sex=sex,
            date_of_birth=date_of_birth,
            colour=colour,
            weight=weight,
            date_acquired=date_acquired,
            status=status,
            notes=notes,
        )

        log_activity(
            request.user,
            'CREATE',
            'Livestock',
            f'Added animal {animal.animal_id}.'
        )

        return redirect('livestock_list')

    return render(
        request,
        'livestock/add_animal.html'
    )


# ============================================================
# ANIMAL DETAIL
# ============================================================

@login_required(login_url='login')
def animal_detail(request, animal_id):

    animal = get_object_or_404(
        Animal,
        animal_id=animal_id
    )

    health_records = HealthRecord.objects.filter(
        animal=animal
    ).order_by(
        '-date',
        '-created_at'
    )

    health_count = health_records.count()

    vaccination_count = health_records.filter(
        record_type='VACCINATION'
    ).count()

    treatment_count = health_records.filter(
        record_type='TREATMENT'
    ).count()

    illness_count = health_records.filter(
        record_type='ILLNESS'
    ).count()

    vet_visit_count = health_records.filter(
        record_type='VET_VISIT'
    ).count()

    breeding_records = BreedingRecord.objects.filter(
        female=animal
    ).select_related(
        'female',
        'male'
    ).order_by(
        '-breeding_date',
        '-created_at'
    )

    breeding_count = breeding_records.count()

    production_records = ProductionRecord.objects.filter(
        animal=animal
    ).order_by(
        '-date',
        '-created_at'
    )

    production_count = production_records.count()

    milk_total = production_records.filter(
        production_type='MILK'
    ).aggregate(
        total=Sum('quantity')
    )['total'] or 0

    meat_total = production_records.filter(
        production_type='MEAT'
    ).aggregate(
        total=Sum('quantity')
    )['total'] or 0

    weight_total = production_records.filter(
        production_type='WEIGHT'
    ).aggregate(
        total=Sum('quantity')
    )['total'] or 0

    financial_records = FinancialRecord.objects.filter(
        animal=animal
    ).order_by(
        '-date',
        '-created_at'
    )

    total_income = financial_records.filter(
        record_type='INCOME'
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    total_expenses = financial_records.filter(
        record_type='EXPENSE'
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    animal_profit = total_income - total_expenses

    context = {
        'animal': animal,

        'health_records': health_records,
        'health_count': health_count,
        'vaccination_count': vaccination_count,
        'treatment_count': treatment_count,
        'illness_count': illness_count,
        'vet_visit_count': vet_visit_count,

        'breeding_records': breeding_records,
        'breeding_count': breeding_count,

        'production_records': production_records,
        'production_count': production_count,
        'milk_total': milk_total,
        'meat_total': meat_total,
        'weight_total': weight_total,

        'financial_records': financial_records,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'animal_profit': animal_profit,
    }

    return render(
        request,
        'livestock/animal_detail.html',
        context
    )


# ============================================================
# EDIT ANIMAL
# ============================================================

@login_required(login_url='login')
@role_required(ADMINISTRATOR, FARM_MANAGER)
def edit_animal(request, animal_id):

    animal = get_object_or_404(
        Animal,
        animal_id=animal_id
    )

    if request.method == 'POST':

        animal.animal_id = request.POST.get('animal_id')
        animal.species = request.POST.get('species')
        animal.breed = request.POST.get('breed')
        animal.sex = request.POST.get('sex')
        animal.date_of_birth = (
            request.POST.get('date_of_birth') or None
        )
        animal.colour = request.POST.get('colour')
        animal.weight = (
            request.POST.get('weight') or None
        )
        animal.date_acquired = (
            request.POST.get('date_acquired') or None
        )
        animal.status = request.POST.get('status')
        animal.notes = request.POST.get('notes')

        animal.save()

        log_activity(
            request.user,
            'UPDATE',
            'Livestock',
            f'Updated animal {animal.animal_id}.'
        )

        return redirect(
            'animal_detail',
            animal_id=animal.animal_id
        )

    return render(
        request,
        'livestock/edit_animal.html',
        {'animal': animal}
    )


# ============================================================
# DELETE ANIMAL
# ============================================================

@login_required(login_url='login')
@role_required(ADMINISTRATOR)
def delete_animal(request, animal_id):

    animal = get_object_or_404(
        Animal,
        animal_id=animal_id
    )

    if request.method == 'POST':

        deleted_animal_id = animal.animal_id

        animal.delete()

        log_activity(
            request.user,
            'DELETE',
            'Livestock',
            f'Deleted animal {deleted_animal_id}.'
        )

        return redirect(
            'livestock_list'
        )

    return render(
        request,
        'livestock/delete_animal.html',
        {'animal': animal}
    )


# ============================================================
# HEALTH RECORDS
# ============================================================

@login_required(login_url='login')
def health_records(request, animal_id):

    animal = get_object_or_404(
        Animal,
        animal_id=animal_id
    )

    records = animal.health_records.all().order_by(
        '-date',
        '-created_at'
    )

    return render(
        request,
        'livestock/health_records.html',
        {
            'animal': animal,
            'records': records,
        }
    )


@login_required(login_url='login')
@role_required(
    ADMINISTRATOR,
    FARM_MANAGER,
    FARM_WORKER
)
def add_health_record(request, animal_id):

    animal = get_object_or_404(
        Animal,
        animal_id=animal_id
    )

    if request.method == 'POST':

        health_record = HealthRecord.objects.create(
            animal=animal,
            record_type=request.POST.get('record_type'),
            date=request.POST.get('date'),
            next_due_date=(
                request.POST.get('next_due_date') or None
            ),
            description=request.POST.get('description'),
            medication=request.POST.get('medication'),
            veterinarian=request.POST.get('veterinarian'),
            notes=request.POST.get('notes'),
        )

        log_activity(
            request.user,
            'CREATE',
            'Health',
            f'Added {health_record.get_record_type_display()} record for {animal.animal_id}.'
        )

        return redirect(
            'health_records',
            animal_id=animal.animal_id
        )

    return render(
        request,
        'livestock/add_health_record.html',
        {'animal': animal}
    )


# ============================================================
# EDIT HEALTH RECORD
# ============================================================

@login_required(login_url='login')
@role_required(
    ADMINISTRATOR,
    FARM_MANAGER
)
def edit_health_record(request, record_id):

    health_record = get_object_or_404(
        HealthRecord,
        id=record_id
    )

    if request.method == 'POST':

        health_record.record_type = request.POST.get(
            'record_type'
        )

        health_record.date = request.POST.get(
            'date'
        )

        health_record.next_due_date = (
            request.POST.get('next_due_date') or None
        )

        health_record.description = request.POST.get(
            'description'
        )

        health_record.medication = request.POST.get(
            'medication'
        )

        health_record.veterinarian = request.POST.get(
            'veterinarian'
        )

        health_record.notes = request.POST.get(
            'notes'
        )

        health_record.save()

        log_activity(
            request.user,
            'UPDATE',
            'Health',
            f'Updated health record for '
            f'{health_record.animal.animal_id}.'
        )

        return redirect(
            'health_records',
            animal_id=health_record.animal.animal_id
        )

    return render(
        request,
        'livestock/edit_health_record.html',
        {
            'record': health_record,
            'animal': health_record.animal,
        }
    )


# ============================================================
# DELETE HEALTH RECORD
# ============================================================

@login_required(login_url='login')
@role_required(
    ADMINISTRATOR
)
def delete_health_record(request, record_id):

    health_record = get_object_or_404(
        HealthRecord,
        id=record_id
    )

    animal_id = health_record.animal.animal_id

    if request.method == 'POST':

        record_type = (
            health_record.get_record_type_display()
        )

        health_record.delete()

        log_activity(
            request.user,
            'DELETE',
            'Health',
            f'Deleted {record_type} health record '
            f'for {animal_id}.'
        )

        return redirect(
            'health_records',
            animal_id=animal_id
        )

    return render(
        request,
        'livestock/delete_health_record.html',
        {
            'record': health_record,
            'animal': health_record.animal,
        }
    )


# ============================================================
# BREEDING RECORDS
# ============================================================

@login_required(login_url='login')
def breeding_records(request, animal_id):

    animal = get_object_or_404(
        Animal,
        animal_id=animal_id
    )

    records = BreedingRecord.objects.filter(
        female=animal
    ).select_related(
        'female',
        'male'
    ).order_by(
        '-breeding_date',
        '-created_at'
    )

    today = date.today()

    total_records = records.count()

    planned_count = records.filter(
        status='PLANNED'
    ).count()

    pregnant_count = records.filter(
        status='PREGNANT'
    ).count()

    successful_count = records.filter(
        status='SUCCESSFUL'
    ).count()

    failed_count = records.filter(
        status='FAILED'
    ).count()

    born_count = records.filter(
        status='BORN'
    ).count()

    total_offspring = records.filter(
        offspring_count__isnull=False
    ).aggregate(
        total=Sum('offspring_count')
    )['total'] or 0

    upcoming_births = records.filter(
        expected_birth_date__isnull=False,
        expected_birth_date__gte=today,
        actual_birth_date__isnull=True
    ).order_by(
        'expected_birth_date'
    )

    overdue_births = records.filter(
        expected_birth_date__isnull=False,
        expected_birth_date__lt=today,
        actual_birth_date__isnull=True
    ).exclude(
        status='BORN'
    ).order_by(
        'expected_birth_date'
    )

    for record in records:

        record.days_until_birth = None
        record.birth_status = None

        if record.expected_birth_date:

            days = (
                record.expected_birth_date - today
            ).days

            record.days_until_birth = days

            if record.actual_birth_date:
                record.birth_status = 'COMPLETED'

            elif days < 0:
                record.birth_status = 'OVERDUE'

            elif days == 0:
                record.birth_status = 'DUE TODAY'

            elif days <= 7:
                record.birth_status = 'DUE SOON'

            else:
                record.birth_status = 'UPCOMING'

    next_birth = upcoming_births.first()

    days_to_next_birth = None

    if next_birth:

        days_to_next_birth = (
            next_birth.expected_birth_date - today
        ).days

    completed_attempts = (
        successful_count +
        failed_count +
        born_count
    )

    if completed_attempts > 0:

        breeding_success_rate = (
            (successful_count + born_count)
            / completed_attempts
        ) * 100

    else:

        breeding_success_rate = 0

    context = {
        'animal': animal,
        'records': records,

        'total_records': total_records,
        'planned_count': planned_count,
        'pregnant_count': pregnant_count,
        'successful_count': successful_count,
        'failed_count': failed_count,
        'born_count': born_count,

        'total_offspring': total_offspring,

        'upcoming_births': upcoming_births,
        'overdue_births': overdue_births,
        'next_birth': next_birth,
        'days_to_next_birth': days_to_next_birth,

        'breeding_success_rate': round(
            breeding_success_rate,
            1
        ),
    }

    return render(
        request,
        'livestock/breeding_records.html',
        context
    )


@login_required(login_url='login')
@role_required(
    ADMINISTRATOR,
    FARM_MANAGER
)
def add_breeding_record(request, animal_id):

    animal = get_object_or_404(
        Animal,
        animal_id=animal_id
    )

    if request.method == 'POST':

        male_id = request.POST.get('male')

        male = None

        if male_id:

            male = get_object_or_404(
                Animal,
                animal_id=male_id
            )

        breeding_record = BreedingRecord.objects.create(
            female=animal,
            male=male,
            breeding_date=request.POST.get('breeding_date'),
            expected_birth_date=(
                request.POST.get('expected_birth_date')
                or None
            ),
            actual_birth_date=(
                request.POST.get('actual_birth_date')
                or None
            ),
            offspring_count=(
                request.POST.get('offspring_count')
                or None
            ),
            status=request.POST.get('status'),
            notes=request.POST.get('notes'),
        )

        log_activity(
            request.user,
            'CREATE',
            'Breeding',
            f'Added breeding record for {animal.animal_id}.'
        )

        return redirect(
            'breeding_records',
            animal_id=animal.animal_id
        )

    male_animals = Animal.objects.filter(
        sex='MALE',
        status='ACTIVE'
    ).exclude(
        animal_id=animal.animal_id
    ).order_by('animal_id')

    return render(
        request,
        'livestock/add_breeding_record.html',
        {
            'animal': animal,
            'male_animals': male_animals,
        }
    )


# ============================================================
# EDIT BREEDING RECORD
# ============================================================

@login_required(login_url='login')
@role_required(
    ADMINISTRATOR,
    FARM_MANAGER
)
def edit_breeding_record(request, record_id):

    breeding_record = get_object_or_404(
        BreedingRecord,
        id=record_id
    )

    animal = breeding_record.female

    if request.method == 'POST':

        male_id = request.POST.get('male')

        male = None

        if male_id:

            male = get_object_or_404(
                Animal,
                animal_id=male_id
            )

        breeding_record.male = male

        breeding_record.breeding_date = (
            request.POST.get('breeding_date')
        )

        breeding_record.expected_birth_date = (
            request.POST.get('expected_birth_date')
            or None
        )

        breeding_record.actual_birth_date = (
            request.POST.get('actual_birth_date')
            or None
        )

        breeding_record.offspring_count = (
            request.POST.get('offspring_count')
            or None
        )

        breeding_record.status = (
            request.POST.get('status')
        )

        breeding_record.notes = (
            request.POST.get('notes')
        )

        breeding_record.save()

        log_activity(
            request.user,
            'UPDATE',
            'Breeding',
            f'Updated breeding record for '
            f'{animal.animal_id}.'
        )

        return redirect(
            'breeding_records',
            animal_id=animal.animal_id
        )

    male_animals = Animal.objects.filter(
        sex='MALE'
    ).exclude(
        animal_id=animal.animal_id
    ).filter(
        Q(status='ACTIVE') |
        Q(id=breeding_record.male_id)
    ).order_by(
        'animal_id'
    )

    return render(
        request,
        'livestock/edit_breeding_record.html',
        {
            'record': breeding_record,
            'animal': animal,
            'male_animals': male_animals,
        }
    )


# ============================================================
# DELETE BREEDING RECORD
# ============================================================

@login_required(login_url='login')
@role_required(
    ADMINISTRATOR
)
def delete_breeding_record(request, record_id):

    breeding_record = get_object_or_404(
        BreedingRecord,
        id=record_id
    )

    animal = breeding_record.female

    animal_id = animal.animal_id

    breeding_date = breeding_record.breeding_date

    if request.method == 'POST':

        breeding_record.delete()

        log_activity(
            request.user,
            'DELETE',
            'Breeding',
            f'Deleted breeding record for '
            f'{animal_id} dated {breeding_date}.'
        )

        return redirect(
            'breeding_records',
            animal_id=animal_id
        )

    return render(
        request,
        'livestock/delete_breeding_record.html',
        {
            'record': breeding_record,
            'animal': animal,
        }
    )


# ============================================================
# PRODUCTION RECORDS
# ============================================================

@login_required(login_url='login')
def production_records(request, animal_id):

    animal = get_object_or_404(
        Animal,
        animal_id=animal_id
    )

    records = ProductionRecord.objects.filter(
        animal=animal
    ).order_by(
        '-date',
        '-created_at'
    )

    today = date.today()

    total_records = records.count()

    milk_records = records.filter(
        production_type='MILK'
    )

    meat_records = records.filter(
        production_type='MEAT'
    )

    weight_records = records.filter(
        production_type='WEIGHT'
    )

    milk_count = milk_records.count()
    meat_count = meat_records.count()
    weight_count = weight_records.count()

    milk_total = milk_records.aggregate(
        total=Sum('quantity')
    )['total'] or 0

    meat_total = meat_records.aggregate(
        total=Sum('quantity')
    )['total'] or 0

    weight_total = weight_records.aggregate(
        total=Sum('quantity')
    )['total'] or 0

    average_milk = milk_records.aggregate(
        average=Avg('quantity')
    )['average'] or 0

    average_meat = meat_records.aggregate(
        average=Avg('quantity')
    )['average'] or 0

    average_weight = weight_records.aggregate(
        average=Avg('quantity')
    )['average'] or 0

    month_start = date(
        today.year,
        today.month,
        1
    )

    month_records = records.filter(
        date__gte=month_start,
        date__lte=today
    )

    this_month_milk = month_records.filter(
        production_type='MILK'
    ).aggregate(
        total=Sum('quantity')
    )['total'] or 0

    this_month_meat = month_records.filter(
        production_type='MEAT'
    ).aggregate(
        total=Sum('quantity')
    )['total'] or 0

    this_month_weight = month_records.filter(
        production_type='WEIGHT'
    ).aggregate(
        total=Sum('quantity')
    )['total'] or 0

    seven_days_ago = today - timedelta(days=6)

    last_7_days = records.filter(
        date__gte=seven_days_ago,
        date__lte=today
    )

    last_7_days_milk = last_7_days.filter(
        production_type='MILK'
    ).aggregate(
        total=Sum('quantity')
    )['total'] or 0

    last_7_days_meat = last_7_days.filter(
        production_type='MEAT'
    ).aggregate(
        total=Sum('quantity')
    )['total'] or 0

    last_7_days_weight = last_7_days.filter(
        production_type='WEIGHT'
    ).aggregate(
        total=Sum('quantity')
    )['total'] or 0

    production_type_summary = []

    for type_code, type_name in ProductionRecord.PRODUCTION_TYPE_CHOICES:

        type_records = records.filter(
            production_type=type_code
        )

        total = type_records.aggregate(
            total=Sum('quantity')
        )['total'] or 0

        count = type_records.count()

        average = type_records.aggregate(
            average=Avg('quantity')
        )['average'] or 0

        production_type_summary.append({
            'code': type_code,
            'name': type_name,
            'total': total,
            'count': count,
            'average': average,
        })

    trend_labels = []
    trend_milk = []
    trend_meat = []
    trend_weight = []

    trend_start = today - timedelta(days=29)

    for day_offset in range(30):

        current_day = (
            trend_start +
            timedelta(days=day_offset)
        )

        daily_milk = records.filter(
            date=current_day,
            production_type='MILK'
        ).aggregate(
            total=Sum('quantity')
        )['total'] or 0

        daily_meat = records.filter(
            date=current_day,
            production_type='MEAT'
        ).aggregate(
            total=Sum('quantity')
        )['total'] or 0

        daily_weight = records.filter(
            date=current_day,
            production_type='WEIGHT'
        ).aggregate(
            total=Sum('quantity')
        )['total'] or 0

        trend_labels.append(
            current_day.strftime('%d %b')
        )

        trend_milk.append(
            float(daily_milk)
        )

        trend_meat.append(
            float(daily_meat)
        )

        trend_weight.append(
            float(daily_weight)
        )

    recent_production = records[:10]

    latest_record = records.first()

    highest_record = records.order_by(
        '-quantity'
    ).first()

    production_days = records.values(
        'date'
    ).distinct().count()

    for record in records:

        record.days_ago = None

        if record.date:

            record.days_ago = (
                today - record.date
            ).days

    context = {
        'animal': animal,
        'records': records,

        'total_records': total_records,

        'milk_count': milk_count,
        'meat_count': meat_count,
        'weight_count': weight_count,

        'milk_total': milk_total,
        'meat_total': meat_total,
        'weight_total': weight_total,

        'average_milk': average_milk,
        'average_meat': average_meat,
        'average_weight': average_weight,

        'this_month_milk': this_month_milk,
        'this_month_meat': this_month_meat,
        'this_month_weight': this_month_weight,

        'last_7_days_milk': last_7_days_milk,
        'last_7_days_meat': last_7_days_meat,
        'last_7_days_weight': last_7_days_weight,

        'latest_record': latest_record,
        'highest_record': highest_record,
        'production_days': production_days,

        'production_type_summary': production_type_summary,

        'trend_labels': trend_labels,
        'trend_milk': trend_milk,
        'trend_meat': trend_meat,
        'trend_weight': trend_weight,

        'recent_production': recent_production,
    }

    return render(
        request,
        'livestock/production_records.html',
        context
    )


@login_required(login_url='login')
@role_required(
    ADMINISTRATOR,
    FARM_MANAGER,
    FARM_WORKER
)
def add_production_record(request, animal_id):

    animal = get_object_or_404(
        Animal,
        animal_id=animal_id
    )

    if request.method == 'POST':

        production_record = ProductionRecord.objects.create(
            animal=animal,
            production_type=request.POST.get(
                'production_type'
            ),
            date=request.POST.get('date'),
            quantity=request.POST.get('quantity'),
            unit=request.POST.get('unit'),
            notes=request.POST.get('notes'),
        )

        log_activity(
            request.user,
            'CREATE',
            'Production',
            f'Added {production_record.get_production_type_display()} production record for {animal.animal_id}.'
        )

        return redirect(
            'production_records',
            animal_id=animal.animal_id
        )

    return render(
        request,
        'livestock/add_production_record.html',
        {'animal': animal}
    )


# ============================================================
# EDIT PRODUCTION RECORD
# ============================================================

@login_required(login_url='login')
@role_required(
    ADMINISTRATOR,
    FARM_MANAGER
)
def edit_production_record(request, record_id):

    production_record = get_object_or_404(
        ProductionRecord,
        id=record_id
    )

    animal = production_record.animal

    if request.method == 'POST':

        production_record.production_type = request.POST.get(
            'production_type'
        )

        production_record.date = request.POST.get(
            'date'
        )

        production_record.quantity = request.POST.get(
            'quantity'
        )

        production_record.unit = request.POST.get(
            'unit'
        )

        production_record.notes = request.POST.get(
            'notes'
        )

        production_record.save()

        log_activity(
            request.user,
            'UPDATE',
            'Production',
            f'Updated {production_record.get_production_type_display()} production record for {animal.animal_id}.'
        )

        return redirect(
            'production_records',
            animal_id=animal.animal_id
        )

    return render(
        request,
        'livestock/edit_production_record.html',
        {
            'record': production_record,
            'animal': animal,
        }
    )


# ============================================================
# DELETE PRODUCTION RECORD
# ============================================================

@login_required(login_url='login')
@role_required(
    ADMINISTRATOR
)
def delete_production_record(request, record_id):

    production_record = get_object_or_404(
        ProductionRecord,
        id=record_id
    )

    animal_id = production_record.animal.animal_id

    if request.method == 'POST':

        production_type = (
            production_record.get_production_type_display()
        )

        production_date = production_record.date

        production_record.delete()

        log_activity(
            request.user,
            'DELETE',
            'Production',
            f'Deleted {production_type} production record for {animal_id} dated {production_date}.'
        )

        return redirect(
            'production_records',
            animal_id=animal_id
        )

    return render(
        request,
        'livestock/delete_production_record.html',
        {
            'record': production_record,
            'animal': production_record.animal,
        }
    )


# ============================================================
# FARM-WIDE RECORDS
# ============================================================

@login_required(login_url='login')
def all_health_records(request):

    records = HealthRecord.objects.all().select_related(
        'animal'
    ).order_by(
        '-date',
        '-created_at'
    )

    return render(
        request,
        'livestock/all_health_records.html',
        {'records': records}
    )


@login_required(login_url='login')
def all_breeding_records(request):

    records = BreedingRecord.objects.all().select_related(
        'female',
        'male'
    ).order_by(
        '-breeding_date',
        '-created_at'
    )

    return render(
        request,
        'livestock/all_breeding_records.html',
        {'records': records}
    )


@login_required(login_url='login')
def all_production_records(request):

    records = ProductionRecord.objects.all().select_related(
        'animal'
    ).order_by(
        '-date',
        '-created_at'
    )

    return render(
        request,
        'livestock/all_production_records.html',
        {'records': records}
    )


# ============================================================
# REPORTS & ANALYTICS
# ============================================================

@login_required(login_url='login')
@role_required(
    ADMINISTRATOR,
    FARM_MANAGER
)
def reports(request):

    # ========================================================
    # ANIMAL STATISTICS
    # ========================================================

    total_animals = Animal.objects.count()

    active_animals = Animal.objects.filter(
        status='ACTIVE'
    ).count()

    sold_animals = Animal.objects.filter(
        status='SOLD'
    ).count()

    deceased_animals = Animal.objects.filter(
        status='DECEASED'
    ).count()

    cows = Animal.objects.filter(
        species='COW'
    ).count()

    goats = Animal.objects.filter(
        species='GOAT'
    ).count()

    sheep = Animal.objects.filter(
        species='SHEEP'
    ).count()

    males = Animal.objects.filter(
        sex='MALE'
    ).count()

    females = Animal.objects.filter(
        sex='FEMALE'
    ).count()

    average_weight = Animal.objects.filter(
        weight__isnull=False
    ).aggregate(
        average=Avg('weight')
    )['average']

    # ========================================================
    # HEALTH STATISTICS
    # ========================================================

    health_count = HealthRecord.objects.count()

    vaccination_count = HealthRecord.objects.filter(
        record_type='VACCINATION'
    ).count()

    treatment_count = HealthRecord.objects.filter(
        record_type='TREATMENT'
    ).count()

    illness_count = HealthRecord.objects.filter(
        record_type='ILLNESS'
    ).count()

    vet_visit_count = HealthRecord.objects.filter(
        record_type='VET_VISIT'
    ).count()

    other_health_count = HealthRecord.objects.filter(
        record_type='OTHER'
    ).count()

    # ========================================================
    # BREEDING STATISTICS
    # ========================================================

    breeding_count = BreedingRecord.objects.count()

    planned_breeding = BreedingRecord.objects.filter(
        status='PLANNED'
    ).count()

    pregnant_count = BreedingRecord.objects.filter(
        status='PREGNANT'
    ).count()

    successful_breeding = BreedingRecord.objects.filter(
        status='SUCCESSFUL'
    ).count()

    failed_breeding = BreedingRecord.objects.filter(
        status='FAILED'
    ).count()

    births_recorded = BreedingRecord.objects.filter(
        status='BORN'
    ).count()

    total_offspring = BreedingRecord.objects.filter(
        offspring_count__isnull=False
    ).aggregate(
        total=Sum('offspring_count')
    )['total'] or 0

    # ========================================================
    # PRODUCTION STATISTICS
    # ========================================================

    production_count = ProductionRecord.objects.count()

    total_milk = ProductionRecord.objects.filter(
        production_type='MILK'
    ).aggregate(
        total=Sum('quantity')
    )['total'] or 0

    total_meat = ProductionRecord.objects.filter(
        production_type='MEAT'
    ).aggregate(
        total=Sum('quantity')
    )['total'] or 0

    total_weight_records = ProductionRecord.objects.filter(
        production_type='WEIGHT'
    ).aggregate(
        total=Sum('quantity')
    )['total'] or 0

    # ========================================================
    # FINANCIAL STATISTICS
    # ========================================================

    total_income = FinancialRecord.objects.filter(
        record_type='INCOME'
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    total_expenses = FinancialRecord.objects.filter(
        record_type='EXPENSE'
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    net_profit = total_income - total_expenses

    # ========================================================
    # CHART DATA
    # ========================================================

    species_labels = [
        'Cows',
        'Goats',
        'Sheep'
    ]

    species_values = [
        cows,
        goats,
        sheep
    ]

    health_labels = [
        'Vaccination',
        'Treatment',
        'Illness',
        'Vet Visit',
        'Other',
    ]

    health_values = [
        vaccination_count,
        treatment_count,
        illness_count,
        vet_visit_count,
        other_health_count,
    ]

    breeding_labels = [
        'Planned',
        'Pregnant',
        'Successful',
        'Failed',
        'Born',
    ]

    breeding_values = [
        planned_breeding,
        pregnant_count,
        successful_breeding,
        failed_breeding,
        births_recorded,
    ]

    # ========================================================
    # MONTHLY REPORT DATA
    # ========================================================

    today = date.today()

    monthly_labels = []
    monthly_milk = []
    monthly_meat = []
    monthly_weight = []
    monthly_income = []
    monthly_expenses = []

    for month_offset in range(11, -1, -1):

        month_number = today.month - month_offset
        year = today.year

        while month_number <= 0:
            month_number += 12
            year -= 1

        month_start = date(
            year,
            month_number,
            1
        )

        if month_number == 12:

            next_month = date(
                year + 1,
                1,
                1
            )

        else:

            next_month = date(
                year,
                month_number + 1,
                1
            )

        monthly_labels.append(
            month_start.strftime('%b %Y')
        )

        monthly_milk.append(
            float(
                ProductionRecord.objects.filter(
                    production_type='MILK',
                    date__gte=month_start,
                    date__lt=next_month
                ).aggregate(
                    total=Sum('quantity')
                )['total'] or 0
            )
        )

        monthly_meat.append(
            float(
                ProductionRecord.objects.filter(
                    production_type='MEAT',
                    date__gte=month_start,
                    date__lt=next_month
                ).aggregate(
                    total=Sum('quantity')
                )['total'] or 0
            )
        )

        monthly_weight.append(
            float(
                ProductionRecord.objects.filter(
                    production_type='WEIGHT',
                    date__gte=month_start,
                    date__lt=next_month
                ).aggregate(
                    total=Sum('quantity')
                )['total'] or 0
            )
        )

        monthly_income.append(
            float(
                FinancialRecord.objects.filter(
                    record_type='INCOME',
                    date__gte=month_start,
                    date__lt=next_month
                ).aggregate(
                    total=Sum('amount')
                )['total'] or 0
            )
        )

        monthly_expenses.append(
            float(
                FinancialRecord.objects.filter(
                    record_type='EXPENSE',
                    date__gte=month_start,
                    date__lt=next_month
                ).aggregate(
                    total=Sum('amount')
                )['total'] or 0
            )
        )

    # ========================================================
    # ANIMAL PERFORMANCE
    # ========================================================

    milk_rows = list(
        ProductionRecord.objects.filter(
            production_type='MILK'
        ).values(
            'animal'
        ).annotate(
            total=Sum('quantity')
        ).order_by(
            '-total'
        )[:5]
    )

    meat_rows = list(
        ProductionRecord.objects.filter(
            production_type='MEAT'
        ).values(
            'animal'
        ).annotate(
            total=Sum('quantity')
        ).order_by(
            '-total'
        )[:5]
    )

    active_rows = list(
        ProductionRecord.objects.values(
            'animal'
        ).annotate(
            total_records=Count('id')
        ).order_by(
            '-total_records'
        )[:5]
    )

    animal_ids = {
        row['animal']
        for row in milk_rows + meat_rows + active_rows
        if row['animal']
    }

    animals_by_pk = {
        animal.pk: animal
        for animal in Animal.objects.filter(
            pk__in=animal_ids
        )
    }

    top_milk_producers = [
        {
            'animal': animals_by_pk.get(
                row['animal']
            ),
            'total': row['total'] or 0,
        }
        for row in milk_rows
        if animals_by_pk.get(row['animal'])
    ]

    top_meat_producers = [
        {
            'animal': animals_by_pk.get(
                row['animal']
            ),
            'total': row['total'] or 0,
        }
        for row in meat_rows
        if animals_by_pk.get(row['animal'])
    ]

    top_active_animals = [
        {
            'animal': animals_by_pk.get(
                row['animal']
            ),
            'total_records': row['total_records'] or 0,
        }
        for row in active_rows
        if animals_by_pk.get(row['animal'])
    ]

    # ========================================================
    # ANIMAL PROFITABILITY
    # ========================================================

    profitability_rows = list(
        FinancialRecord.objects.filter(
            animal__isnull=False
        ).values(
            'animal'
        ).annotate(
            total_income=Sum(
                'amount',
                filter=Q(record_type='INCOME')
            ),
            total_expenses=Sum(
                'amount',
                filter=Q(record_type='EXPENSE')
            ),
        )
    )

    profitability_ids = {
        row['animal']
        for row in profitability_rows
        if row['animal']
    }

    profitability_animals = {
        animal.pk: animal
        for animal in Animal.objects.filter(
            pk__in=profitability_ids
        )
    }

    animal_profitability = []

    for row in profitability_rows:

        animal = profitability_animals.get(
            row['animal']
        )

        if animal:

            income = row['total_income'] or 0
            expenses = row['total_expenses'] or 0

            animal_profitability.append({
                'animal': animal,
                'total_income': income,
                'total_expenses': expenses,
                'profit': income - expenses,
            })

    animal_profitability.sort(
        key=lambda item: item['profit'],
        reverse=True
    )

    top_profitable_animals = animal_profitability[:5]

    least_profitable_animals = list(
        reversed(
            animal_profitability[-5:]
        )
    )

    # ========================================================
    # RECENT RECORDS
    # ========================================================

    recent_production = ProductionRecord.objects.select_related(
        'animal'
    ).order_by(
        '-date',
        '-created_at'
    )[:10]

    recent_health = HealthRecord.objects.select_related(
        'animal'
    ).order_by(
        '-date',
        '-created_at'
    )[:10]

    recent_breeding = BreedingRecord.objects.select_related(
        'female',
        'male'
    ).order_by(
        '-breeding_date',
        '-created_at'
    )[:10]

    # ========================================================
    # REPORT CONTEXT
    # ========================================================

    context = {
        'total_animals': total_animals,
        'active_animals': active_animals,
        'sold_animals': sold_animals,
        'deceased_animals': deceased_animals,

        'cows': cows,
        'goats': goats,
        'sheep': sheep,
        'males': males,
        'females': females,
        'average_weight': average_weight,

        'health_count': health_count,
        'breeding_count': breeding_count,
        'production_count': production_count,

        'vaccination_count': vaccination_count,
        'treatment_count': treatment_count,
        'illness_count': illness_count,
        'vet_visit_count': vet_visit_count,
        'other_health_count': other_health_count,

        'planned_breeding': planned_breeding,
        'pregnant_count': pregnant_count,
        'successful_breeding': successful_breeding,
        'failed_breeding': failed_breeding,
        'births_recorded': births_recorded,
        'total_offspring': total_offspring,

        'total_milk': total_milk,
        'total_meat': total_meat,
        'total_weight_records': total_weight_records,

        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_profit': net_profit,

        'species_labels': species_labels,
        'species_values': species_values,

        'health_labels': health_labels,
        'health_values': health_values,

        'breeding_labels': breeding_labels,
        'breeding_values': breeding_values,

        'monthly_labels': monthly_labels,
        'monthly_milk': monthly_milk,
        'monthly_meat': monthly_meat,
        'monthly_weight': monthly_weight,
        'monthly_income': monthly_income,
        'monthly_expenses': monthly_expenses,

        'top_milk_producers': top_milk_producers,
        'top_meat_producers': top_meat_producers,
        'top_active_animals': top_active_animals,

        'top_profitable_animals': top_profitable_animals,
        'least_profitable_animals': least_profitable_animals,

        'recent_production': recent_production,
        'recent_health': recent_health,
        'recent_breeding': recent_breeding,

        'user_role': get_user_role(request.user),
    }

    return render(
        request,
        'livestock/reports.html',
        context
    )


# ============================================================
# REPORT EXPORTS
# PDF / EXCEL / CSV
# ADMINISTRATOR + FARM MANAGER
# ============================================================


def _report_export_data(report_type):
    """
    Build database-backed datasets for report exports.

    Returns a dictionary where each key is a report section and
    each value contains a title plus tabular headers and rows.
    """

    report_type = (report_type or 'comprehensive').lower()

    sections = []

    if report_type in ('livestock', 'comprehensive'):
        animals = Animal.objects.all().order_by('animal_id')
        rows = []

        for animal in animals:
            rows.append([
                animal.animal_id,
                animal.get_species_display(),
                animal.breed or '',
                animal.get_sex_display(),
                animal.date_of_birth.strftime('%d %b %Y') if animal.date_of_birth else '',
                animal.colour or '',
                animal.weight if animal.weight is not None else '',
                animal.date_acquired.strftime('%d %b %Y') if animal.date_acquired else '',
                animal.get_status_display(),
                animal.notes or '',
            ])

        sections.append({
            'title': 'Livestock Report',
            'headers': [
                'Animal ID',
                'Species',
                'Breed',
                'Sex',
                'Date of Birth',
                'Colour',
                'Weight',
                'Date Acquired',
                'Status',
                'Notes',
            ],
            'rows': rows,
        })

    if report_type in ('health', 'comprehensive'):
        records = HealthRecord.objects.select_related(
            'animal'
        ).order_by('-date', '-created_at')

        rows = []
        for record in records:
            rows.append([
                record.date.strftime('%d %b %Y') if record.date else '',
                record.animal.animal_id,
                record.get_record_type_display(),
                record.next_due_date.strftime('%d %b %Y') if record.next_due_date else '',
                record.description or '',
                record.medication or '',
                record.veterinarian or '',
                record.notes or '',
            ])

        sections.append({
            'title': 'Health Records Report',
            'headers': [
                'Date',
                'Animal ID',
                'Record Type',
                'Next Due Date',
                'Description',
                'Medication',
                'Veterinarian',
                'Notes',
            ],
            'rows': rows,
        })

    if report_type in ('breeding', 'comprehensive'):
        records = BreedingRecord.objects.select_related(
            'female',
            'male'
        ).order_by('-breeding_date', '-created_at')

        rows = []
        for record in records:
            rows.append([
                record.breeding_date.strftime('%d %b %Y') if record.breeding_date else '',
                record.female.animal_id,
                record.male.animal_id if record.male else '',
                record.get_status_display(),
                record.expected_birth_date.strftime('%d %b %Y') if record.expected_birth_date else '',
                record.actual_birth_date.strftime('%d %b %Y') if record.actual_birth_date else '',
                record.offspring_count if record.offspring_count is not None else '',
                record.notes or '',
            ])

        sections.append({
            'title': 'Breeding Records Report',
            'headers': [
                'Breeding Date',
                'Female',
                'Male',
                'Status',
                'Expected Birth',
                'Actual Birth',
                'Offspring',
                'Notes',
            ],
            'rows': rows,
        })

    if report_type in ('production', 'comprehensive'):
        records = ProductionRecord.objects.select_related(
            'animal'
        ).order_by('-date', '-created_at')

        rows = []
        for record in records:
            rows.append([
                record.date.strftime('%d %b %Y') if record.date else '',
                record.animal.animal_id,
                record.get_production_type_display(),
                record.quantity,
                record.unit or '',
                record.notes or '',
            ])

        sections.append({
            'title': 'Production Records Report',
            'headers': [
                'Date',
                'Animal ID',
                'Production Type',
                'Quantity',
                'Unit',
                'Notes',
            ],
            'rows': rows,
        })

    if report_type in ('financial', 'comprehensive'):
        records = FinancialRecord.objects.select_related(
            'animal'
        ).order_by('-date', '-created_at')

        rows = []
        for record in records:
            rows.append([
                record.date.strftime('%d %b %Y') if record.date else '',
                record.get_record_type_display(),
                record.get_category_display(),
                record.amount,
                record.animal.animal_id if record.animal else '',
                record.description or '',
                record.notes or '',
            ])

        sections.append({
            'title': 'Financial Records Report',
            'headers': [
                'Date',
                'Record Type',
                'Category',
                'Amount (KSh)',
                'Animal ID',
                'Description',
                'Notes',
            ],
            'rows': rows,
        })

    return sections


def _report_title(report_type):
    titles = {
        'livestock': 'Livestock Report',
        'health': 'Health Records Report',
        'breeding': 'Breeding Records Report',
        'production': 'Production Records Report',
        'financial': 'Financial Records Report',
        'comprehensive': 'Comprehensive Farm Report',
    }
    return titles.get(
        (report_type or '').lower(),
        'Comprehensive Farm Report'
    )


def _export_csv(sections, filename):
    response = HttpResponse(
        content_type='text/csv; charset=utf-8'
    )
    response['Content-Disposition'] = (
        f'attachment; filename="{filename}.csv"'
    )

    writer = csv.writer(response)

    for index, section in enumerate(sections):
        if index:
            writer.writerow([])
            writer.writerow([])

        writer.writerow([section['title']])
        writer.writerow(section['headers'])

        for row in section['rows']:
            writer.writerow(row)

    return response


def _export_excel(sections, title, filename):
    workbook = Workbook()
    default_sheet = workbook.active
    workbook.remove(default_sheet)

    for index, section in enumerate(sections, start=1):
        sheet_name = section['title'].replace(' Report', '')[:31]
        if not sheet_name:
            sheet_name = f'Report {index}'

        worksheet = workbook.create_sheet(title=sheet_name)

        worksheet.append([title])
        worksheet.merge_cells(
            start_row=1,
            start_column=1,
            end_row=1,
            end_column=max(1, len(section['headers']))
        )

        worksheet['A1'].font = Font(
            bold=True,
            size=16,
            color='1B5E20'
        )
        worksheet['A1'].alignment = Alignment(
            horizontal='center'
        )

        worksheet.append([])
        worksheet.append(section['headers'])

        header_row = 3
        for cell in worksheet[header_row]:
            cell.font = Font(
                bold=True,
                color='FFFFFF'
            )
            cell.fill = PatternFill(
                fill_type='solid',
                fgColor='1B5E20'
            )
            cell.alignment = Alignment(
                horizontal='center',
                vertical='center'
            )

        for row in section['rows']:
            worksheet.append(row)

        worksheet.freeze_panes = 'A4'
        worksheet.auto_filter.ref = worksheet.dimensions

        for column_cells in worksheet.columns:
            max_length = 0
            column_letter = get_column_letter(
                column_cells[0].column
            )

            for cell in column_cells:
                value = '' if cell.value is None else str(cell.value)
                max_length = max(
                    max_length,
                    len(value)
                )

            worksheet.column_dimensions[
                column_letter
            ].width = min(
                max(max_length + 2, 12),
                35
            )

    output = BytesIO()
    workbook.save(output)
    output.seek(0)

    response = HttpResponse(
        output.getvalue(),
        content_type=(
            'application/vnd.openxmlformats-officedocument.'
            'spreadsheetml.sheet'
        )
    )
    response['Content-Disposition'] = (
        f'attachment; filename="{filename}.xlsx"'
    )

    return response


def _export_pdf(sections, title, filename):
    output = BytesIO()

    document = SimpleDocTemplate(
        output,
        pagesize=landscape(A4),
        rightMargin=12 * mm,
        leftMargin=12 * mm,
        topMargin=12 * mm,
        bottomMargin=12 * mm,
        title=title,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'ReportTitle',
        parent=styles['Title'],
        fontSize=20,
        leading=24,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#1B5E20'),
        spaceAfter=8,
    )

    section_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#1B5E20'),
        spaceBefore=8,
        spaceAfter=8,
    )

    cell_style = ParagraphStyle(
        'Cell',
        parent=styles['BodyText'],
        fontSize=7,
        leading=9,
    )

    header_style = ParagraphStyle(
        'HeaderCell',
        parent=cell_style,
        fontName='Helvetica-Bold',
        textColor=colors.white,
    )

    story = [
        Paragraph('WAHOME HERD', title_style),
        Paragraph(title, title_style),
        Paragraph(
            f'Generated on {date.today().strftime("%d %b %Y")}',
            ParagraphStyle(
                'GeneratedDate',
                parent=styles['Normal'],
                alignment=TA_CENTER,
                textColor=colors.HexColor('#68736C'),
                spaceAfter=14,
            )
        ),
    ]

    for index, section in enumerate(sections):
        story.append(
            Paragraph(
                section['title'],
                section_style
            )
        )

        table_data = [
            [
                Paragraph(str(header), header_style)
                for header in section['headers']
            ]
        ]

        for row in section['rows']:
            table_data.append([
                Paragraph(
                    str(value) if value not in (None, '') else '—',
                    cell_style
                )
                for value in row
            ])

        if len(table_data) == 1:
            table_data.append([
                Paragraph('No records available.', cell_style)
            ] + [
                ''
            ] * (len(section['headers']) - 1))

        table = Table(
            table_data,
            repeatRows=1,
            hAlign='LEFT',
        )

        table.setStyle(TableStyle([
            (
                'BACKGROUND',
                (0, 0),
                (-1, 0),
                colors.HexColor('#1B5E20')
            ),
            (
                'TEXTCOLOR',
                (0, 0),
                (-1, 0),
                colors.white
            ),
            (
                'GRID',
                (0, 0),
                (-1, -1),
                0.35,
                colors.HexColor('#D9E2DA')
            ),
            (
                'VALIGN',
                (0, 0),
                (-1, -1),
                'TOP'
            ),
            (
                'ROWBACKGROUNDS',
                (0, 1),
                (-1, -1),
                [colors.white, colors.HexColor('#F4F7F4')]
            ),
            (
                'LEFTPADDING',
                (0, 0),
                (-1, -1),
                4
            ),
            (
                'RIGHTPADDING',
                (0, 0),
                (-1, -1),
                4
            ),
            (
                'TOPPADDING',
                (0, 0),
                (-1, -1),
                4
            ),
            (
                'BOTTOMPADDING',
                (0, 0),
                (-1, -1),
                4
            ),
        ]))

        story.append(table)

        if index < len(sections) - 1:
            story.append(PageBreak())

    document.build(story)
    output.seek(0)

    response = HttpResponse(
        output.getvalue(),
        content_type='application/pdf'
    )
    response['Content-Disposition'] = (
        f'attachment; filename="{filename}.pdf"'
    )

    return response


@login_required(login_url='login')
@role_required(
    ADMINISTRATOR,
    FARM_MANAGER
)
def export_report(request):
    """
    Generate and download a farm report.

    Query parameters:
        type   = livestock / health / breeding / production /
                 financial / comprehensive
        format = pdf / excel / csv
    """

    report_type = request.GET.get(
        'type',
        'comprehensive'
    ).lower()

    export_format = request.GET.get(
        'format',
        'pdf'
    ).lower()

    allowed_types = {
        'livestock',
        'health',
        'breeding',
        'production',
        'financial',
        'comprehensive',
    }

    allowed_formats = {
        'pdf',
        'excel',
        'csv',
    }

    if report_type not in allowed_types:
        report_type = 'comprehensive'

    if export_format not in allowed_formats:
        export_format = 'pdf'

    sections = _report_export_data(
        report_type
    )

    title = _report_title(report_type)
    filename = (
        f'WAHOME_HERD_{report_type}_report_'
        f'{date.today().strftime("%Y%m%d")}'
    )

    if export_format == 'csv':
        return _export_csv(
            sections,
            filename
        )

    if export_format == 'excel':
        return _export_excel(
            sections,
            title,
            filename
        )

    return _export_pdf(
        sections,
        title,
        filename
    )


# ============================================================
# FINANCE DASHBOARD
# ============================================================

@login_required(login_url='login')
@role_required(
    ADMINISTRATOR,
    FARM_MANAGER
)
def finance_dashboard(request):

    total_income = FinancialRecord.objects.filter(
        record_type='INCOME'
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    total_expenses = FinancialRecord.objects.filter(
        record_type='EXPENSE'
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    net_profit = total_income - total_expenses

    income_count = FinancialRecord.objects.filter(
        record_type='INCOME'
    ).count()

    expense_count = FinancialRecord.objects.filter(
        record_type='EXPENSE'
    ).count()

    transaction_count = (
        income_count +
        expense_count
    )

    if total_income > 0:

        profit_margin = (
            float(net_profit) /
            float(total_income)
        ) * 100

    else:

        profit_margin = 0

    recent_transactions = FinancialRecord.objects.select_related(
        'animal'
    ).order_by(
        '-date',
        '-created_at'
    )[:15]

    expense_categories = []

    for category_code, category_name in FinancialRecord.CATEGORY_CHOICES:

        total = FinancialRecord.objects.filter(
            record_type='EXPENSE',
            category=category_code
        ).aggregate(
            total=Sum('amount')
        )['total'] or 0

        if total > 0:

            expense_categories.append({
                'name': category_name,
                'amount': total,
            })

    expense_categories.sort(
        key=lambda item: item['amount'],
        reverse=True
    )

    income_categories = []

    for category_code, category_name in FinancialRecord.CATEGORY_CHOICES:

        total = FinancialRecord.objects.filter(
            record_type='INCOME',
            category=category_code
        ).aggregate(
            total=Sum('amount')
        )['total'] or 0

        if total > 0:

            income_categories.append({
                'name': category_name,
                'amount': total,
            })

    income_categories.sort(
        key=lambda item: item['amount'],
        reverse=True
    )

    today = date.today()

    monthly_labels = []
    monthly_income = []
    monthly_expenses = []
    monthly_profit = []

    for month_offset in range(11, -1, -1):

        month_number = today.month - month_offset
        year = today.year

        while month_number <= 0:
            month_number += 12
            year -= 1

        month_start = date(
            year,
            month_number,
            1
        )

        if month_number == 12:

            next_month = date(
                year + 1,
                1,
                1
            )

        else:

            next_month = date(
                year,
                month_number + 1,
                1
            )

        income = FinancialRecord.objects.filter(
            record_type='INCOME',
            date__gte=month_start,
            date__lt=next_month
        ).aggregate(
            total=Sum('amount')
        )['total'] or 0

        expenses = FinancialRecord.objects.filter(
            record_type='EXPENSE',
            date__gte=month_start,
            date__lt=next_month
        ).aggregate(
            total=Sum('amount')
        )['total'] or 0

        profit = income - expenses

        monthly_labels.append(
            month_start.strftime('%b %Y')
        )

        monthly_income.append(
            float(income)
        )

        monthly_expenses.append(
            float(expenses)
        )

        monthly_profit.append(
            float(profit)
        )

    # ========================================================
    # ANIMAL FINANCIAL PERFORMANCE
    # ========================================================

    profitability_rows = list(
        FinancialRecord.objects.filter(
            animal__isnull=False
        ).values(
            'animal'
        ).annotate(
            total_income=Sum(
                'amount',
                filter=Q(record_type='INCOME')
            ),
            total_expenses=Sum(
                'amount',
                filter=Q(record_type='EXPENSE')
            ),
        )
    )

    animal_ids = {
        row['animal']
        for row in profitability_rows
        if row['animal']
    }

    animals = {
        animal.pk: animal
        for animal in Animal.objects.filter(
            pk__in=animal_ids
        )
    }

    animal_finances = []

    for row in profitability_rows:

        animal = animals.get(
            row['animal']
        )

        if not animal:
            continue

        income = row['total_income'] or 0
        expenses = row['total_expenses'] or 0
        profit = income - expenses

        animal_finances.append({
            'animal': animal,
            'income': income,
            'expenses': expenses,
            'profit': profit,
        })

    animal_finances.sort(
        key=lambda item: item['profit'],
        reverse=True
    )

    top_profitable_animals = animal_finances[:5]

    highest_expense_animals = sorted(
        animal_finances,
        key=lambda item: item['expenses'],
        reverse=True
    )[:5]

    highest_expense_category = (
        expense_categories[0]
        if expense_categories
        else None
    )

    highest_income_category = (
        income_categories[0]
        if income_categories
        else None
    )

    context = {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_profit': net_profit,

        'income_count': income_count,
        'expense_count': expense_count,
        'transaction_count': transaction_count,

        'profit_margin': profit_margin,

        'recent_transactions': recent_transactions,

        'expense_categories': expense_categories,
        'income_categories': income_categories,

        'monthly_labels': monthly_labels,
        'monthly_income': monthly_income,
        'monthly_expenses': monthly_expenses,
        'monthly_profit': monthly_profit,

        'top_profitable_animals': top_profitable_animals,
        'highest_expense_animals': highest_expense_animals,

        'highest_expense_category': highest_expense_category,
        'highest_income_category': highest_income_category,
    }

    return render(
        request,
        'livestock/finance_dashboard.html',
        context
    )


# ============================================================
# ADD FINANCIAL RECORD
# ============================================================

@login_required(login_url='login')
@role_required(
    ADMINISTRATOR,
    FARM_MANAGER
)
def add_financial_record(request):

    if request.method == 'POST':

        record_type = request.POST.get(
            'record_type'
        )

        category = request.POST.get(
            'category'
        )

        record_date = request.POST.get(
            'date'
        )

        amount = request.POST.get(
            'amount'
        )

        description = request.POST.get(
            'description'
        )

        animal_id = request.POST.get(
            'animal'
        )

        notes = request.POST.get(
            'notes'
        )

        animal = None

        if animal_id:

            animal = get_object_or_404(
                Animal,
                animal_id=animal_id
            )

        financial_record = FinancialRecord.objects.create(
            record_type=record_type,
            category=category,
            date=record_date,
            amount=amount,
            description=description,
            animal=animal,
            notes=notes,
        )

        log_activity(
            request.user,
            'CREATE',
            'Finance',
            f'Added {financial_record.get_record_type_display().lower()} financial record of {financial_record.amount}.'
        )

        return redirect(
            'finance_dashboard'
        )

    animals = Animal.objects.all().order_by(
        'animal_id'
    )

    return render(
        request,
        'livestock/add_financial_record.html',
        {
            'animals': animals,
        }
    )


# ============================================================
# FINANCIAL RECORDS
# ============================================================

@login_required(login_url='login')
@role_required(
    ADMINISTRATOR,
    FARM_MANAGER
)
def financial_records(request):

    records = FinancialRecord.objects.select_related(
        'animal'
    ).order_by(
        '-date',
        '-created_at'
    )

    record_type = request.GET.get(
        'record_type',
        ''
    )

    category = request.GET.get(
        'category',
        ''
    )

    if record_type:

        records = records.filter(
            record_type=record_type
        )

    if category:

        records = records.filter(
            category=category
        )

    return render(
        request,
        'livestock/financial_records.html',
        {
            'records': records,
            'selected_record_type': record_type,
            'selected_category': category,
        }
    )


# ============================================================
# FARM SETTINGS
# ============================================================

@login_required(login_url='login')
@role_required(
    ADMINISTRATOR
)
def farm_settings(request):

    settings = FarmSettings.objects.first()

    if not settings:

        settings = FarmSettings.objects.create(
            farm_name='WAHOME HERD'
        )

    if request.method == 'POST':

        settings.farm_name = request.POST.get(
            'farm_name',
            'WAHOME HERD'
        )

        settings.location = request.POST.get(
            'location',
            ''
        )

        settings.owner_name = request.POST.get(
            'owner_name',
            ''
        )

        settings.phone = request.POST.get(
            'phone',
            ''
        )

        settings.email = request.POST.get(
            'email',
            ''
        )

        settings.description = request.POST.get(
            'description',
            ''
        )

        settings.save()

        log_activity(
            request.user,
            'UPDATE',
            'Farm Settings',
            'Updated farm settings.'
        )

        return redirect(
            'farm_settings'
        )

    return render(
        request,
        'livestock/farm_settings.html',
        {
            'settings': settings,
        }
    )


# ============================================================
# USER MANAGEMENT
# ADMINISTRATOR ONLY
# ============================================================

@login_required(login_url='login')
@role_required(ADMINISTRATOR)
def user_management(request):

    users = User.objects.all().prefetch_related(
        'groups'
    ).order_by(
        'username'
    )

    user_data = []

    for user in users:

        role = get_user_role(user)

        if not role:
            role = 'No Role Assigned'

        user_data.append({
            'user': user,
            'role': role,
        })

    context = {
        'user_data': user_data,
        'total_users': users.count(),
        'active_users': users.filter(
            is_active=True
        ).count(),
        'inactive_users': users.filter(
            is_active=False
        ).count(),
    }

    return render(
        request,
        'livestock/user_management.html',
        context
    )


# ============================================================
# ADD USER
# ============================================================

@login_required(login_url='login')
@role_required(ADMINISTRATOR)
def add_user(request):

    if request.method == 'POST':

        form = UserCreationForm(
            request.POST
        )

        if form.is_valid():

            user = form.save()

            first_name = request.POST.get(
                'first_name',
                ''
            ).strip()

            last_name = request.POST.get(
                'last_name',
                ''
            ).strip()

            email = request.POST.get(
                'email',
                ''
            ).strip()

            role = request.POST.get(
                'role',
                FARM_WORKER
            )

            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.is_active = True

            user.save()

            user.groups.clear()

            valid_roles = [
                ADMINISTRATOR,
                FARM_MANAGER,
                FARM_WORKER,
            ]

            if role not in valid_roles:
                role = FARM_WORKER

            group, created = Group.objects.get_or_create(
                name=role
            )

            user.groups.add(group)

            log_activity(
                request.user,
                'CREATE',
                'User Management',
                f'Created user {user.username} with role {role}.'
            )

            return redirect(
                'user_management'
            )

    else:

        form = UserCreationForm()

    context = {
        'form': form,
        'roles': [
            ADMINISTRATOR,
            FARM_MANAGER,
            FARM_WORKER,
        ],
    }

    return render(
        request,
        'livestock/add_user.html',
        context
    )


# ============================================================
# EDIT USER
# ============================================================

@login_required(login_url='login')
@role_required(ADMINISTRATOR)
def edit_user(request, user_id):

    user = get_object_or_404(
        User,
        id=user_id
    )

    if request.method == 'POST':

        username = request.POST.get(
            'username',
            ''
        ).strip()

        first_name = request.POST.get(
            'first_name',
            ''
        ).strip()

        last_name = request.POST.get(
            'last_name',
            ''
        ).strip()

        email = request.POST.get(
            'email',
            ''
        ).strip()

        role = request.POST.get(
            'role',
            FARM_WORKER
        )

        if user == request.user:
            role = ADMINISTRATOR

        valid_roles = [
            ADMINISTRATOR,
            FARM_MANAGER,
            FARM_WORKER,
        ]

        if role not in valid_roles:
            role = FARM_WORKER

        username_exists = User.objects.filter(
            username=username
        ).exclude(
            id=user.id
        ).exists()

        if username_exists:

            context = {
                'user_account': user,
                'roles': valid_roles,
                'current_role': get_user_role(user),
                'error': (
                    'That username is already in use. '
                    'Please choose another username.'
                ),
            }

            return render(
                request,
                'livestock/edit_user.html',
                context
            )

        if not username:

            context = {
                'user_account': user,
                'roles': valid_roles,
                'current_role': get_user_role(user),
                'error': 'Username cannot be empty.',
            }

            return render(
                request,
                'livestock/edit_user.html',
                context
            )

        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email

        user.save()

        user.groups.clear()

        group, created = Group.objects.get_or_create(
            name=role
        )

        user.groups.add(group)

        log_activity(
            request.user,
            'UPDATE',
            'User Management',
            f'Updated user {user.username} and assigned role {role}.'
        )

        return redirect(
            'user_management'
        )

    context = {
        'user_account': user,
        'roles': [
            ADMINISTRATOR,
            FARM_MANAGER,
            FARM_WORKER,
        ],
        'current_role': get_user_role(user),
    }

    return render(
        request,
        'livestock/edit_user.html',
        context
    )


# ============================================================
# ACTIVATE / DEACTIVATE USER
# ============================================================

@login_required(login_url='login')
@role_required(ADMINISTRATOR)
def toggle_user_status(request, user_id):

    user = get_object_or_404(
        User,
        id=user_id
    )

    if user == request.user:
        return redirect(
            'user_management'
        )

    if request.method == 'POST':

        user.is_active = not user.is_active

        user.save(
            update_fields=[
                'is_active'
            ]
        )

        status = 'activated' if user.is_active else 'deactivated'

        log_activity(
            request.user,
            'UPDATE',
            'User Management',
            f'{status.capitalize()} user {user.username}.'
        )

    return redirect(
        'user_management'
    )


# ============================================================
# RESET USER PASSWORD
# ============================================================

@login_required(login_url='login')
@role_required(ADMINISTRATOR)
def reset_user_password(request, user_id):

    user = get_object_or_404(
        User,
        id=user_id
    )

    if request.method == 'POST':

        password = request.POST.get(
            'password',
            ''
        )

        password_confirmation = request.POST.get(
            'password_confirmation',
            ''
        )

        if password and password == password_confirmation:

            user.set_password(
                password
            )

            user.save()

            log_activity(
                request.user,
                'UPDATE',
                'User Management',
                f'Reset password for user {user.username}.'
            )

            return redirect(
                'user_management'
            )

        context = {
            'user_account': user,
            'error': (
                'The passwords do not match '
                'or the password is empty.'
            ),
        }

        return render(
            request,
            'livestock/reset_user_password.html',
            context
        )

    return render(
        request,
        'livestock/reset_user_password.html',
        {
            'user_account': user,
        }
    )


# ============================================================
# ACTIVITY / AUDIT LOG
# ADMINISTRATOR ONLY
# ============================================================

@login_required(login_url='login')
@role_required(ADMINISTRATOR)
def activity_log(request):

    logs = ActivityLog.objects.select_related(
        'user'
    ).order_by(
        '-created_at'
    )

    action = request.GET.get(
        'action',
        ''
    ).strip()

    module = request.GET.get(
        'module',
        ''
    ).strip()

    username = request.GET.get(
        'username',
        ''
    ).strip()

    if action:
        logs = logs.filter(
            action=action
        )

    if module:
        logs = logs.filter(
            module=module
        )

    if username:
        logs = logs.filter(
            user__username__icontains=username
        )

    context = {
        'logs': logs,
        'action_choices': ActivityLog.ACTION_CHOICES,
        'modules': (
            ActivityLog.objects
            .values_list(
                'module',
                flat=True
            )
            .distinct()
            .order_by('module')
        ),
        'selected_action': action,
        'selected_module': module,
        'selected_username': username,
        'total_logs': logs.count(),
    }

    return render(
        request,
        'livestock/activity_log.html',
        context
    )