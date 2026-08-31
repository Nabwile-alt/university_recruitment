from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, StudentProfile, EmployerProfile, UniversityStaffProfile
from universities.models import University, Department


class StudentRegistrationForm(UserCreationForm):
    university = forms.ModelChoiceField(queryset=University.objects.all(), required=False)
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False)
    graduation_year = forms.IntegerField(required=False, min_value=2000, max_value=2040)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'student'
        if commit:
            user.save()
            StudentProfile.objects.create(
                user=user,
                university=self.cleaned_data.get('university'),
                department=self.cleaned_data.get('department'),
                graduation_year=self.cleaned_data.get('graduation_year'),
            )
        return user


class EmployerRegistrationForm(UserCreationForm):
    company_name = forms.CharField(max_length=200)
    company_website = forms.URLField(required=False)
    contact_phone = forms.CharField(max_length=20, required=False)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'employer'
        if commit:
            user.save()
            EmployerProfile.objects.create(
                user=user,
                company_name=self.cleaned_data.get('company_name'),
                company_website=self.cleaned_data.get('company_website', ''),
                contact_phone=self.cleaned_data.get('contact_phone', ''),
            )
        return user


class StaffRegistrationForm(UserCreationForm):
    university = forms.ModelChoiceField(queryset=University.objects.all())
    employee_id = forms.CharField(max_length=50)
    position = forms.CharField(max_length=100, required=False)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'university_staff'
        if commit:
            user.save()
            UniversityStaffProfile.objects.create(
                user=user,
                university=self.cleaned_data.get('university'),
                employee_id=self.cleaned_data.get('employee_id'),
                position=self.cleaned_data.get('position', ''),
            )
        return user


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['university', 'department', 'graduation_year', 'resume', 'bio', 'phone', 'linkedin']


class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = EmployerProfile
        fields = ['company_name', 'company_website', 'company_description', 'contact_phone', 'contact_address', 'company_logo']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']
