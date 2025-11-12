from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse
from datetime import datetime, time, date
from .models import Attendance, RegularizationRequest, Holiday
from django.db.models import Count

LATE_THRESHOLD = time(9, 30)
EARLY_LEAVE_THRESHOLD = time(17, 0)

@login_required
def mark_attendance(request):
    now = timezone.now()
    today = now.date()
    user = request.user

    if Holiday.objects.filter(date=today).exists():
        Attendance.objects.get_or_create(employee=user, date=today, defaults={'status': 'Holiday'})
        return redirect('attendance:view_attendance')

    attendance = Attendance.objects.filter(employee=user, date=today).first()
    if not attendance:
        status = 'Present'
        if now.time() > LATE_THRESHOLD:
            status = 'Late'
        Attendance.objects.create(employee=user, date=today, check_in=now.time(), status=status)
    else:
        attendance.check_out = now.time()
        if now.time() < EARLY_LEAVE_THRESHOLD:
            attendance.status = 'Early Leave'
        attendance.save()

    return redirect('attendance:view_attendance')

@login_required
def view_attendance(request):
    records = Attendance.objects.filter(employee=request.user).order_by('-date')
    return render(request, 'attendance/view_attendance.html', {'records': records})

@login_required
def monthly_summary(request):
    today = date.today()
    records = Attendance.objects.filter(employee=request.user, date__month=today.month, date__year=today.year)
    summary = records.values('status').annotate(count=Count('status'))
    return render(request, 'attendance/monthly_summary.html', {'summary': summary})

@login_required
def request_regularization(request, attendance_id):
    attendance = get_object_or_404(Attendance, id=attendance_id, employee=request.user)
    if request.method == 'POST':
        reason = request.POST.get('reason')
        RegularizationRequest.objects.create(employee=request.user, attendance=attendance, reason=reason)
        messages.success(request, "Request submitted.")
        return redirect('attendance:view_attendance')
    return render(request, 'attendance/request_regularization.html', {'attendance': attendance})

@login_required
def hr_approval_list(request):
    if request.user.role != 'HR_ADMIN':
        return redirect('attendance:view_attendance')
    requests = RegularizationRequest.objects.filter(approved=False)
    return render(request, 'attendance/hr_approval_list.html', {'requests': requests})

@login_required
def approve_request(request, request_id):
    req = get_object_or_404(RegularizationRequest, id=request_id)
    req.approved = True
    req.attendance.status = 'Regularized'
    req.attendance.save()
    req.save()
    messages.success(request, "Request approved.")
    return redirect('attendance:hr_approval_list')

import csv
from django.http import HttpResponse

@login_required
def export_attendance_csv(request):
    records = Attendance.objects.filter(employee=request.user)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="attendance.csv"'
    writer = csv.writer(response)
    writer.writerow(['Date', 'Check In', 'Check Out', 'Status', 'Work Hours'])
    for r in records:
        writer.writerow([r.date, r.check_in, r.check_out, r.status, r.work_hours()])
    return response


@login_required
def dashboard(request):
    if request.user.role == 'HR_ADMIN':
        return render(request, 'attendance/hr_dashboard.html')
    return render(request, 'attendance/employee_dashboard.html')