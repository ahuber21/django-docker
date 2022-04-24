from logging import getLogger

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import TemplateView

log = getLogger("fingerprints")


class EnrollView(PermissionRequiredMixin, TemplateView):
    permission_required = "is_staff"
    template_name = "enroll_index.html"
