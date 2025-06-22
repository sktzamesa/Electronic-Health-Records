from django import forms
from django.core.exceptions import ValidationError
from patients.models import Appointment, Service, SubService
from doctor.models import Doctor
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User



class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_date', 'appointment_time', 'service', 'sub_service']
        widgets = {
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'service': forms.Select(attrs={'class': 'form-control'}),
            'sub_service': forms.Select(attrs={'class': 'form-control'}),
            'appointment_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'id': 'appointment-date'
                }
            ),
            'appointment_time': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'appointment-time',
            }),
        }

    # dito need dapat ma-align ung date and time sa flatpickr
    # base sa kung ano ung nasa javascript na flatpickr
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['appointment_time'].input_formats = ['%I:%M %p']  # Matches Flatpickr's "h:i K" format

        # Add price display for service field
        self.fields['service'].label_from_instance = lambda obj: f"{obj.name} (₱{obj.price})"

        # Add price display for sub_service field
        self.fields['sub_service'].label_from_instance = lambda obj: f"{obj.SubService} (₱{obj.price})"

    def clean_appointment_time(self):
        appointment_time = self.cleaned_data.get('appointment_time')
        if appointment_time and appointment_time.minute != 0:
            raise ValidationError("Appointment time must be on the hour (e.g., 10:00, 11:00).")
        return appointment_time

class RegisterForm(forms.Form):

    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'id': 'register-name',
            'placeholder': 'Enter your full name',
            'autocomplete': 'name',
            'class': 'form-group'
        })
    )
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'id': 'register-username',
            'placeholder': 'Enter your username',
            'autocomplete': 'username',
            'class': 'form-group'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'id': 'register-email',
            'placeholder': 'Enter your email',
            'autocomplete': 'username',
            'class': 'form-group'
        })
    )
    age = forms.IntegerField(
        required=True,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'id': 'register-age',
            'placeholder': 'Enter your age',
            'class': 'form-group'
        })
    )
    contact = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'id': 'register-contact',
            'placeholder': 'Enter your contact number',
            'class': 'form-group'
        })
    )
    birthday = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={
            'id': 'register-birthday',
            'placeholder': 'YYYY-MM-DD',
            'type': 'date',
            'class': 'form-group'
        })
    )
    gender = forms.ChoiceField(
        required=True,
        choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
        widget=forms.Select(attrs={
            'id': 'register-gender',
            'class': 'form-control'
        })
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'id': 'register-password',
            'placeholder': 'Create a password',
            'autocomplete': 'new-password',
            'class': 'form-group'
        })
    )
    confirm_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'id': 'register-confirm-password',
            'placeholder': 'Confirm your password',
            'autocomplete': 'new-password',
            'class': 'form-group'
        })

    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match.')

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password and len(password) < 7:
            raise ValidationError('Password must be at least 7 characters long.')
        return password

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use.")
        return email