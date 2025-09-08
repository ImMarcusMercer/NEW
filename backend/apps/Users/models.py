from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

# ID are auto generate by Django
class FacultyDepartment(models.Model):
    department_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.department_name

class Position(models.Model):
    position_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.position_name

class Program(models.Model):
    program_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.program_name

class Section(models.Model):
    section_name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.section_name
    
class BaseUser(AbstractUser):
    """Custom model that would inherit and extend the AbstractBaseUser"""
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    suffix = models.CharField(max_length=5, blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    institutional_id = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("student", "Student"),
        ("faculty", "Faculty"),
        ("staff", "Staff"),
    ]
    role_type = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True, null=True)

class FacultyProfile(models.Model):
    user               = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="faculty_profile")
    faculty_department = models.ForeignKey(FacultyDepartment, on_delete=models.SET_NULL, null=True)
    position           = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True)
    hire_date          = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"FacultyProfile<{self.user_id}>"
    

class StudentProfile(models.Model):
    user         = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="student_profile")
    program      = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True)
    section      = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True)
    indiv_points = models.IntegerField(default=0)
    year_level   = models.IntegerField()

    def __str__(self):
        return f"StudentProfile<{self.user_id}>"


class StaffProfile(models.Model):
    user               = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="staff_profile")
    faculty_department = models.ForeignKey(FacultyDepartment, on_delete=models.SET_NULL, null=True)
    job_title          = models.CharField(max_length=50)

    def __str__(self):
        return f"StaffProfile<{self.user_id}>"


# Organiztional Models / for subroles (Proposed approach)
class Organization(models.Model):
    name        = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    adviser     = models.ForeignKey("FacultyProfile", on_delete=models.SET_NULL, null=True, blank=True)

class OrgMembership(models.Model):
    """sample membership model (change if needed)"""
    ROLE_CHOICES = [
        ("member",  "Member"),
        ("officer", "Officer"),
        ("pres",    "President"),
        ("vp",      "Vice President"),
        ("sec",     "Secretary"),
        ("treas",   "Treasurer"),
    ]
    student      = models.ForeignKey("StudentProfile", on_delete=models.CASCADE, related_name="org_memberships")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="memberships")
    role         = models.CharField(max_length=16, choices=ROLE_CHOICES, default="member")
    position_title = models.CharField(max_length=80, blank=True)
    start_date   = models.DateField(null=True, blank=True)
    end_date     = models.DateField(null=True, blank=True)
    is_active    = models.BooleanField(default=True)


    # no two rows in the table can have the same values for all those fields at once.
    # ensure no duplicate role with the same student
    class Meta:
        unique_together = [("student", "organization", "role", "is_active")]

@property
def is_org_officer(self):
    return self.org_memberships.filter(is_active=True).exclude(role="member").exists()
