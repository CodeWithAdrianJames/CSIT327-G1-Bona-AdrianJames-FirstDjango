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
        self.assertContains(response, "profile was updated")

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
        self.assertContains(response, "Account created successfully! You can now log in.")
        self.assertEqual(CustomUser.objects.get(username="newbie").role, CustomUser.Role.STUDENT)
