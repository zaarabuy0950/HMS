from django.forms import ModelForm
from .models import *

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class createPatient(ModelForm):  # update patient  ko form
    class Meta:
        model = Patient
        fields = '__all__'


class createDoctor(ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'


class updateForm(ModelForm):  # update patient  ko form
    class Meta:
        model = Patient
        fields = '__all__'


class PatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'


class DoctorForm(ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'


class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'


select = (
    ('doctor', 'doctor'),
    ('patient', 'patient')
)


class CreateUserForm(UserCreationForm):
    group = forms.ChoiceField(choices=select, required=True, widget=forms.Select)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'group']
