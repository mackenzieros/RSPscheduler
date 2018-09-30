from django.db import models
import uuid # placeholder for student IDs
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

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
    # Checks all the services appointed to the student, will be True if all the
    # services are met, false otherwise
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
        ('Push-In', 'Push-In'),
        ('Pull-Out', 'Pull-Out')
        )
        
    service_type = models.CharField(
        max_length=8,
        choices=SERVICES,
        default=None,
        help_text='Service type'
        )
    
    total_time_req = models.IntegerField(help_text='Enter total time required')
    satisfied = models.BooleanField(help_text='Check if this service has been satisfied')
        
    def __str__(self):
        """String for representing the Model "Service" object."""
        return f'{str(self.student)}\n{self.subject} {self.service_type}'

    def get_absolute_url(self):
        """Returns a URL for displaying all instances of this service"""
        return reverse('service-detail', args=[str(self.id)])

    # Goes through all the service instances associated with this service
    # If each service instance that belongs to an active calendar adds up to
    # the time required, then the service is satisfied!
    @property
    def is_satisfied(self):
        allocated_time= 0
        for serviceinstance in self.stud_serviceinstances.all():
            if serviceinstance.scheduled_for.active:
                if serviceinstance.duration:
                    allocated_time += serviceinstance.duration
        return allocated_time >= self.total_time_req

class ServiceInstance(models.Model):
    """Model representing a ServiceInstance"""
    service = models.ForeignKey('Service', related_name='stud_serviceinstances', on_delete=models.SET_NULL, null=True, help_text='The particular service this belongs to')
    DAYS = (
        ('Monday','Monday'),
        ('Tuesday','Tuesday'),
        ('Wednesday','Wednesday'),
        ('Thursday','Thursday'),
        ('Friday','Friday'),
        )

    day = models.CharField(
        max_length=9,
        choices=DAYS,
        help_text='Day for the service')

    time_start = models.TimeField(default=timezone.now, blank=True)
    time_end = models.TimeField(default=timezone.now, blank=True)
    scheduled_for = models.ForeignKey('Schedule', related_name='sched_serviceinstances', on_delete=models.SET_NULL, null=True)

    @property
    def duration(self):
        if self.time_start != None and self.time_end != None:   # check because time_start and time_end can be blank
            start = timedelta(hours=self.time_start.hour, minutes=self.time_start.minute, seconds=self.time_start.second)
            end = timedelta(hours=self.time_end.hour, minutes=self.time_end.minute, seconds=self.time_end.second)
            # must reformat the timedelta if the hour is at or beyond 12 to fit 12-hour clock format
            if start.seconds // 3600 >= 12:
                start = timedelta(hours=((start.seconds//3600) - 12), minutes=((start.seconds%3600)//60), seconds=start.seconds%60)
            if end.seconds // 3600 >= 12:
                end = timedelta(hours=((end.seconds//3600) - 12), minutes=((end.seconds%3600)//60), seconds=end.seconds%60)
            time = end - start
            duration = abs(int(time.total_seconds() / 60))
            return duration
    
    def __str__(self):
        """String for representing the Model "ServiceInstance" object."""
        return '{service}\n{day}\n{start} - {end}'.format(service=self.service, day=self.day,
                                                                                         start=self.time_start.strftime("%I:%M"), end=self.time_end.strftime("%I:%M"))

    def get_absolute_url(self):
        """Returns a URL for displaying the details of this Service Instance"""
        return reverse('serviceinstance-detail', args=[str(self.id)])
    
class Schedule(models.Model):
    """Model representing a Schedule"""
    title = models.CharField(max_length=200, help_text='Enter title for this schedule')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    active = models.BooleanField(default=False)

    # Function to represent the constraint of one model having the "active"
    # field to be True
    # This function was found at: https://stackoverflow.com/questions/44718872/django-model-where-only-one-row-can-have-active-true
    def save(self, *args, **kwargs):
        if self.active:
            queryset = type(self).objects.filter(active=True)
            if self.pk:
                queryset = queryset.exclude(pk=self.pk)
            queryset.update(active=False)
        super(Schedule, self).save(*args, **kwargs)

    def __str__(self):
        """String representing the Model "Schedule" object."""
        return f'{self.title} Start: {self.start_date} End: {self.end_date}'

    def get_absolute_url(self):
        """Returns the url to access a detail record for this student"""
        return reverse('schedule-detail', args=[str(self.id)])
