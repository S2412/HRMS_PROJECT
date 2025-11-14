from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import LeaveRequest
from .forms import LeaveRequestForm

# ✅ Public homepage view
def home(request):
    return HttpResponse("Welcome to the HRMS System!")

# ✅ List of leave requests for the logged-in user
@login_required
def leave_list(request):
    leaves = LeaveRequest.objects.filter(employee=request.user)
    return render(request, 'leave/list.html', {'leaves': leaves})

# ✅ Form to apply for leave
@login_required
def leave_apply(request):
    form = LeaveRequestForm(request.POST or None)
    if form.is_valid():
        leave = form.save(commit=False)
        leave.employee = request.user
        leave.full_clean()
        leave.save()
        return redirect('leave_list')  # Ensure this matches your URL name
    return render(request, 'leave/form.html', {'form': form})

# ✅ Detail view for a specific leave request
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
    leave = get_object_or_404(leave, pk=leave_id)
    leave.status = 'Approved'
    leave.save()
    messages.success(request, "Leave approved.")
    return redirect('leave:leave_list')  # or 'leave:admin_leave_list' if defined

def leave_detail(request, pk):
    leave = get_object_or_404(leave, pk=pk)
    return render(request, 'leave/leave_detail.html', {'leave': leave})
