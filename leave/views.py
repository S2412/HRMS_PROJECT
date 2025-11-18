
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import LeaveRequest
from .forms import LeaveRequestForm

@login_required
def leave_dashboard(request):
    leaves = LeaveRequest.objects.filter(user=request.user)
    return render(request, 'leave/dashboard.html', {'leaves': leaves})

@login_required
def apply_leave(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.user = request.user
            leave.save()
            return redirect('leave:leave_dashboard')
    else:
        form = LeaveRequestForm()
    return render(request, 'leave/apply_leave.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def admin_leave_list(request):
    leaves = LeaveRequest.objects.all()
    return render(request, 'leave/admin_list.html', {'leaves': leaves})

@user_passes_test(lambda u: u.is_superuser)
def approve_leave(request, leave_id):
    leave = get_object_or_404(LeaveRequest, id=leave_id)
    leave.status = 'APPROVED'
    leave.save()
    return redirect('admin_leave_list')

@user_passes_test(lambda u: u.is_superuser)
def reject_leave(request, leave_id):
    leave = get_object_or_404(LeaveRequest, id=leave_id)
    leave.status = 'REJECTED'
    leave.save()
    return redirect('admin_leave_list')


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import LeaveRequest

def approve_leave(request, leave_id):
    leave = get_object_or_404(LeaveRequest, id=leave_id)
    leave.status = "APPROVED"
    leave.save()
    messages.success(request, "Leave approved successfully.")
    return redirect('accounts:hr_dashboard')

def reject_leave(request, leave_id):
    leave = get_object_or_404(LeaveRequest, id=leave_id)
    leave.status = "REJECTED"
    leave.save()
    messages.success(request, "Leave rejected.")
    return redirect('accounts:hr_dashboard')
