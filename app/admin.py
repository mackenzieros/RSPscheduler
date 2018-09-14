from django.contrib import admin

# Register your models here.
from app.models import Student, Service, ServiceInstance, Calendar

admin.site.register(Student)
admin.site.register(Service)
admin.site.register(ServiceInstance)
admin.site.register(Calendar)
