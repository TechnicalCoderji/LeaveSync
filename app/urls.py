from django.urls import path
from .views import home_view, update_leave_status

urlpatterns = [
    path('', home_view, name='home'),
    path('leave/update/<int:request_id>/<str:status>/', update_leave_status, name='update_leave_status'),
]