from django.test import TestCase
from django.urls import reverse

from .models import CustomUser


class ProfileUpdateViewTests(TestCase):
    def setUp(self):
        self.url = reverse("profile")
        self.user = CustomUser.objects.create_user(
            username="student1", password="pass12345!", email="s1@example.com",
            first_name="Stu", last_name="Dent", course="BSCS",
        )
        self.other = CustomUser.objects.create_user(
            username="student2", password="pass12345!", email="taken@example.com",
        )

    def test_anonymous_user_is_redirected_to_login(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f"{reverse('login')}?next={self.url}")

    def test_user_can_update_own_profile(self):
        self.client.login(username="student1", password="pass12345!")
        response = self.client.post(self.url, {
            "first_name": "New", "last_name": "Name",
            "email": "new@example.com", "course": "BSIT",
        }, follow=True)
        self.assertRedirects(response, reverse("dashboard"))
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "New")
        self.assertEqual(self.user.email, "new@example.com")
        self.assertEqual(self.user.course, "BSIT")
        self.assertContains(response, "Your profile has been updated successfully!")

    def test_restricted_fields_cannot_be_modified(self):
        self.client.login(username="student1", password="pass12345!")
        self.client.post(self.url, {
            "first_name": "Stu", "last_name": "Dent", "email": "s1@example.com",
            "course": "BSCS", "role": CustomUser.Role.ADMIN,
            "is_staff": "on", "is_superuser": "on", "username": "hacker",
        })
        self.user.refresh_from_db()
        self.assertEqual(self.user.role, CustomUser.Role.STUDENT)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
        self.assertEqual(self.user.username, "student1")

    def test_duplicate_email_is_rejected_case_insensitively(self):
        self.client.login(username="student1", password="pass12345!")
        response = self.client.post(self.url, {
            "first_name": "Stu", "last_name": "Dent",
            "email": "TAKEN@example.com", "course": "BSCS",
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "already in use")
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "s1@example.com")

    def test_user_cannot_modify_another_users_profile(self):
        """User A's requests never touch User B, even if B's identifiers are supplied."""
        self.client.login(username="student1", password="pass12345!")
        other_before = CustomUser.objects.get(pk=self.other.pk)

        # Extra pk/id/username fields and a pk in the query string must be ignored.
        response = self.client.post(f"{self.url}?pk={self.other.pk}", {
            "pk": self.other.pk, "id": self.other.pk, "username": "student2",
            "first_name": "Hijacked", "last_name": "Hijacked",
            "email": "hijack@example.com", "course": "HACK",
        })
        self.assertRedirects(response, reverse("dashboard"))

        self.other.refresh_from_db()
        self.assertEqual(self.other.first_name, other_before.first_name)
        self.assertEqual(self.other.last_name, other_before.last_name)
        self.assertEqual(self.other.email, "taken@example.com")
        self.assertEqual(self.other.course, other_before.course)

        # The edits landed on the logged-in user (A) only.
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Hijacked")
        self.assertEqual(self.user.username, "student1")

    def test_profile_form_shows_only_own_data(self):
        self.client.login(username="student1", password="pass12345!")
        response = self.client.get(self.url)
        self.assertEqual(response.context["form"].instance.pk, self.user.pk)
        self.assertNotContains(response, "taken@example.com")

    def test_own_email_can_be_resubmitted(self):
        self.client.login(username="student1", password="pass12345!")
        response = self.client.post(self.url, {
            "first_name": "Stu", "last_name": "Dent",
            "email": "S1@example.com", "course": "BSCS",
        })
        self.assertRedirects(response, reverse("dashboard"))


class SignUpMessageTests(TestCase):
    def test_signup_shows_success_message(self):
        response = self.client.post(reverse("signup"), {
            "username": "newbie", "email": "n@example.com",
            "first_name": "N", "last_name": "B", "course": "BSCS",
            "password1": "Str0ngPass!234", "password2": "Str0ngPass!234",
        }, follow=True)
        self.assertRedirects(response, reverse("login"))
        self.assertContains(response, "Account created successfully! Please log in.")
        self.assertContains(response, "alert alert-success")
        self.assertEqual(CustomUser.objects.get(username="newbie").role, CustomUser.Role.STUDENT)

    def test_signup_rejects_duplicate_email_case_insensitively(self):
        CustomUser.objects.create_user(username="existing", password="x", email="dup@example.com")
        response = self.client.post(reverse("signup"), {
            "username": "newbie2", "email": "DUP@example.com",
            "first_name": "N", "last_name": "B", "course": "BSCS",
            "password1": "Str0ngPass!234", "password2": "Str0ngPass!234",
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "already in use")
        self.assertFalse(CustomUser.objects.filter(username="newbie2").exists())


class BootstrapFormMixinTests(TestCase):
    def test_widget_types_get_matching_bootstrap_classes(self):
        from django import forms

        from .forms import BootstrapFormMixin

        class DemoForm(BootstrapFormMixin, forms.Form):
            text = forms.CharField()
            choice = forms.ChoiceField(choices=[("a", "A")])
            agree = forms.BooleanField()

        form = DemoForm()
        self.assertIn("form-control", form.fields["text"].widget.attrs["class"])
        self.assertIn("form-select", form.fields["choice"].widget.attrs["class"])
        self.assertIn("form-check-input", form.fields["agree"].widget.attrs["class"])
