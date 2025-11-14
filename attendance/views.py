from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import time, timedelta
from .models import Attendance, Holiday, RegularizationRequest
from .forms import AttendanceForm, RegularizationRequestForm

LATE_THRESHOLD = time(9, 30)
EARLY_LEAVE_THRESHOLD = time(17, 0)

def parse_ampm_time(hour, minute, ampm):
    hour = int(hour)
    minute = int(minute)
    if ampm == 'PM' and hour != 12:
        hour += 12
    elif ampm == 'AM' and hour == 12:
        hour = 0
    return time(hour, minute)

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

@login_required
def mark_attendance_form(request):
    today = timezone.now().date()
    attendance, created = Attendance.objects.get_or_create(
        employee=request.user,
        date=today
    )

    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=attendance)
        form.fields['employee'].initial = request.user

        if form.is_valid():
            check_in = parse_ampm_time(
                request.POST.get('check_in_hour'),
                request.POST.get('check_in_minute'),
                request.POST.get('check_in_ampm')
            )
            check_out = parse_ampm_time(
                request.POST.get('check_out_hour'),
                request.POST.get('check_out_minute'),
                request.POST.get('check_out_ampm')
            )

            attendance.check_in = check_in
            attendance.check_out = check_out
            attendance.status = form.cleaned_data['status']
            attendance.is_overtime_manual = form.cleaned_data['is_overtime_manual']
            attendance.overtime_hours = form.cleaned_data['overtime_hours']
            attendance.employee = request.user
            attendance.save()

            messages.success(request, "Attendance marked successfully.")
            return redirect('attendance:view_attendance')
    else:
        form = AttendanceForm(instance=attendance)
        form.fields['employee'].initial = request.user

    context = {
        'form': form,
        'hours': range(1, 13),
        'minutes': [f"{i:02d}" for i in range(0, 60, 5)],
    }
    return render(request, 'attendance/mark_attendance_form.html', context)

@login_required
def view_attendance(request):
    if request.user.is_staff or request.user.is_superuser:
        username = request.GET.get('username')
        user = User.objects.filter(username=username).first() or request.user
        all_users = User.objects.all()
    else:
        user = request.user
        all_users = []

    records = Attendance.objects.filter(employee=user).order_by('-date')
    employee_name = user.get_full_name() or user.username

    return render(request, 'attendance/view_attendance.html', {
        'records': records,
        'employee_name': employee_name,
        'all_users': all_users
    })

@login_required
def submit_regularization_request(request):
    if request.method == 'POST':
        form = RegularizationRequestForm(request.POST)
        if form.is_valid():
            regularization = form.save(commit=False)
            regularization.employee = request.user
            regularization.save()
            messages.success(request, "Regularization request submitted.")
            return redirect('attendance:view_attendance')
    else:
        form = RegularizationRequestForm()
    return render(request, 'attendance/regularization_form.html', {'form': form})

@login_required
def monthly_attendance(request):
    user = request.user
    records = Attendance.objects.filter(employee=user).order_by('date')
    return render(request, 'attendance/monthly_attendance.html', {'records': records})

@login_required
def attendance_summary(request):
    user = request.user
    records = Attendance.objects.filter(employee=user)
    total_days = records.count()
    present_days = records.filter(status='Present').count()
    late_days = records.filter(status='Late').count()
    early_leave_days = records.filter(status='Early Leave').count()
    holidays = records.filter(status='Holiday').count()

    total_overtime = sum([r.overtime_hours or 0 for r in records])

    return render(request, 'attendance/summary.html', {
        'total_days': total_days,
        'present_days': present_days,
        'late_days': late_days,
        'early_leave_days': early_leave_days,
        'holidays': holidays,
        'total_overtime': total_overtime
    })
import csv
from django.http import HttpResponse
from .models import Attendance  # adjust if your model is named differently

def export_attendance_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="attendance.csv"'

    writer = csv.writer(response)
    writer.writerow(['Employee ID', 'Date', 'Status'])  # adjust headers

    for record in Attendance.objects.all():
        writer.writerow([record.employee_id, record.date, record.status])  # adjust fields

    return response