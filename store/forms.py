from django import forms
from django.contrib.auth.models import User
from .models import Profile


class RegistrationForm(forms.ModelForm):
    name = forms.CharField(required=True)
    age = forms.IntegerField(required=True, min_value=1, max_value=120)
    
    gender = forms.ChoiceField(
        choices=Profile.GENDER_CHOICES,
        required=False
    )

    
    email = forms.EmailField(required=True)

    password = forms.CharField(
        widget=forms.PasswordInput
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        user.email = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()

            profile = user.profile
            profile.name = self.cleaned_data["name"]
            profile.age = self.cleaned_data["age"]
            profile.gender = self.cleaned_data["gender"]
            profile.save()

        return user