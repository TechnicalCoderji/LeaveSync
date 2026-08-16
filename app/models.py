from django.db import models
from django.conf import settings

# Create your models here.
class EmployeeInfo(models.Model):
    # Reference CustomUser via settings.AUTH_USER_MODEL for modularity
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='employee_info'
    )
    remaining_leave = models.IntegerField(default=24)

    def __str__(self):
        return f"{self.user.username} - Remaining Leaves: {self.remaining_leave}"

class LeaveRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='leave_requests'
    )
    start_date = models.DateField()
    end_date = models.DateField()
    leave_day = models.IntegerField()
    reason = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Request #{self.id} - {self.user.username} ({self.status})"