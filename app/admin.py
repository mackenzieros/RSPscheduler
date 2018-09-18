from django.contrib import admin

# Register your models here.
from app.models import Student, Service, ServiceInstance, Schedule

#admin.site.register(Student)
#admin.site.register(Service)
admin.site.register(ServiceInstance)
admin.site.register(Schedule)

class ServiceInstanceInline(admin.TabularInline):
    model = ServiceInstance
    
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    inlines = [ServiceInstanceInline]

    fieldsets = (
        (None, {
            'fields': ('student',),
            }),
        ('Service details', {
            'fields': ('subject', 'service_type', 'total_time_req', 'satisfied',)
            }),
        )

class ServiceInline(admin.TabularInline):
    model = Service
    extra = 1
    max_num = 4
    
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'middle_name', 'first_name')
    inlines = [ServiceInline]

