from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import ListView

from viewer.views.utils import User
from viewer.forms import SearchForm


class UserListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = User
    template_name = 'navbar/employees.html'
    context_object_name = "employees"
    permission_required = 'auth.view_user'

    def get_queryset(self):
        """
        Based on the search query, it retrieves a fltrated list of users.
        """
        queryset = super().get_queryset()
        query = self.request.GET.get("query")
        if query:
            queryset = queryset.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(username__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        """
        Adds a search form and additional context to the template.
        """
        context = super().get_context_data(**kwargs)
        context["search_form"] = SearchForm()
        context["search_url"] = "employees"
        context["show_search"] = True
        return context