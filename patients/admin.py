from django.contrib import admin
from .models import Patient,Appointment,Service,SubService
from unfold.admin import ModelAdmin
@admin.register(Patient)
class adminDoctor(ModelAdmin):
    pass


# Python
@admin.register(Appointment)
class AppointmentAdmin(ModelAdmin):
    """
    Custom admin configuration for the Appointment model.
    """
    # --- List Display Configuration ---
    list_display = ('patient', 'doctor', 'appointment_date','appointment_time', 'status', 'service')  # Corrected field name

    # --- Filtering and Searching ---
    list_filter = ('status', 'doctor', 'appointment_date','appointment_time', 'service')  # Corrected field name
    search_fields = ('patient__patient_name', 'doctor__doctor_name')

    # --- Form Field Configuration ---
    fieldsets = (
        ('Appointment Details', {
            'fields': ('patient', 'doctor', 'appointment_date','appointment_time')
        }),
        ('Service Information', {
            'fields': ('service', 'sub_service')  # Corrected field name
        }),
        ('Appointment Status', {
            'fields': ('status',)
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('patient', 'doctor', 'appointment_date', 'service', 'sub_service')  # Corrected field name
        else:
            return ()

@admin.register(Service)
class adminDoctorService(ModelAdmin):
    list_display = ['name', 'price']
    search_fields = ['name', 'price']
    list_filter = ['name']

@admin.register(SubService)
class adminDoctorSubService(ModelAdmin):
    list_display = ['service','SubService','price']
    list_filter = ["service"]
    search_fields = ['service__name', 'SubService', 'price']

