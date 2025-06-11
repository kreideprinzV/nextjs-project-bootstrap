from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

class Employee(models.Model):
    POSITION_CHOICES = [
        ('MANAGER', 'Manager'),
        ('CHEF', 'Chef'),
        ('WAITER', 'Waiter/Waitress'),
        ('CASHIER', 'Cashier'),
        ('KITCHEN', 'Kitchen Staff'),
        ('CLEANER', 'Cleaning Staff'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='employee_profile'
    )
    position = models.CharField(max_length=20, choices=POSITION_CHOICES)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    emergency_contact = models.CharField(max_length=100)
    emergency_phone = models.CharField(max_length=20)
    date_hired = models.DateField()
    hourly_rate = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.position}"

    class Meta:
        ordering = ['user__last_name', 'user__first_name']

class Schedule(models.Model):
    SHIFT_CHOICES = [
        ('MORNING', 'Morning Shift'),
        ('AFTERNOON', 'Afternoon Shift'),
        ('EVENING', 'Evening Shift'),
        ('NIGHT', 'Night Shift'),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='schedules'
    )
    date = models.DateField()
    shift = models.CharField(max_length=20, choices=SHIFT_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date', 'start_time']
        unique_together = ['employee', 'date', 'shift']

    def __str__(self):
        return f"{self.employee.user.get_full_name()} - {self.date} {self.shift}"

    def clean(self):
        # Check if end time is after start time
        if self.end_time <= self.start_time:
            raise ValidationError("End time must be after start time")
        
        # Check for overlapping shifts
        overlapping = Schedule.objects.filter(
            employee=self.employee,
            date=self.date
        ).exclude(id=self.id)
        
        for schedule in overlapping:
            if (self.start_time < schedule.end_time and 
                self.end_time > schedule.start_time):
                raise ValidationError("This schedule overlaps with another shift")

class Attendance(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='attendance'
    )
    schedule = models.ForeignKey(
        Schedule,
        on_delete=models.CASCADE,
        related_name='attendance_records'
    )
    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('PRESENT', 'Present'),
            ('ABSENT', 'Absent'),
            ('LATE', 'Late'),
            ('LEAVE', 'On Leave'),
        ],
        default='ABSENT'
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-schedule__date', '-check_in']
        unique_together = ['employee', 'schedule']

    def __str__(self):
        return f"{self.employee.user.get_full_name()} - {self.schedule.date} ({self.status})"

    def clean(self):
        if self.check_out and self.check_in:
            if self.check_out <= self.check_in:
                raise ValidationError("Check-out time must be after check-in time")

class Leave(models.Model):
    LEAVE_TYPES = [
        ('SICK', 'Sick Leave'),
        ('VACATION', 'Vacation'),
        ('PERSONAL', 'Personal Leave'),
        ('OTHER', 'Other'),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='leaves'
    )
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'Pending'),
            ('APPROVED', 'Approved'),
            ('REJECTED', 'Rejected'),
        ],
        default='PENDING'
    )
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_leaves'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.employee.user.get_full_name()} - {self.leave_type} ({self.start_date} to {self.end_date})"

    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError("End date must be after start date")
