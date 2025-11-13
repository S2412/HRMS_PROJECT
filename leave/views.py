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
        leave.save()
        return redirect('leave_list')  # Ensure this matches your URL name
    return render(request, 'leave/form.html', {'form': form})

# ✅ Detail view for a specific leave request
@login_required
def leave_detail(request, pk):
    leave = get_object_or_404(LeaveRequest, pk=pk, employee=request.user)
    return render(request, 'leave/detail.html', {'leave': leave})