
from celery import shared_task
from django.utils.timezone import now
from .models import Task
from django.core.cache import cache

@shared_task
def activate_scheduled_tasks():
    current_time = now()  # This includes date and time
    scheduled_tasks = Task.objects.filter(
        status="Scheduled",
        scheduled_date__lte=current_time  # Compare datetime, not just date
    )

    if scheduled_tasks:
        for task in scheduled_tasks:
            task.status = "Ongoing"
            task.save()

        return f"Updated {len(scheduled_tasks)} tasks to Ongoing"
    return "No tasks to update"

from celery import shared_task
from django.core.cache import cache
from .models import Task
from django.utils.timezone import now

@shared_task
def refresh_task_cache(user_id):
    today = now()
    ongoing_tasks = Task.objects.filter(user_id=user_id, status="Ongoing").order_by('-id')
    completed_tasks = Task.objects.filter(user_id=user_id, status="Completed").order_by('-id')
    scheduled_tasks = Task.objects.filter(user_id=user_id, status="Scheduled", scheduled_date__gte=today)

    cache.set(f"ongoing_tasks_{user_id}", ongoing_tasks, timeout=None)
    cache.set(f"completed_tasks_{user_id}", completed_tasks, timeout=None)
    cache.set(f"scheduled_tasks_{user_id}", scheduled_tasks, timeout=None)

    return "Cache refreshed successfully."

# tasks.py in your_app_name

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from task.models import Task
from django.contrib.auth.models import User
from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth.models import User
from task.models import Task  # Adjust the model import based on your structure

@shared_task
def send_weekly_report():
    for user in User.objects.all():
        # Fetch tasks for the user
        ongoing_tasks = Task.objects.filter(user=user, status='Ongoing')
        completed_tasks = Task.objects.filter(user=user, status='Completed')

        if ongoing_tasks.exists() or completed_tasks.exists():
            # Format email content
            subject = "Your Task Summary"
            message = f"Hello {user.username},\n\nHere is your task summary:\n\n"

            if ongoing_tasks.exists():
                message += "Ongoing Tasks:\n"
                for task in ongoing_tasks:
                    message += f"- {task.title}\n"

            if completed_tasks.exists():
                message += "\nCompleted Tasks:\n"
                for task in completed_tasks:
                    message += f"- {task.title}\n"


            message += "\nBest regards,\nYour Team"

            # Send email
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=True,
            )

    return 'Mail Sent Successfully.'



@shared_task
def add(x, y):
    return x + y