from django.shortcuts import render
from app.models import Student, Service, ServiceInstance, Schedule
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# Following 2 implement requirements for user to
# be logged in or have the right permissions
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
# Finds a specific object using the primary key, or returns 404 if not found
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

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
    login_url = '/accounts/login/'
    model = Student
     
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
    appts = {
        "M": [],
        "Tu": [],
        "W": [],
        "Th": [],
        "F": [],
        }

    for serviceinstance in schedule.sched_serviceinstances.all():
        appts[serviceinstance.day].append(serviceinstance)
        
    context = {
        "schedule": schedule,
        "appts": appts,
        }
    return render(request, "app/schedule_detail.html", context)

class ServiceListView(LoginRequiredMixin, generic.ListView):
    login_url = '/accounts/login/'
    model = Service

    def get_queryset(self):
        return Service.objects.filter(student__teacher=self.request.user)

class ServiceDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = '/accounts/login/'
    model = Service

class ServiceInstanceDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = '/accounts/login/'
    model = ServiceInstance

class StudentCreate(LoginRequiredMixin, CreateView):
    login_url = '/accounts/login/'
    model = Student
    fields = '__all__'

class StudentUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/accounts/login/'
    model = Student
    fields = '__all__'

class StudentDelete(LoginRequiredMixin, DeleteView):
    login_url = '/accounts/login/'
    model = Student
    success_url = reverse_lazy('student-list')
    
    
