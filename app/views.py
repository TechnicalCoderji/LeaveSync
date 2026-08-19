from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from datetime import timedelta
from .models import EmployeeInfo, LeaveRequest
from .forms import LeaveRequestForm

User = get_user_model()

def landing_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'landing.html')

def calculate_business_days(start_date, end_date):
    """Calculates total days between two dates excluding weekends."""
    days = 0
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() < 5:  # 0-4 denotes Monday-Friday
            days += 1
        current_date += timedelta(days=1)
    return days

@login_required
def dashboard_view(request):
    user = request.user
    user_info = getattr(user, 'user_info', None)
    is_manager = user_info.is_manager if user_info else False
    
    if is_manager:
        leave_requests = LeaveRequest.objects.filter(
            user__user_info__organization=user_info.organization
        ).order_by('-id')
        
        context = {
            'is_manager': True,
            'user_info': user_info,
            'leave_requests': leave_requests
        }
    else:
        employee_info = getattr(user, 'employee_info', None)
        leave_requests = LeaveRequest.objects.filter(user=user).order_by('-id')
        
        if request.method == 'POST':
            form = LeaveRequestForm(request.POST)
            if form.is_valid():
                leave = form.save(commit=False)
                leave.user = user
                
                # Automatically calculate days excluding weekends
                leave.leave_day = calculate_business_days(leave.start_date, leave.end_date)
                
                # Prevent negative or zero days if end date is before start date
                if leave.leave_day > 0:
                    leave.save()
                    messages.success(request, f"Leave request for {leave.leave_day} days submitted successfully.")
                else:
                    messages.error(request, "Invalid date range or no working days selected.")
                return redirect('dashboard')
        else:
            form = LeaveRequestForm()

        context = {
            'is_manager': False,
            'user_info': user_info,
            'employee_info': employee_info,
            'leave_requests': leave_requests,
            'form': form
        }

    return render(request, 'dashboard.html', context)

@login_required
def profile_view(request):
    user = request.user
    user_info = getattr(user, 'user_info', None)
    is_manager = user_info.is_manager if user_info else False

    if is_manager:
        # Get all non-manager employees in the same organization
        employees = User.objects.filter(
            user_info__organization=user_info.organization,
            user_info__is_manager=False
        )
        context = {
            'is_manager': True,
            'user_info': user_info,
            'employees': employees
        }
    else:
        employee_info = getattr(user, 'employee_info', None)
        # Find a manager in the same organization
        manager = User.objects.filter(
            user_info__organization=user_info.organization,
            user_info__is_manager=True
        ).first()
        
        context = {
            'is_manager': False,
            'user_info': user_info,
            'employee_info': employee_info,
            'manager_name': manager.username if manager else "N/A"
        }

    return render(request, 'profile.html', context)

@login_required
def update_leave_status(request, request_id, status):
    if not getattr(request.user, 'user_info', None) or not request.user.user_info.is_manager:
        messages.error(request, "Unauthorized access.")
        return redirect('dashboard')
        
    leave_req = get_object_or_404(LeaveRequest, id=request_id)
    if status in ['Approved', 'Rejected']:
        leave_req.status = status
        leave_req.save()
        
        if status == 'Approved' and hasattr(leave_req.user, 'employee_info'):
            emp_info = leave_req.user.employee_info
            emp_info.remaining_leave -= leave_req.leave_day
            emp_info.save()

        messages.success(request, f"Leave request #{leave_req.id} marked as {status}.")
    
    return redirect('dashboard')