from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse
from datetime import datetime, time, date
from django.db.models import Count
import csv

from .models import Attendance, RegularizationRequest, Holiday
from .forms import AttendanceForm, RegularizationForm

# Thresholds
LATE_THRESHOLD = time(9, 30)
EARLY_LEAVE_THRESHOLD = time(17, 0)

# 🕒 Mark Attendance Automatically
@login_required
def mark_attendance(request):
    now = timezone.now()
    today = now.date()
    user = request.user

    if Holiday.objects.filter(date=today).exists():
        Attendance.objects.get_or_create(
            employee=user,
            date=today,
            defaults={'status': 'Holiday'}
        )
        return redirect('attendance:view_attendance')

    attendance = Attendance.objects.filter(employee=user, date=today).first()
    if not attendance:
        status = 'Present'
        if now.time() > LATE_THRESHOLD:
            status = 'Late'
        Attendance.objects.create(
            employee=user,
            date=today,
            check_in=now.time(),
            status=status
        )
    else:
        attendance.check_out = now.time()
        if now.time() < EARLY_LEAVE_THRESHOLD:
            attendance.status = 'Early Leave'
        attendance.save()

    return redirect('attendance:view_attendance')

# 📝 Mark Attendance via Form
@login_required
def mark_attendance_form(request):
    today = timezone.now().date()
    attendance, created = Attendance.objects.get_or_create(
        employee=request.user,
        date=today
    )

    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            form.save()
            messages.success(request, "Attendance marked successfully.")
            return redirect('attendance:view_attendance')
    else:
        form = AttendanceForm(instance=attendance)

    return render(request, 'attendance/mark_attendance_form.html', {'form': form})

# 📋 View Attendance Records
@login_required
def view_attendance(request):
    records = Attendance.objects.filter(employee=request.user).order_by('-date')
    return render(request, 'attendance/view_attendance.html', {'records': records})

# 📊 Monthly Summary
@login_required
def monthly_summary(request):
    today = date.today()
    records = Attendance.objects.filter(
        employee=request.user,
        date__month=today.month,
        date__year=today.year
    )
    summary = records.values('status').annotate(count=Count('status'))
    return render(request, 'attendance/monthly_summary.html', {'summary': summary})

# 🛠️ Request Regularization
@login_required
def request_regularization(request, attendance_id):
    attendance = get_object_or_404(Attendance, id=attendance_id, employee=request.user)

    if request.method == 'POST':
        form = RegularizationForm(request.POST)
        if form.is_valid():
            reg = form.save(commit=False)
            reg.employee = request.user
            reg.attendance = attendance
            reg.save()
            messages.success(request, "Regularization request submitted.")
            return redirect('attendance:view_attendance')
    else:
        form = RegularizationForm()

    return render(request, 'attendance/request_regularization.html', {
        'form': form,
        'attendance': attendance
    })

# ✅ HR Approval List
@login_required
def hr_approval_list(request):
    if request.user.role != 'HR_ADMIN':
        return redirect('attendance:view_attendance')

    requests = RegularizationRequest.objects.filter(approved=False)
    return render(request, 'attendance/hr_approval_list.html', {'requests': requests})

# ✅ Approve Regularization Request
@login_required
def approve_request(request, request_id):
    req = get_object_or_404(RegularizationRequest, id=request_id)
    req.approved = True
    req.attendance.status = 'Regularized'
    req.attendance.save()
    req.save()
    messages.success(request, "Request approved.")
    return redirect('attendance:hr_approval_list')

# 📤 Export Attendance to CSV
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

# 🧭 Role-Based Dashboard
@login_required
def dashboard(request):
    if request.user.role == 'HR_ADMIN':
        return render(request, 'attendance/hr_dashboard.html')
    return render(request, 'attendance/employee_dashboard.html')