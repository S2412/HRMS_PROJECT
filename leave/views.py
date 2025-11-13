from django.shortcuts import render, redirect, get_object_or_404
from .models import LeaveRequest
from .forms import LeaveRequestForm
from django.contrib.auth.decorators import login_required

@login_required
def leave_list(request):
    leaves = LeaveRequest.objects.filter(employee=request.user)
    return render(request, 'leave/list.html', {'leaves': leaves})

@login_required
def leave_apply(request):
    form = LeaveRequestForm(request.POST or None)
    if form.is_valid():
        leave = form.save(commit=False)
        leave.employee = request.user
        leave.save()
        return redirect('leave_list')
    return render(request, 'leave/form.html', {'form': form})

@login_required
def leave_detail(request, pk):
    leave = get_object_or_404(LeaveRequest, pk=pk, employee=request.user)
    return render(request, 'leave/detail.html', {'leave': leave})