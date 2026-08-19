from django.urls import path
from .views import dashboard_view, profile_view, update_leave_status, landing_view

urlpatterns = [
    path('', landing_view, name='landing'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('profile/', profile_view, name='profile'),
    path('leave/update/<int:request_id>/<str:status>/', update_leave_status, name='update_leave_status'),
]