# Script for manual role manipulation
# used in python manage.py shell

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()
u = User.objects.get(username="Janmarc")

# Assign a role
u.groups.add(Group.objects.get(name="staff"))

# Remove a role
u.groups.remove(Group.objects.get(name="student"))

# See roles
list(u.groups.values_list("name", flat=True))

# Script for managing groups
from django.contrib.auth.models import Group
Group.objects.get_or_create(name="org_officer")


# Creation + promotion/demotion

from django.contrib.auth import get_user_model
User = get_user_model()

user = User.objects.create_user(
    username="s2025",
    email="s2025@cmu.edu.ph",
    password="testpass123",
    first_name="Sam",
    last_name="Delos Reyes",
    institutional_id="CMU-25-0002",
    role_type="student",
)
from apps.Users.models import Program, Section, StudentProfile

prog, _ = Program.objects.get_or_create(program_name="BS IT")
sec, _  = Section.objects.get_or_create(section_name="IT-1A")

sp = StudentProfile.objects.create(
    user=user,
    program=prog,
    section=sec,
    year_level=1,
    indiv_points=0,
)

# Methods
from django.contrib.auth.models import Group

def grant_org_officer(user):
    group, _ = Group.objects.get_or_create(name="org_officer")
    user.groups.add(group)\
    
def revoke_org_officer(user):
    group, _ = Group.objects.get_or_create(name="org_officer")
    user.groups.remove(group)

# Check roles
user.groups.values_list("name", flat=True)