from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import clinicadmin,CustomLoginView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('appointment/', views.appointment, name='appointment'),
    path('appointment-form/', views.appointment_form, name='appointment_form'),
    path('profile/', views.profile, name='profile'),
    path('',views.home,name="home"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('get-sub-services/', views.get_sub_services, name='get_sub_services'),
    path('clinic-admin/',clinicadmin.as_view(),name = 'clinic_admin'),
    path('appointments/<str:status>/', views.appointment_status_view, name='appointment_status'),
    path('appointments/<int:appointment_id>/update/', views.update_appointment_status, name='update_appointment_status'),
    path("summarize/", views.summarize_report, name="summarize_report"),
    path("ai/", views.ai_page, name="ai_page"),
    path('account/login/', CustomLoginView.as_view(), name='login'),
]