from django.shortcuts import render,redirect,get_object_or_404
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.http import JsonResponse
from django.contrib import messages
from patients.models import Appointment, Service, SubService, Patient
from doctor.models import Doctor
from datetime import datetime
from .forms import AppointmentForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User

class CustomLoginView(LoginView):
    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        if user.is_staff or user.is_superuser:
            return redirect('/admin/')
        return redirect('dashboard')

# Create your views here.
def homepage(request):
    return render(
        request,
        'home.html'
    )

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Extract form data
            name = form.cleaned_data['name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            age = form.cleaned_data['age']
            contact = form.cleaned_data['contact']
            birthday = form.cleaned_data['birthday']
            gender = form.cleaned_data['gender']

            # Create user
            user = User.objects.create(
                username=username,
                email=email,
                password=make_password(password),
                first_name=name  # or split and use first_name, last_name
            )

            # Create profile linked to the user
            Profile.objects.create(
                user=user,
                phone=contact,
                gender=gender,
                age=age,
                date_of_birth=birthday,
                status_profile='patient'  # or change if you allow selecting status
            )

            return redirect('login')  # or wherever you want to redirect
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

@login_required
def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'patient_dashboard.html')
    else:
        return redirect('login')

@login_required
def dashboard(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    doctors = Doctor.objects.all()  # Get all doctors

    return render(request, 'patient_dashboard.html',
                  {
                      'username': request.user.username
                        ,'Profile': profile
                        ,'doctors': doctors
                  })

@login_required
def appointment(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    appointments = Appointment.objects.filter(profile=profile)

    for appointment in appointments:
        appointment.total_price = 0
        if appointment.service:
            appointment.total_price += appointment.service.price
        if appointment.sub_service:
            appointment.total_price += appointment.sub_service.price


    return render(request, 'appointment/appointment_records.html', {
        'username': request.user.username,
        'Profile': profile,
        'appointments': appointments,
    })


@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Handle profile picture update if 'avatarInput' is present in FILES
        if request.FILES.get('avatarInput'):
            profile.image = request.FILES['avatarInput']
            profile.save()
            messages.success(request, 'Profile picture updated successfully!')

        return render(
            request,
            'patient_profile.html',
            {
                'username': request.user.username,
                'Profile': profile, # Ensure this 'Profile' object reflects the latest changes
            }
        )
    else: # This block handles GET requests
        return render(
            request,
            'patient_profile.html',
            {
                'username': request.user.username,
                'Profile': profile,
            }
        )


# Python
@login_required
def appointment_form(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    patient, created = Patient.objects.get_or_create(profile=profile)  # Ensure patient exists

    # Get doctor_id from the URL query parameters
    doctor_id = request.GET.get('doctor_id')
    doctor = None
    if doctor_id:
        doctor = get_object_or_404(Doctor, id=doctor_id)  # Retrieve the doctor instance

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.profile = profile
            appointment.patient = patient  # Assign the patient here
            appointment.doctor = doctor  # Automatically set the doctor
            appointment.save()
            messages.success(request, 'Appointment booked successfully!')
            return redirect('appointment')
    else:
        # Pre-fill the doctor field in the form
        form = AppointmentForm(initial={'doctor': doctor})

    return render(request, 'appointment/appointment_form.html', {
        'form': form,
        'Profile': profile,
        'username': request.user.username,
    })


def get_appointment_details(request):
    appointment_id = request.GET.get('appointment_id')
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        data = {
            'date': appointment.appointment_date.strftime('%Y-%m-%d'),
            'time': appointment.appointment_date.strftime('%H:%M'),
            'doctor': str(appointment.doctor),
            'service': str(appointment.service.name) if appointment.service else 'N/A',
            'service_price': appointment.service.price if appointment.service else 0,
            'sub_service': str(appointment.sub_service.SubService) if appointment.sub_service else 'N/A',
            'sub_service_price': appointment.sub_service.price if appointment.sub_service else 0,
        }
        return JsonResponse(data)
    except Appointment.DoesNotExist:
        return JsonResponse({'error': 'Appointment not found'}, status=404)
    

@login_required
def available_slots(request):
    date = request.GET.get('date')
    # Your logic to get available slots for the date
    # Example response:
    slots = [
        {
            'doctor_id': 1,
            'doctor_name': 'Dr. Smith',
            'time': '10:00',
            'datetime': f'{date}T10:00'
        },
        # ... more slots ...
    ]
    return JsonResponse({'slots': slots})

def get_sub_services(request):
    service_id = request.GET.get('service_id')
    sub_services = SubService.objects.filter(service_id=service_id).values('id', 'SubService')
    return JsonResponse(list(sub_services), safe=False)