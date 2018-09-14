from django.db import models
import uuid # placeholder for student IDs

# Create your models here.
class Student(models.Model):
    """Model representing a Student."""
    first_name = models.CharField(max_length=20, help_text='Enter First Name')
    middle_name = models.CharField(max_length=20, null=True, blank=True, help_text='Enter Middle Name')
    last_name = models.CharField(max_length=20, help_text='Enter Last Name')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this student')
    
    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        """String for representing the Model "Student" object."""
        return f'{self.last_name}, {self.first_name}'

class Service(models.Model):
    """Model representing a Time Service for a Student"""
    total_time_req = models.IntegerField(help_text='Enter total time required')
    student = models.ForeignKey('Student', on_delete=models.SET_NULL, null=True)
    satisfied = models.BooleanField(help_text='Check if this service has been satisfied')
    
    SUBJECTS = (
        ('MATH', 'Math'),
        ('ELA', 'ELA')
        )

    subject = models.CharField(
        max_length=4,
        choices=SUBJECTS,
        blank=True,
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
        blank=True,
        default=None,
        help_text='Service type'
        )

    def __str__(self):
        """String for representing the Model "Service" object."""
        return f'{str(self.student)}: {self.subject} {self.service_type}'

class ServiceInstance(models.Model):
    """Model representing a ServiceInstance"""
    duration = models.IntegerField(help_text='Enter duration of this service')
    service = models.ForeignKey('Service', on_delete=models.SET_NULL, null=True)
    calendar = models.ForeignKey('Calendar', on_delete=models.SET_NULL, null=True)
    
    DAYS = (
        ('M','Monday'),
        ('Tu','Tuesday'),
        ('W','Wednesday'),
        ('Th','Thursday'),
        ('F','Friday'),
        )

    day = models.CharField(
        max_length=1,
        choices=DAYS,
        help_text='Day for the service')

    def __str__(self):
        """String for representing the Model "ServiceInstance" object."""
        return f'{self.service}: {self.day} {self.duration}'

class Calendar(models.Model):
    """Model representing a Calendar"""
    title = models.CharField(max_length=200, help_text='Enter title for this schedule')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        """String representing the Model "Calendar" object."""
        return f'{self.title} Start: {self.start_date} End: {self.end_date}'
