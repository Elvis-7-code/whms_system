from django.contrib import admin
from .models import Animal


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = (
        'animal_id',
        'species',
        'breed',
        'sex',
        'weight',
        'status',
    )

    list_filter = (
        'species',
        'sex',
        'status',
    )

    search_fields = (
        'animal_id',
        'breed',
    )
