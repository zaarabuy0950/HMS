import django_filters
from .models import *
from django_filters import DateFilter, CharFilter


class PatientFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="admitDate", lookup_expr='gte')
    end_date = DateFilter(field_name="admitDate", lookup_expr='lte')

    class Meta:
        model = Patient
        fields = '__all__'
        exclude = ['assignedDoctor', 'age', 'address', 'bloodGroup', 'mobile', 'symptoms', 'admitDate', 'profile_pic']


class DoctorFilter(django_filters.FilterSet):
    class Meta:
        model = Doctor
        fields = '__all__'
        exclude = ['address', 'status', 'email', 'mobile', 'profile_pic']


class AppointmentFilter(django_filters.FilterSet):
    class Meta:
        model = Appointment
        fields = '__all__'
