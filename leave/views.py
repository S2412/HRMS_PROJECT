from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import LeaveRequest
from .forms import LeaveRequestForm

@login_required
def apply_leave(request):
    form = LeaveRequestForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        leave = form.save(commit=False)
        leave.employee = request.user
        leave.full_clean()
        leave.save()
        messages.success(request, "Leave request submitted successfully.")
        return redirect('leave:view_leave_history')
    return render(request, 'leave/apply_leave.html', {'form': form})

@login_required
def view_leave_history(request):
    leaves = LeaveRequest.objects.filter(employee=request.user).order_by('-applied_on')
    employee_name = request.user.get_full_name() or request.user.username
    return render(request, 'leave/view_leave_history.html', {
        'leaves': leaves,
        'employee_name': employee_name
    })

@login_required
def cancel_leave(request, leave_id):
    leave = get_object_or_404(LeaveRequest, leave_id=leave_id, employee=request.user)
    if leave.status == 'Pending':
        leave.status = 'Cancelled'
        leave.save()
        messages.info(request, "Leave request cancelled.")
    return redirect('leave:view_leave_history')

@login_required
def admin_leave_list(request):
    if request.user.role != 'HR_ADMIN':
        return redirect('accounts:login')
    leaves = LeaveRequest.objects.all().order_by('-applied_on')
    return render(request, 'leave/admin_leave_list.html', {'leaves': leaves})

@login_required
def approve_leave(request, leave_id):
    leave = get_object_or_404(LeaveRequest, leave_id=leave_id)
    leave.status = 'Approved'
    leave.save()
    messages.success(request, "Leave approved.")
    return redirect('leave:admin_leave_list')