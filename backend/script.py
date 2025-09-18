# Script for manual role manipulation
# can be used in python manage.py shell, but will be converted to an executable file after running server but should be run manually
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from apps.Users.models import Program, Section, StudentProfile, StaffProfile, FacultyProfile, FacultyDepartment, Position
User = get_user_model()
import requests
from datetime import date

# Get a user
def get_user(identifier):
    # Fetch user by id, username, or email.
    # Returns User instance or None.
    if isinstance(identifier, int):
        return User.objects.filter(pk=identifier).first()
    if "@" in identifier:
        return User.objects.filter(email__iexact=identifier).first()
    return User.objects.filter(username__iexact=identifier).first() 
def assign_role(identifier, new_role):
    """Since roles are defaulted to student upon creation, use this method to change it.
    identifier - username
    new_role - new role to assign (e.g. admin, faculty)"""
    # Get user
    u = User.objects.get(username=identifier)
    # # Remove a role
    u.groups.remove(Group.objects.get(name="student"))
    # # Assign a role
    u.groups.add(Group.objects.get(name=new_role))
#==============================Start of Script==============================
admin = User.objects.create_superuser(
    username="admin",
    email="admin@cmu.edu.ph",
    password="admin123",
    first_name="System",
    last_name="Administrator",
    institutional_id="100100100",
    role_type="admin"
)
assign_role("admin", "admin")
user1 = User.objects.create_user(
    username="Adolf",
    email="adolfhitler@cmu.edu.ph",
    password="password123",
    first_name="Adolf",
    last_name="Hitler",
    institutional_id="456456456",
    role_type="student",
)
user2 = User.objects.create_user(
    username="Donald",
    email="donaldtrump@cmu.edu.ph",
    password="password123",
    first_name="Donald",
    last_name="Trump",
    institutional_id="123123123",
    role_type="staff",
)
assign_role("Donald", "staff")
user3 = User.objects.create_user(
    username="Kim",
    email="kimjongun@cmu.edu.ph",
    password="password123",
    first_name="Kim",
    last_name="Jong Un",
    institutional_id="789789789",
    role_type="faculty",
)
assign_role("Kim", "faculty")

#DEfault program and section, for example rani
prog, _ = Program.objects.get_or_create(program_name="BS IT")
sec, _  = Section.objects.get_or_create(section_name="IT-1A")
# Default Positions
pos1, _ =Position.objects.get_or_create(position_name="Instructor 1")
#Default Department
dep1, _ =FacultyDepartment.objects.get_or_create(department_name="CISC")

#then create a student profile
sp1 = StudentProfile.objects.create(
    user=user1,
    program=prog,
    section=sec,
    year_level=1,
    indiv_points=0,
)
# Create Staff(Registrar)
staff1= StaffProfile.objects.create(
    user=user2,
    faculty_department=dep1,
    job_title="registrar"
)
# Create faculty(Instructor 1)
Fac1= FacultyProfile.objects.create(
    user=user3,
    faculty_department=dep1,
    position= pos1,
    hire_date= date(2001, 9,11),
)

# Verify creation
for ident in ("Adolf", "Donald", "Kim"):
    u = get_user(ident)
    if u:
        print(f"Successfully created {u.get_username()} (id={u.id})")
    else:
        print(f"User {ident} not found")
#==============================End of Script==============================



# list(u.groups.values_list("name", flat=True))


# u = User.objects.get(username="Janmarc")

# # Assign a role
# u.groups.add(Group.objects.get(name="staff"))

# # Remove a role
# u.groups.remove(Group.objects.get(name="student"))

# # See roles
# list(u.groups.values_list("name", flat=True))

# Script for managing groups
# from django.contrib.auth.models import Group
# from apps.Users.models import Program, Section, StudentProfile
# Group.objects.get_or_create(name="org_officer")


# # Creation + promotion/demotion
# user = User.objects.create_user(
#     username="Adolf",
#     email="adolfhitler@cmu.edu.ph",
#     password="password123",
#     first_name="Adolf",
#     last_name="Hitler",
#     institutional_id="123123123",
#     role_type="student",
# )

# prog, _ = Program.objects.get_or_create(program_name="BS IT")
# sec, _  = Section.objects.get_or_create(section_name="IT-1A")

# sp = StudentProfile.objects.create(
#     user=user,
#     program=prog,
#     section=sec,
#     year_level=1,
#     indiv_points=0,
# )

# Methods (for shell, method is in views.py)

# def grant_org_officer(user):
#     group, _ = Group.objects.get_or_create(name="org_officer")
#     user.groups.add(group)\
    
# def revoke_org_officer(user):
#     group, _ = Group.objects.get_or_create(name="org_officer")
#     user.groups.remove(group)

# Check roles
# user.groups.values_list("name", flat=True)



# In-script methods only, already created api-callable methods from Users/view
# def promote_officer(self, user_id, token):
#     url = f"http://127.0.0.1:8000/api/roles/org-officer/{user_id}/promote/"
#     headers = {"Authorization": f"Bearer {token}"}
#     resp = requests.post(url, headers=headers, timeout=10)
#     return resp.json()

# def demote_officer(self, user_id, token):
#     url = f"http://127.0.0.1:8000/api/roles/org-officer/{user_id}/demote/"
#     headers = {"Authorization": f"Bearer {token}"}
#     resp = requests.post(url, headers=headers, timeout=10)
#     return resp.json()