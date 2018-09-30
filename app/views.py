from django.shortcuts import render
from app.models import Student, Service, ServiceInstance, Schedule
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Following 2 implement requirements for user to
# be logged in or have the right permissions
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404  # finds a specific object using the primary key, or returns 404 if not found
from django.urls import reverse_lazy # reverses the url for redirection

from app.forms import CreateServiceForm, CreateScheduleForm, CreateServiceInstanceForm, CreateStudentForm  # custom forms

# Following 2 imports are for redirecting after form submission
from django.http import HttpResponseRedirect
from django.urls import reverse

import datetime # for creating time objects in the schedule detail view
import pprint # for debugging

# Create your views here.

def index(request):
    """View function for home page of site"""

    # Generate counts of students
    num_students = Student.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    
    context = {
        'num_students' : num_students,
        'num_visits' : num_visits
        }

    return render(request, 'index.html', context=context)


class StudentDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = '/accounts/login/' # the url to which the user is redirected if not logged in
    model = Student                # the model that the view will display, if get_queryset method is not overriden, then
                                   # the default method will return all Student objects
                                   
class StudentListView(LoginRequiredMixin, generic.ListView):
    login_url = '/accounts/login/'
    model = Student

    def get_queryset(self):
        return Student.objects.filter(teacher=self.request.user)

class ScheduleListView(LoginRequiredMixin, generic.ListView):
    login_url = '/accounts/login/'
    model = Schedule

    def get_queryset(self):
        return Schedule.objects.filter(teacher=self.request.user)

@login_required
def ScheduleDetailView(request, pk):
    """View function for displaying a Schedule model"""
    schedule = get_object_or_404(Schedule, pk=pk)
    students = Student.objects.all()
    html = ""

    def get_time_slot():
        # Returns a time_slot dict
        time_slot = {
            (datetime.time(hour=7), "AM"): [],
            (datetime.time(hour=8), "AM"): [],
            (datetime.time(hour=9), "AM"): [],
            (datetime.time(hour=10), "AM"): [],
            (datetime.time(hour=11), "AM"): [],
            (datetime.time(hour=12), "PM"): [],
            (datetime.time(hour=1), "PM"): [],
            (datetime.time(hour=2), "PM"): [],
            (datetime.time(hour=3), "PM"): [],
        }
        return time_slot
    
    # Construct a dict of dicts to map all of the service appointments to their days and time slots
    # For example, a Monday service at 10AM would go to the Monday dict, and then into the 10AM dict
    # I use a datetime object because it's easier to reference the hours, minutes, etc.

    appts = {
        "Monday": get_time_slot(),
        "Tuesday": get_time_slot(),
        "Wednesday": get_time_slot(),
        "Thursday": get_time_slot(),
        "Friday": get_time_slot(),
        }

    # Goes through every service instance and maps it into the appts dict
    # with the appropriate service day and time
    for serviceinstance in schedule.sched_serviceinstances.all():   # using the related_name of the model to backtrace its one-to-many relationship
        for day_slot in appts.keys():
            if day_slot == serviceinstance.day:
                for time_slot in appts[day_slot].keys():
                    if serviceinstance.time_start and serviceinstance.time_start.hour == time_slot[0].hour:  # make sure the service instance has a time_start field to begin with,
                        appts[day_slot][time_slot].append(serviceinstance)                                   # then check if the service instance start hour can be mapped to a time slot,
                                                                                                             # if so, add the service to that day, and to the correct time slot!
    #pprint.pprint(appts)  
    context = {
        "schedule": schedule,
        "student_list": students,
        "appts": appts,
        }
    return render(request, "app/schedule_detail.html", context)

class ServiceListView(LoginRequiredMixin, generic.ListView):
    login_url = '/accounts/login/'
    model = Service

    def get_queryset(self):
        return Service.objects.filter(student__teacher=self.request.user)   # double underscore allows us to find objects that span several relationships

class ServiceDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = '/accounts/login/'
    model = Service

class ServiceInstanceDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = '/accounts/login/'
    model = ServiceInstance

@login_required
def StudentCreate(request):
    # If the request is a POST, check if the fields are valid and the inputs, clean.
    # Save if valid.
    # If the request is not a POST, but a GET, add the initial teacher value
    if request.method == 'POST':
        student_create_form = CreateStudentForm(request.POST)

        if student_create_form.is_valid():
            new_student = Student(**student_create_form.cleaned_data)
            new_student.save()
            return HttpResponseRedirect(reverse('student-list'))    # redirects user to the student list page
    else:
        student_create_form = CreateStudentForm(initial={'teacher': request.user})
    
    context = {
        'form': student_create_form,
        }
    
    return render(request, 'app/student_form.html', context)

class StudentUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/accounts/login/'
    model = Student
    fields = '__all__'

class StudentDelete(LoginRequiredMixin, DeleteView):
    login_url = '/accounts/login/'
    model = Student
    success_url = reverse_lazy('student-list')

@login_required
def ServiceCreate(request, pk):
    # Find the student for initial student field
    student = get_object_or_404(Student, pk=pk)

    # If the request is a POST, check if the fields are valid and the inputs, clean.
    # Save if valid.
    # If the request is not a POST, but a GET, add the initial student value
    if request.method == 'POST':
        service_create_form = CreateServiceForm(request.POST)

        if service_create_form.is_valid():
            new_service = Service(**service_create_form.cleaned_data)
            new_service.save()
            return HttpResponseRedirect(reverse('student-list'))    # redirects user to the student list page
    else:
        chosen_student = student
        service_create_form = CreateServiceForm(initial={'student': student})
    
    context = {
        'form': service_create_form,
        }
    
    return render(request, 'app/service_form.html', context)

class ServiceUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/accounts/login/'
    model = Service
    fields = '__all__'

class ServiceDelete(LoginRequiredMixin, DeleteView):
    login_url = '/accounts/login/'
    model = Service
    success_url = reverse_lazy('student-list')

@login_required
def ScheduleCreate(request):
    # If the request is a POST, check if the fields are valid and the inputs, clean.
    # Save if valid.
    # If the request is not a POST, but a GET, add the initial teacher value
    if request.method == 'POST':
        schedule_create_form = CreateScheduleForm(request.POST, initial={'teacher': request.user})

        if schedule_create_form.is_valid():
            new_schedule = Schedule(**schedule_create_form.cleaned_data)
            new_schedule.save()
            return HttpResponseRedirect(reverse('schedule-list'))    # redirects user to the schedule list page
    else:
        schedule_create_form = CreateScheduleForm(initial={'teacher': request.user})
    
    context = {
        'form': schedule_create_form,
        }
    
    return render(request, 'app/schedule_form.html', context)

class ScheduleUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/accounts/login/'
    model = Schedule
    fields = '__all__'

class ScheduleDelete(LoginRequiredMixin, DeleteView):
    login_url = '/accounts/login/'
    model = Schedule
    success_url = reverse_lazy('schedule-list')

@login_required
def ServiceInstanceCreate(request, pk):
    schedule = get_object_or_404(Schedule, pk=pk)
    
    # If the request is a POST, check if the fields are valid and the inputs, clean.
    # Save if valid.
    # If the request is not a POST, but a GET, add the initial schedule value
    if request.method == 'POST':
        serviceinstance_create_form = CreateServiceInstanceForm(request.POST, initial={'scheduled_for': schedule})

        if serviceinstance_create_form.is_valid():
            new_serviceinstane = ServiceInstance(**serviceinstance_create_form.cleaned_data)
            new_serviceinstane.save()
            return HttpResponseRedirect(reverse('schedule-detail', kwargs={'pk':pk}))    # redirects user to the schedule list page, kwarg pk specified to get back to the schedule
    else:
        serviceinstance_create_form = CreateServiceInstanceForm(initial={'scheduled_for': schedule})
    
    context = {
        'form': serviceinstance_create_form,
        }
    
    return render(request, 'app/serviceinstance_form.html', context)

class ServiceInstanceUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/accounts/login/'
    model = ServiceInstance
    fields = '__all__'
    
class ServiceInstanceDelete(LoginRequiredMixin, DeleteView):
    login_url = '/accounts/login/'
    model = ServiceInstance
    success_url = reverse_lazy('schedule-list')
