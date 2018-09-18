from django.db import models
import uuid # placeholder for student IDs
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import User

# Create your models here.
class Student(models.Model):
    """Model representing a Student."""
    first_name = models.CharField(max_length=20, help_text='Enter First Name')
    middle_name = models.CharField(max_length=20, null=True, blank=True, help_text='Enter Middle Name')
    last_name = models.CharField(max_length=20, help_text='Enter Last Name')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    serviced = models.BooleanField(default=False, help_text='Check if the services for this student have been completed')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this student')
    
    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        """String for representing the Model "Student" object."""
        return f'{self.last_name}, {self.first_name}'

    def get_absolute_url(self):
        """Returns the url to access a detail record for this student"""
        return reverse('student-detail', args=[str(self.id)])
    @property
    def is_serviced(self):
        for service in self.services.all():
            if not service.is_satisfied:
                return False
        return True
    
class Service(models.Model):
    """Model representing a Time Service for a Student"""
    student = models.ForeignKey('Student', related_name='services', on_delete=models.SET_NULL, null=True)
    
    SUBJECTS = (
        ('MATH', 'Math'),
        ('ELA', 'ELA')
        )

    subject = models.CharField(
        max_length=4,
        choices=SUBJECTS,
        default=None,
        help_text='Subject'
        )

    SERVICES = (
        ('PI', 'Push-In'),
        ('PO', 'Pull-Out')
        )
        
    service_type = models.CharField(
        max_length=2,
        choices=SERVICES,
        default=None,
        help_text='Service type'
        )
    
    total_time_req = models.IntegerField(help_text='Enter total time required')
    satisfied = models.BooleanField(help_text='Check if this service has been satisfied')

    def __str__(self):
        """String for representing the Model "Service" object."""
        return f'{str(self.student)}: {self.subject} {self.service_type}'

    def get_absolute_url(self):
        """Returns a URL for displaying all instances of this service"""
        return reverse('service-detail', args=[str(self.id)])

    @property
    def is_satisfied(self):
        allocated_time= 0
        for serviceinstance in self.stud_serviceinstances.all():
            allocated_time += serviceinstance.duration
        return allocated_time >= self.total_time_req

class ServiceInstance(models.Model):
    """Model representing a ServiceInstance"""
    service = models.ForeignKey('Service', related_name='stud_serviceinstances', on_delete=models.SET_NULL, null=True, help_text='The particular service this belongs to')
    DAYS = (
        ('M','Monday'),
        ('Tu','Tuesday'),
        ('W','Wednesday'),
        ('Th','Thursday'),
        ('F','Friday'),
        )

    day = models.CharField(
        max_length=2,
        choices=DAYS,
        help_text='Day for the service')
    duration = models.IntegerField(help_text='Enter duration of this service (in minutes)')
    scheduled_for = models.ForeignKey('Schedule', related_name='sched_serviceinstances', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """String for representing the Model "ServiceInstance" object."""
        return f'{self.service}: {self.day} {self.duration}'

class Schedule(models.Model):
    """Model representing a Schedule"""
    title = models.CharField(max_length=200, help_text='Enter title for this schedule')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this student')

    def __str__(self):
        """String representing the Model "Schedule" object."""
        return f'{self.title} Start: {self.start_date} End: {self.end_date}'

    def get_absolute_url(self):
        """Returns the url to access a detail record for this student"""
        return reverse('schedule-detail', args=[str(self.id)])
