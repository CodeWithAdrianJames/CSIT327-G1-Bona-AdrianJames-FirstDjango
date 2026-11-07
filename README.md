# CSIT327 Lab Challenge: FirstDjango & User Profile

## Student Details

| | |
|---|---|
| **Full Name** | Adrian James F. Bona |
| **Course & Section** | CSIT327 (Information Management 2) — Section G1 |
| **Instructor** | Mr. Frederick L. Revilleza Jr. |

## Project Overview

**CampusConnect** is a small Django application with:

- **Authentication** — sign-up, log in and log out using a custom user model (`accounts.CustomUser`) with a `role` (Student / Instructor / Administrator) and a `course` field.
- **Profile management** — a login-protected profile page built on Django's class-based `UpdateView`. The edited object is always `request.user`, so a user can never open or edit another user's profile. Only `first_name`, `last_name`, `email` and `course` are editable.
- **Feedback** — success messages (account created, profile updated) are raised with Django's `messages` framework and shown as dismissible Bootstrap alerts.
- **Bootstrap 5 UI** — Bootstrap 5.3 is loaded from the jsDelivr **CDN** (no local Bootstrap files). Every page extends `templates/base.html`, which provides the shared responsive navbar, alert area and footer. All form inputs carry Bootstrap classes.

## Getting Started

1. **Clone the repository**

   ```bash
   git clone https://github.com/CodeWithAdrianJames/CSIT327-G1-Bona-AdrianJames-FirstDjango.git
   cd CSIT327-G1-Bona-AdrianJames-FirstDjango
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv .venv
   ```

   - Windows (PowerShell): `.venv\Scripts\Activate.ps1`
   - Windows (cmd): `.venv\Scripts\activate.bat`
   - macOS / Linux: `source .venv/bin/activate`

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the environment** — copy the example file and (optionally) set your own secret key.

   - Windows: `copy .env.example .env`
   - macOS / Linux: `cp .env.example .env`

5. **Apply database migrations**

   ```bash
   python manage.py migrate
   ```

6. **Run the development server**

   ```bash
   python manage.py runserver
   ```

   Open <http://127.0.0.1:8000/>.

Optional: `python manage.py createsuperuser` to create an admin account, and `python manage.py test` to run the test suite.

## Application Endpoints

| URL | Description |
|---|---|
| `/accounts/signup/` | Registration |
| `/accounts/login/` | Authentication |
| `/accounts/profile/` | Profile view and edit (requires login) |
| `/accounts/logout/` | Sign out (POST, via the navbar button) |
| `/` | Dashboard (requires login) |
| `/admin-panel/` | Role-restricted admin panel |
