from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import CustomUser


class BootstrapFormMixin:
    """Apply Bootstrap 5 control classes to every widget."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = "form-control"
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing} {css}".strip()


class BootstrapAuthenticationForm(BootstrapFormMixin, AuthenticationForm):
    pass


class CustomUserCreationForm(BootstrapFormMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "email", "first_name", "last_name", "course")


class ProfileUpdateForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "email", "course")

    def clean_email(self):
        email = self.cleaned_data["email"]
        if email:
            taken = CustomUser.objects.filter(email__iexact=email).exclude(pk=self.instance.pk)
            if taken.exists():
                raise forms.ValidationError("This email address is already in use.")
        return email
