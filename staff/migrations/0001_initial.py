# Generated by Django 5.2.3 on 2025-06-11 01:39

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Employee",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "position",
                    models.CharField(
                        choices=[
                            ("MANAGER", "Manager"),
                            ("CHEF", "Chef"),
                            ("WAITER", "Waiter/Waitress"),
                            ("CASHIER", "Cashier"),
                            ("KITCHEN", "Kitchen Staff"),
                            ("CLEANER", "Cleaning Staff"),
                        ],
                        max_length=20,
                    ),
                ),
                ("phone", models.CharField(max_length=20)),
                ("address", models.TextField()),
                ("emergency_contact", models.CharField(max_length=100)),
                ("emergency_phone", models.CharField(max_length=20)),
                ("date_hired", models.DateField()),
                (
                    "hourly_rate",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=6,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="employee_profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["user__last_name", "user__first_name"],
            },
        ),
        migrations.CreateModel(
            name="Leave",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "leave_type",
                    models.CharField(
                        choices=[
                            ("SICK", "Sick Leave"),
                            ("VACATION", "Vacation"),
                            ("PERSONAL", "Personal Leave"),
                            ("OTHER", "Other"),
                        ],
                        max_length=20,
                    ),
                ),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("reason", models.TextField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PENDING", "Pending"),
                            ("APPROVED", "Approved"),
                            ("REJECTED", "Rejected"),
                        ],
                        default="PENDING",
                        max_length=20,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "approved_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="approved_leaves",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="leaves",
                        to="staff.employee",
                    ),
                ),
            ],
            options={
                "ordering": ["-start_date"],
            },
        ),
        migrations.CreateModel(
            name="Schedule",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                (
                    "shift",
                    models.CharField(
                        choices=[
                            ("MORNING", "Morning Shift"),
                            ("AFTERNOON", "Afternoon Shift"),
                            ("EVENING", "Evening Shift"),
                            ("NIGHT", "Night Shift"),
                        ],
                        max_length=20,
                    ),
                ),
                ("start_time", models.TimeField()),
                ("end_time", models.TimeField()),
                ("notes", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="schedules",
                        to="staff.employee",
                    ),
                ),
            ],
            options={
                "ordering": ["date", "start_time"],
                "unique_together": {("employee", "date", "shift")},
            },
        ),
        migrations.CreateModel(
            name="Attendance",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("check_in", models.DateTimeField(blank=True, null=True)),
                ("check_out", models.DateTimeField(blank=True, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PRESENT", "Present"),
                            ("ABSENT", "Absent"),
                            ("LATE", "Late"),
                            ("LEAVE", "On Leave"),
                        ],
                        default="ABSENT",
                        max_length=20,
                    ),
                ),
                ("notes", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="attendance",
                        to="staff.employee",
                    ),
                ),
                (
                    "schedule",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="attendance_records",
                        to="staff.schedule",
                    ),
                ),
            ],
            options={
                "ordering": ["-schedule__date", "-check_in"],
                "unique_together": {("employee", "schedule")},
            },
        ),
    ]
