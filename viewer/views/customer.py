from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from viewer.forms import SearchForm, CustomerForm
from viewer.models import Customer


class CustomerView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    """
    View the list of customers.
    """
    model = Customer
    template_name = 'navbar/navbar_customers.html'
    context_object_name = "customers"
    permission_required = 'viewer.view_customer'

    def get_queryset(self):
        """
        Gets a filtered list of customers based on a search query.
        """
        queryset = super().get_queryset()
        query = self.request.GET.get("query")
        if query:
            queryset = queryset.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        """
        Adds a search form and related context to the template.
        """
        context = super().get_context_data(**kwargs)
        context["search_form"] = SearchForm()
        context["search_url"] = "navbar_customers"
        context["show_search"] = True
        return context


class CustomerCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    """
    Creating a new customer.
    """
    template_name = 'forms/form.html'
    form_class = CustomerForm
    success_url = reverse_lazy('navbar_customers')
    permission_required = 'viewer.add_customer'


class CustomerUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = 'forms/form.html'
    model = Customer
    form_class = CustomerForm
    success_url = reverse_lazy('navbar_customers')
    permission_required = 'viewer.change_customer'


class CustomerDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    template_name = 'forms/delete_confirmation.html'
    model = Customer
    permission_required = 'viewer.delete_customer'

    def get_success_url(self):
        referer = self.request.POST.get('referer', None)
        if referer:
            return referer
        return reverse_lazy('navbar_customers')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request'] = self.request
        return context