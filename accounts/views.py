from django.core.mail import send_mail
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from .filters import *

from django.contrib import messages

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .decorators import unauthenticated_user, allowed_users, admin_only
from  django.contrib.auth.models import Group


# Create your views here.
#
@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            group = form.cleaned_data.get('group')
            if group == 'patient':
                group = Group.objects.get(name='patient')
                user.groups.add(group)
                Patient.objects.create(
                    user=user
                )
            if group == 'doctor':
                group = Group.objects.get(name='doctor')
                user.groups.add(group)
                Doctor.objects.create(
                    user=user
                )
            return redirect('login')
    context = {'form': form}
    return render(request, 'accounts/register_login/register.html', context)


@unauthenticated_user
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password invalid !!')

    context = {}
    return render(request, 'accounts/register_login/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


# 1 for table ma data dekhuna

@login_required(login_url='login')
@admin_only
def home(request):
    patient = Patient.objects.all()
    doctor = Doctor.objects.all()
    appointment = Appointment.objects.all()

    total_patient = patient.count()
    total_doctor = doctor.count()
    total_appointments = appointment.count()
    appointment_pending = appointment.filter(status="pending").count()

    context = {'patient': patient, 'doctor': doctor, 'appointment': appointment
        , 'total_patient': total_patient, 'total_doctor': total_doctor, 'total_appointments': total_appointments}
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['patient', 'doctor'])
def userPage(request):
    group = None
    group = request.user.groups.all()[0].name

    if group == 'patient':
        patients = request.user.patient
        appointments = patients.appointment_set.all()
        context = {'appointments': appointments, 'patients':patients}

        return render(request, 'accounts/create_patient/user.html', context)

    if group == 'doctor':
        appointments = request.user.doctor.appointment_set.all()
        total_appointment = appointments.count()
        context = {'total_appointment': total_appointment, 'appointments': appointments}

        return render(request, 'accounts/update_doctor/user.html', context)

    #
    # appointment = request.user.patient.appointment_set()
    #
    # total_appointment = appointment.count()
    # appointmentDelivered = appointment.filter(status='Delivered').count()
    # appointmentPending = appointment.filter(status='Pending').count()
    #
    # context = {'appointment': appointment, 'total_appointment': total_appointment, 'appointmentDelivered': appointmentDelivered, 'appointmentPending': appointmentPending}
    # return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def patient(request):
    patient = Patient.objects.all()
    total_patient = patient.count()

    myFilter = PatientFilter(request.GET, queryset=patient)
    patient = myFilter.qs

    context = {'patient': patient, 'total_patient': total_patient, 'myFilter': myFilter}
    return render(request, 'accounts/patient.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def doctor(request):
    doctor = Doctor.objects.all()
    appointment = Appointment.objects.all()
    total_appointment = appointment.count()

    myFilter = DoctorFilter(request.GET, queryset=doctor)
    doctor = myFilter.qs

    approve_appointment = appointment.filter(status="approved").count()

    context = {'doctor': doctor, 'appointment': appointment, 'total_appointment': total_appointment,
               'approve_appointment': approve_appointment, 'myFilter': myFilter}
    return render(request, 'accounts/doctor.html', context)


def about(request):
    context = {}
    return render(request, 'accounts/about.html', context)


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        sub = f'Message from {name}[{email}]'
        from_email = 'zaarabuyghimire@gmail.com'
        to = ['zaarabuyghimire@gmail.com']
        message = message

        send_mail(subject=sub, message=message, from_email=from_email, recipient_list=to, fail_silently=True)
        return redirect('home')
    return render(request, 'accounts/contact.html')


@login_required(login_url='login')
def updatePatient(request, pk):
    patient = Patient.objects.get(id=pk)
    form = updateForm(instance=patient)
    if request.method == "POST":
        form = updateForm(request.POST, instance=patient)
        form.is_valid()
        form.save()
        return redirect('patient')
    context = {'form': form}
    return render(request, 'accounts/create_patient/update_patient.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateDoctor(request, pk):
    doctor = Doctor.objects.get(id=pk)
    form = createDoctor(instance=doctor)
    if request.method == 'POST':
        form = createDoctor(request.POST, instance=doctor)
        form.is_valid()
        form.save()
        return redirect('doctor')
    context = {'form': form}
    return render(request, 'accounts/update_doctor/createDoctor.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['patient', 'admin'])
def createPatient(request):
    form = PatientForm()
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient')
    context = {'form': form}
    return render(request, 'accounts/create_patient/create_patient.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def viewPatient(request, pk):
    patient = Patient.objects.get(id=pk)
    appointment = patient.appointment_set.all()
    context = {'patient': patient, 'appointment': appointment}
    return render(request, 'accounts/create_patient/patient_view.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def viewDoctor(request, pk):
    doctor = Doctor.objects.get(id=pk)
    context = {'doctor': doctor}
    return render(request, 'accounts/update_doctor/doctor_view.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['patient'])
def accountSettings(request):
    patient = request.user.patient
    form = PatientForm(instance=patient)
    if request.method == "POST":
        form = PatientForm(request.POST, request.FILES, instance=patient)
        form.is_valid()
        form.save()

    content = {'form': form}
    return render(request, 'accounts/create_patient/account_settings.html', content)


@login_required(login_url='login')
@allowed_users(allowed_roles=['doctor'])
def doctorSettings(request):
    doctor = request.user.doctor
    form = DoctorForm(instance=doctor)
    if request.method == "POST":
        form = DoctorForm(request.POST, request.FILES, instance=doctor)
        form.is_valid()
        form.save()

    content = {'form': form}
    return render(request, 'accounts/update_doctor/doctor_settings.html', content)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_patient(request, pk):
    patient = Patient.objects.get(id=pk)
    if request.method == "POST":
        patient.delete()
        return redirect('patient')
    context = {'patient': patient}
    return render(request, 'accounts/delete_forms/delete_patient.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_doctor(request, pk):
    doctor = Doctor.objects.get(id=pk)
    if request.method == "POST":
        doctor.delete()
        return redirect('doctor')
    context = {'doctor': doctor}
    return render(request, 'accounts/delete_forms/delete_doctor.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def appoint(request, pk):
    Appointments = inlineformset_factory(Patient, Appointment, fields=('appointDate', 'doctor'), extra=1)
    patient = Patient.objects.get(id=pk)
    formset = Appointments(queryset=Appointment.objects.none(), instance=patient)

    if request.method == 'POST':
        formset = Appointments(request.POST, instance=patient)
        formset.is_valid()
        formset.save()
        return redirect('patient')
    context = {'formset': formset}
    return render(request, 'accounts/appointments.html', context)