from django.urls import path
from app import views


urlpatterns = [
    path('', views.index, name='index'),
    path('studentlist/', views.StudentListView.as_view(), name='student-list'),
    path('student/<uuid:pk>', views.StudentDetailView.as_view(), name='student-detail'),
    path('schedulelist/', views.ScheduleListView.as_view(), name='schedule-list'),
    path('schedule/<uuid:pk>', views.ScheduleDetailView, name='schedule-detail'),
    path('servicelist/', views.ServiceListView.as_view(), name='service-list'),
    path('servicedetail/<int:pk>', views.ServiceDetailView.as_view(), name='service-detail'),
    path('serviceinstancedetail/', views.ServiceInstanceDetailView.as_view(), name='serviceinstance-detail'),
]
