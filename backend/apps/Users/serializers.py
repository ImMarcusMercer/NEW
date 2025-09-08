from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import BaseUser

# serializers.py
from rest_framework import serializers
from django.conf import settings
from .models import (
    BaseUser, FacultyDepartment, Position, Program, Section,
    FacultyProfile, StudentProfile, StaffProfile
)
User=get_user_model()

class FacultyDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacultyDepartment
        fields = ["id", "department_name"]

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ["id", "position_name"]

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ["id", "program_name"]

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ["id", "section_name"]

class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = [
            "id", "username", "email",
            "first_name", "middle_name", "last_name", "suffix",
            "profile_picture", "birth_date",
            "institutional_id", "phone_number",
            "role_type",
        ]
        read_only_fields = ["id", "institutional_id", "username", "email"]

class FacultyProfileSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=BaseUser.objects.all(),
        write_only=True,
        source="user"
    )
    faculty_department_detail = FacultyDepartmentSerializer(source="faculty_department", read_only=True)
    position_detail = PositionSerializer(source="position", read_only=True)

    class Meta:
        model = FacultyProfile
        fields = [
            "user", "user_id",
            "faculty_department", "faculty_department_detail",
            "position", "position_detail",
            "hire_date",
        ]


class StudentProfileSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=BaseUser.objects.all(),
        write_only=True,
        source="user"
    )
    program_detail = ProgramSerializer(source="program", read_only=True)
    section_detail = SectionSerializer(source="section", read_only=True)

    class Meta:
        model = StudentProfile
        fields = [
            "user", "user_id",
            "program", "program_detail",
            "section", "section_detail",
            "indiv_points", "year_level",
        ]


class StaffProfileSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=BaseUser.objects.all(),
        write_only=True,
        source="user"
    )
    faculty_department_detail = FacultyDepartmentSerializer(source="faculty_department", read_only=True)

    class Meta:
        model = StaffProfile
        fields = [
            "user", "user_id",
            "faculty_department", "faculty_department_detail",
            "job_title",
        ]
        
class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField(write_only=True)
    def validate(self, attrs):
        identifier = attrs.get("identifier")
        password = attrs.get("password")
        user = authenticate(username=identifier, password=password)

        if user is None and "@" in identifier:
            try:
                u = User.objects.get(email__iexact=identifier)
                user = authenticate(username=u.username, password=password)
            except User.DoesNotExist:
                pass

        if user is None:
            raise serializers.ValidationError("Invalid credentials.")
        if not user.is_active:
            raise serializers.ValidationError("Account is inactive.")

        refresh = RefreshToken.for_user(user)
        roles = list(user.groups.values_list("name", flat=True))
        if hasattr(user, "student_profile") and user.student_profile.is_org_officer:
            roles.append("org_officer")

        # Implement custom permissions
        role_priority = ["admin","faculty","staff","student"]
        primary_role = next((r for r in role_priority if r in roles), None)

        return {
            "user": user,
            "access_token": str(refresh.access_token),
            "roles": roles,
            "primary_role": primary_role,
        }
    


# Serializers for Organizxation models
from rest_framework import serializers
from .models import Organization, OrgMembership

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["id", "name", "description", "adviser"]


class OrgMembershipSerializer(serializers.ModelSerializer):
    organization_detail = OrganizationSerializer(source="organization", read_only=True)

    class Meta:
        model = OrgMembership
        fields = [
            "id", "student", "organization", "organization_detail",
            "role", "position_title",
            "start_date", "end_date", "is_active"
        ]
