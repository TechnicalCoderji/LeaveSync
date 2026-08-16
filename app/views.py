from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import EmployeeInfo, LeaveRequest
from .forms import LeaveRequestForm

@login_required
def home_view(request):
    user = request.user
    user_info = getattr(user, 'user_info', None)
    
    is_manager = user_info.is_manager if user_info else False
    
    if is_manager:
        # Manager view: See leave requests from all users in the same organization
        leave_requests = LeaveRequest.objects.filter(
            user__user_info__organization=user_info.organization
        ).order_by('-id')
        context = {
            'is_manager': True,
            'user_info': user_info,
            'leave_requests': leave_requests
        }
    else:
        # Employee view: See personal leave status and own requests
        employee_info = getattr(user, 'employee_info', None)
        leave_requests = LeaveRequest.objects.filter(user=user).order_by('-id')
        
        if request.method == 'POST':
            form = LeaveRequestForm(request.POST)
            if form.is_valid():
                leave = form.save(commit=False)
                leave.user = user
                leave.save()
                messages.success(request, "Leave request submitted successfully.")
                return redirect('home')
        else:
            form = LeaveRequestForm()

        context = {
            'is_manager': False,
            'user_info': user_info,
            'employee_info': employee_info,
            'leave_requests': leave_requests,
            'form': form
        }

    return render(request, 'home.html', context)

@login_required
def update_leave_status(request, request_id, status):
    if not getattr(request.user, 'user_info', None) or not request.user.user_info.is_manager:
        messages.error(request, "Unauthorized access.")
        return redirect('home')
        
    leave_req = get_object_or_404(LeaveRequest, id=request_id)
    if status in ['Approved', 'Rejected']:
        leave_req.status = status
        leave_req.save()
        
        # Deduct leave days if approved and employee info exists
        if status == 'Approved' and hasattr(leave_req.user, 'employee_info'):
            emp_info = leave_req.user.employee_info
            emp_info.remaining_leave -= leave_req.leave_day
            emp_info.save()

        messages.success(request, f"Leave request #{leave_req.id} marked as {status}.")
    
    return redirect('home')