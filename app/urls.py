from django.urls import path
from app import views
from django.contrib.admin.views.decorators import staff_member_required
# staff_member_required is a decorator enforcing the permission that only staff members have access to the url

urlpatterns = [
    path('', views.index, name='index'),
    # Student URLS
    path('studentlist/', staff_member_required(views.StudentListView.as_view()), name='student-list'), 
    path('studentlist/createstudent', staff_member_required(views.StudentCreate), name='create-student'), 
    path('student/<uuid:pk>', staff_member_required(views.StudentDetailView.as_view()), name='student-detail'),
    path('student/<uuid:pk>/updatestudent', staff_member_required(views.StudentUpdate.as_view()), name='update-student'),
    path('student/<uuid:pk>/deletestudent', staff_member_required(views.StudentDelete), name='delete-student'),
    # Schedule URLS
    path('schedulelist/', staff_member_required(views.ScheduleListView.as_view()), name='schedule-list'),
    path('schedulelist/createschedule', staff_member_required(views.ScheduleCreate), name='create-schedule'),
    path('schedule/<int:pk>', staff_member_required(views.ScheduleDetailView), name='schedule-detail'),
    path('schedule/<int:pk>/updateschedule', staff_member_required(views.ScheduleUpdate.as_view()), name='update-schedule'),
    path('schedule/<int:pk>/deleteschedule', staff_member_required(views.ScheduleDelete.as_view()), name='delete-schedule'),
    # Service URLS
    path('servicelist/', staff_member_required(views.ServiceListView.as_view()), name='service-list'),
    path('servicedetail/<int:pk>', staff_member_required(views.ServiceDetailView.as_view()), name='service-detail'),
    path('studentlist/<uuid:pk>/createservice', staff_member_required(views.ServiceCreate), name='create-service'),
    path('service/<int:pk>/updateservice', staff_member_required(views.ServiceUpdate.as_view()), name='update-service'),
    path('service/<int:pk>/deleteservice', staff_member_required(views.ServiceDelete.as_view()), name='delete-service'),
    # Service Instance URLS
    path('schedule/<int:pk>/createserviceappt', staff_member_required(views.ServiceInstanceCreate), name='create-serviceinstance'),
    path('serviceinstance/<int:pk>/updateserviceappt', staff_member_required(views.ServiceInstanceUpdate.as_view()), name='update-serviceinstance'),
    path('serviceinstance/<int:pk>/deleteserviceappt', staff_member_required(views.ServiceInstanceDelete.as_view()), name='delete-serviceinstance'),
    path('serviceinstance/<int:pk>', staff_member_required(views.ServiceInstanceDetailView.as_view()), name='serviceinstance-detail'),
]
