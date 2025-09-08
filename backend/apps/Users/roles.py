# backend/apps/Users/roles.py
from django.contrib.auth.models import Group

ROLES = [
    "student",
    "org_officer",
    "faculty",
    "staff",
    "admin",
]

def ensure_roles():
    for name in ROLES:
        Group.objects.get_or_create(name=name)
