from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from livestock.views import (
    dashboard,

    # Authentication
    login_view,
    profile,
    change_password,

    # Livestock
    livestock_list,
    add_animal,
    animal_detail,
    edit_animal,
    delete_animal,

    # Health
    health_records,
    add_health_record,
    edit_health_record,
    delete_health_record,

    # Breeding
    breeding_records,
    add_breeding_record,
    edit_breeding_record,
    delete_breeding_record,

    # Production
    production_records,
    add_production_record,
    edit_production_record,
    delete_production_record,

    # Farm-wide records
    all_health_records,
    all_breeding_records,
    all_production_records,

    # Reports
    reports,
    export_report,

    # Finance
    finance_dashboard,
    add_financial_record,
    financial_records,

    # Farm Settings
    farm_settings,

    # User Management
    user_management,
    add_user,
    edit_user,
    toggle_user_status,
    reset_user_password,

    # Activity / Audit Log
    activity_log,
)


urlpatterns = [

    path(
        'admin/',
        admin.site.urls
    ),

    # ========================================================
    # AUTHENTICATION
    # ========================================================

    path(
        'accounts/login/',
        login_view,
        name='login'
    ),

    path(
        'accounts/logout/',
        auth_views.LogoutView.as_view(
            next_page='/accounts/login/'
        ),
        name='logout'
    ),

    path(
        'accounts/password-change/',
        change_password,
        name='password_change'
    ),

    path(
        'accounts/password-change/done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='registration/password_change_done.html'
        ),
        name='password_change_done'
    ),

    path(
        'accounts/profile/',
        profile,
        name='profile'
    ),

    # ========================================================
    # FORGOT PASSWORD / PASSWORD RESET
    # ========================================================

    path(
        'accounts/password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset_form.html',
            email_template_name='registration/password_reset_email.html',
            subject_template_name='registration/password_reset_subject.txt',
        ),
        name='password_reset'
    ),

    path(
        'accounts/password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    path(
        'accounts/reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),

    path(
        'accounts/reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),

    # ========================================================
    # DASHBOARD
    # ========================================================

    path(
        '',
        dashboard,
        name='dashboard'
    ),

    # ========================================================
    # USER MANAGEMENT
    # ========================================================

    path(
        'users/',
        user_management,
        name='user_management'
    ),

    path(
        'users/add/',
        add_user,
        name='add_user'
    ),

    path(
        'users/<int:user_id>/edit/',
        edit_user,
        name='edit_user'
    ),

    path(
        'users/<int:user_id>/toggle-status/',
        toggle_user_status,
        name='toggle_user_status'
    ),

    path(
        'users/<int:user_id>/reset-password/',
        reset_user_password,
        name='reset_user_password'
    ),

    # ========================================================
    # ACTIVITY LOG
    # ========================================================

    path(
        'activity-log/',
        activity_log,
        name='activity_log'
    ),

    # ========================================================
    # FARM-WIDE RECORDS
    # ========================================================

    path(
        'health-records/',
        all_health_records,
        name='all_health_records'
    ),

    path(
        'breeding/',
        all_breeding_records,
        name='all_breeding_records'
    ),

    path(
        'production/',
        all_production_records,
        name='all_production_records'
    ),

    # ========================================================
    # REPORTS
    # ========================================================

    path(
        'reports/',
        reports,
        name='reports'
    ),

    path(
        'reports/export/',
        export_report,
        name='export_report'
    ),

    # ========================================================
    # FINANCE
    # ========================================================

    path(
        'finance/',
        finance_dashboard,
        name='finance_dashboard'
    ),

    path(
        'finance/add/',
        add_financial_record,
        name='add_financial_record'
    ),

    path(
        'finance/transactions/',
        financial_records,
        name='financial_records'
    ),

    # ========================================================
    # FARM SETTINGS
    # ========================================================

    path(
        'settings/',
        farm_settings,
        name='farm_settings'
    ),

    # ========================================================
    # LIVESTOCK
    # ========================================================

    path(
        'livestock/',
        livestock_list,
        name='livestock_list'
    ),

    path(
        'livestock/add/',
        add_animal,
        name='add_animal'
    ),

    path(
        'livestock/<str:animal_id>/',
        animal_detail,
        name='animal_detail'
    ),

    path(
        'livestock/<str:animal_id>/edit/',
        edit_animal,
        name='edit_animal'
    ),

    path(
        'livestock/<str:animal_id>/delete/',
        delete_animal,
        name='delete_animal'
    ),

    # ========================================================
    # HEALTH
    # ========================================================

    path(
        'livestock/<str:animal_id>/health/',
        health_records,
        name='health_records'
    ),

    path(
        'livestock/<str:animal_id>/health/add/',
        add_health_record,
        name='add_health_record'
    ),

    path(
        'health-record/<int:record_id>/edit/',
        edit_health_record,
        name='edit_health_record'
    ),

    path(
        'health-record/<int:record_id>/delete/',
        delete_health_record,
        name='delete_health_record'
    ),

    # ========================================================
    # BREEDING
    # ========================================================

    path(
        'livestock/<str:animal_id>/breeding/',
        breeding_records,
        name='breeding_records'
    ),

    path(
        'livestock/<str:animal_id>/breeding/add/',
        add_breeding_record,
        name='add_breeding_record'
    ),

    path(
        'breeding-record/<int:record_id>/edit/',
        edit_breeding_record,
        name='edit_breeding_record'
    ),

    path(
        'breeding-record/<int:record_id>/delete/',
        delete_breeding_record,
        name='delete_breeding_record'
    ),

    # ========================================================
    # PRODUCTION
    # ========================================================

    path(
        'livestock/<str:animal_id>/production/',
        production_records,
        name='production_records'
    ),

    path(
        'livestock/<str:animal_id>/production/add/',
        add_production_record,
        name='add_production_record'
    ),

    path(
        'production-record/<int:record_id>/edit/',
        edit_production_record,
        name='edit_production_record'
    ),

    path(
        'production-record/<int:record_id>/delete/',
        delete_production_record,
        name='delete_production_record'
    ),
]