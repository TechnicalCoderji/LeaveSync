from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, UserInfo
from app.models import EmployeeInfo

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    name = forms.CharField(max_length=150)
    organization = forms.CharField(max_length=255)
    is_manager = forms.BooleanField(required=False, label="Register as Manager")

    class Meta:
        model = CustomUser
        fields = ['name', 'username', 'email', 'organization', 'is_manager', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

    def clean(self):
        cleaned_data = super().clean()
        organization = cleaned_data.get('organization')
        is_manager = cleaned_data.get('is_manager', False)

        if organization:
            # Case-insensitive check if organization already exists in UserInfo
            org_exists = UserInfo.objects.filter(organization__iexact=organization).exists()

            if is_manager:
                # Manager CANNOT use an existing organization name
                if org_exists:
                    self.add_error(
                        'organization', 
                        "This organization already exists. Choose a different name or contact your admin."
                    )
            else:
                # Employee CAN ONLY register under an existing organization
                if not org_exists:
                    self.add_error(
                        'organization', 
                        "This organization does not exist. An employee can only join an existing organization."
                    )

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.name = self.cleaned_data.get('name')
        user.email = self.cleaned_data.get('email')
        
        if commit:
            user.save()
            organization = self.cleaned_data.get('organization')
            is_manager = self.cleaned_data.get('is_manager', False)

            # Create UserInfo
            UserInfo.objects.create(
                user=user,
                is_manager=is_manager,
                organization=organization
            )

            # Create EmployeeInfo only if user is an Employee
            if not is_manager:
                EmployeeInfo.objects.create(user=user, remaining_leave=24)

        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)