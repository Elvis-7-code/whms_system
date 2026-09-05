from django.db import models


class Animal(models.Model):

    SPECIES_CHOICES = [
        ('COW', 'Cow'),
        ('GOAT', 'Goat'),
        ('SHEEP', 'Sheep'),
    ]

    SEX_CHOICES = [
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
    ]

    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('SOLD', 'Sold'),
        ('DECEASED', 'Deceased'),
    ]

    animal_id = models.CharField(max_length=20, unique=True)

    species = models.CharField(
        max_length=10,
        choices=SPECIES_CHOICES
    )

    breed = models.CharField(
        max_length=100,
        blank=True
    )

    sex = models.CharField(
        max_length=10,
        choices=SEX_CHOICES
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True
    )

    colour = models.CharField(
        max_length=100,
        blank=True
    )

    weight = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True
    )

    date_acquired = models.DateField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='ACTIVE'
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.animal_id


class HealthRecord(models.Model):

    RECORD_TYPE_CHOICES = [
        ('VACCINATION', 'Vaccination'),
        ('TREATMENT', 'Treatment'),
        ('ILLNESS', 'Illness'),
        ('VET_VISIT', 'Veterinary Visit'),
        ('OTHER', 'Other'),
    ]

    animal = models.ForeignKey(
        Animal,
        on_delete=models.CASCADE,
        related_name='health_records'
    )

    record_type = models.CharField(
        max_length=20,
        choices=RECORD_TYPE_CHOICES
    )

    date = models.DateField()

    next_due_date = models.DateField(
        null=True,
        blank=True
    )

    description = models.TextField()

    medication = models.CharField(
        max_length=200,
        blank=True
    )

    veterinarian = models.CharField(
        max_length=200,
        blank=True
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.animal.animal_id} - "
            f"{self.record_type} - "
            f"{self.date}"
        )


class BreedingRecord(models.Model):

    STATUS_CHOICES = [
        ('PLANNED', 'Planned'),
        ('PREGNANT', 'Pregnant'),
        ('SUCCESSFUL', 'Successful'),
        ('FAILED', 'Failed'),
        ('BORN', 'Birth Recorded'),
    ]

    female = models.ForeignKey(
        Animal,
        on_delete=models.CASCADE,
        related_name='breeding_records_as_female'
    )

    male = models.ForeignKey(
        Animal,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='breeding_records_as_male'
    )

    breeding_date = models.DateField()

    expected_birth_date = models.DateField(
        null=True,
        blank=True
    )

    actual_birth_date = models.DateField(
        null=True,
        blank=True
    )

    offspring_count = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=12,
        choices=STATUS_CHOICES,
        default='PLANNED'
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.female.animal_id} - "
            f"{self.breeding_date}"
        )


class ProductionRecord(models.Model):

    PRODUCTION_TYPE_CHOICES = [
        ('MILK', 'Milk'),
        ('WEIGHT', 'Weight'),
        ('MEAT', 'Meat'),
        ('OTHER', 'Other'),
    ]

    animal = models.ForeignKey(
        Animal,
        on_delete=models.CASCADE,
        related_name='production_records'
    )

    production_type = models.CharField(
        max_length=20,
        choices=PRODUCTION_TYPE_CHOICES
    )

    date = models.DateField()

    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    unit = models.CharField(
        max_length=30
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.animal.animal_id} - "
            f"{self.production_type} - "
            f"{self.date}"
        )


# =========================
# FINANCIAL RECORDS
# =========================

class FinancialRecord(models.Model):

    RECORD_TYPE_CHOICES = [
        ('INCOME', 'Income'),
        ('EXPENSE', 'Expense'),
    ]

    CATEGORY_CHOICES = [
        ('ANIMAL_SALE', 'Animal Sale'),
        ('MILK_SALE', 'Milk Sale'),
        ('MEAT_SALE', 'Meat Sale'),
        ('OTHER_INCOME', 'Other Income'),

        ('FEED', 'Feed'),
        ('MEDICINE', 'Medicine'),
        ('VETERINARY', 'Veterinary'),
        ('LABOUR', 'Labour'),
        ('EQUIPMENT', 'Equipment'),
        ('TRANSPORT', 'Transport'),
        ('OTHER_EXPENSE', 'Other Expense'),
    ]

    record_type = models.CharField(
        max_length=10,
        choices=RECORD_TYPE_CHOICES
    )

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES
    )

    date = models.DateField()

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    description = models.TextField(
        blank=True
    )

    animal = models.ForeignKey(
        Animal,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='financial_records'
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.record_type} - "
            f"{self.category} - "
            f"{self.amount}"
        )


# =========================
# FARM SETTINGS
# =========================

class FarmSettings(models.Model):

    farm_name = models.CharField(
        max_length=200,
        default='WAHOME HERD'
    )

    location = models.CharField(
        max_length=200,
        blank=True
    )

    owner_name = models.CharField(
        max_length=200,
        blank=True
    )

    phone = models.CharField(
        max_length=30,
        blank=True
    )

    email = models.EmailField(
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.farm_name


# =========================
# ACTIVITY / AUDIT LOG
# =========================

class ActivityLog(models.Model):

    ACTION_CHOICES = [
        ('CREATE', 'Created'),
        ('UPDATE', 'Updated'),
        ('DELETE', 'Deleted'),
        ('LOGIN', 'Logged In'),
        ('LOGOUT', 'Logged Out'),
        ('OTHER', 'Other'),
    ]

    user = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='activity_logs'
    )

    action = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES
    )

    module = models.CharField(
        max_length=100
    )

    description = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        username = self.user.username if self.user else 'System'

        return (
            f"{username} - "
            f"{self.action} - "
            f"{self.module}"
        )