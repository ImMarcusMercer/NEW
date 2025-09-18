# backend/apps/Users/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

DEFAULT_ROLE = "student"

@receiver(post_save, sender=User)
def assign_default_role(sender, instance, created, **kwargs):
    if not created:
        return

    # Never auto-assign for superusers/admin staff
    if instance.is_superuser or instance.is_staff:
        return

    # If user already has any group, do nothing
    if instance.groups.exists():
        return

    # Only auto-assign 'student' when role_type explicitly says so
    if getattr(instance, "role_type", None) == "student":
        student_group, _ = Group.objects.get_or_create(name="student")
        instance.groups.add(student_group)
    # if not created:
    #     return
    # try:
    #     group = Group.objects.get(name=DEFAULT_ROLE)
    #     instance.groups.add(group)
    # except Group.DoesNotExist:
    #     # If roles weren’t created yet, silently ignore
    #     # (or you can import ensure_roles() and create them here)
    #     pass
