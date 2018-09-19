from django.urls import path
from app import views
from django.contrib.admin.views.decorators import staff_member_required

urlpatterns = [
    path('', views.index, name='index'),
    path('studentlist/', staff_member_required(views.StudentListView.as_view()), name='student-list'),
    path('student/<uuid:pk>', staff_member_required(views.StudentDetailView.as_view()), name='student-detail'),
    path('schedulelist/', staff_member_required(views.ScheduleListView.as_view()), name='schedule-list'),
    path('schedule/<uuid:pk>', staff_member_required(views.ScheduleDetailView), name='schedule-detail'),
    path('servicelist/', staff_member_required(views.ServiceListView.as_view()), name='service-list'),
    path('servicedetail/<int:pk>', staff_member_required(views.ServiceDetailView.as_view()), name='service-detail'),
    path('serviceinstancedetail/', staff_member_required(views.ServiceInstanceDetailView.as_view()), name='serviceinstance-detail'),
    path('studentlist/create', staff_member_required(views.StudentCreate.as_view()), name='create-student'),
    path('student/<uuid:pk>/update', staff_member_required(views.StudentUpdate.as_view()), name='update-student'),
    path('student/<uuid:pk>/delete', staff_member_required(views.StudentDelete.as_view()), name='delete-student'),
]
