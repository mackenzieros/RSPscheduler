from django.shortcuts import render
from app.models import Student, Service, ServiceInstance, Schedule
from django.views import generic
# Following 2 implement requirements for user to
# be logged in or have the right permissions
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
# Finds a specific object using the primary key, or returns 404 if not found
from django.shortcuts import get_object_or_404


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

class StudentDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    login_url = '/accounts/login/'
    permission_required = 'app.is_staff'
    model = Student
    
class StudentListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    login_url = '/accounts/login/'
    permission_required = 'app.is_staff'
    model = Student

class ScheduleListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    login_url = '/accounts/login/'
    permission_required = 'app.is_staff'
    model = Schedule

@login_required
@permission_required('is_staff')
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

class ServiceListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    login_url = '/accounts/login/'
    permission_required = 'app.is_staff'
    model = Service

class ServiceDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    login_url = '/accounts/login/'
    permission_required = 'app.is_staff'
    model = Service

class ServiceInstanceDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    login_url = '/accounts/login/'
    permission_required = 'app.is_staff'
    model = ServiceInstance
