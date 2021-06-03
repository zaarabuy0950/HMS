from django.urls import path
from .import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('', views.home, name='home'),
    path('user/', views.userPage, name="user_page"),

    path('patient/', views.patient, name='patient'),
    path('doctor/', views.doctor, name='doctor'),

    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('appoint/<str:pk>/', views.appoint, name='appoint'),

    path('updatePatient/<str:pk>/', views.updatePatient, name='updatePatient'),
    path('updateDoctor/<str:pk>/', views.updateDoctor, name='updateDoctor'),

    path('create_patient/', views.createPatient, name='create_patient'),
    path('view_patient/<str:pk>/', views.viewPatient, name='view_patient'),
    path('view_doctor/<str:pk>/', views.viewDoctor, name='view_doctor'),

    path('patient_settings/', views.accountSettings, name='patient_settings'),
    path('doctor_settings/', views.doctorSettings, name='doctor_settings'),

    path('deletePatient/<str:pk>/', views.delete_patient, name="deletePatient"),
    path('deletedoctor/<str:pk>/', views.delete_doctor, name="deletedoctor"),

    path('reset_password/',
         auth_views.PasswordResetView.as_view(),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(),
         name="password_reset_complete"),
]
