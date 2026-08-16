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

    def save(self, commit=True):
        user = super().save(commit=commit)
        organization = self.cleaned_data.get('organization')
        is_manager = self.cleaned_data.get('is_manager')

        # Create UserInfo
        user_info = UserInfo.objects.create(
            user=user,
            is_manager=is_manager,
            organization=organization
        )

        # Create EmployeeInfo only if user is NOT a manager
        if not is_manager:
            EmployeeInfo.objects.create(user=user, remaining_leave=24)

        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)