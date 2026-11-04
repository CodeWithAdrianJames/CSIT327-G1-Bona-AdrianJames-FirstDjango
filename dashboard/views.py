from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView

from accounts.models import CustomUser


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['member_count'] = CustomUser.objects.count()
        context['is_admin'] = (self.request.user.role == CustomUser.Role.ADMIN)
        return context


class AdminPanelView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'dashboard/admin_panel.html'

    def test_func(self):
        return self.request.user.role == CustomUser.Role.ADMIN
