from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from app.models import Student, Service, ServiceInstance, Schedule
from django.contrib.auth.models import User

class CreateServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = '__all__'

class CreateScheduleForm(ModelForm):
    start_date = forms.DateField(widget=forms.SelectDateWidget)
    end_date = forms.DateField(widget=forms.SelectDateWidget)
    class Meta:
        model = Schedule
        fields = '__all__'
        widgets = {'teacher': forms.HiddenInput()}

class CreateServiceInstanceForm(ModelForm):
    class Meta:
        model = ServiceInstance
        fields = '__all__'
        widgets = {'scheduled_for': forms.HiddenInput(),
                   'time_start': forms.TimeInput(format="%H:%M"),
                   'time_end': forms.TimeInput(format="%H:%M")}

class CreateStudentForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        widgets = {'teacher': forms.HiddenInput()}
