from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404, render

from viewer.forms import ContractForm, SearchForm
from viewer.models import Contract, Customer


class ContractView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    """
    View the details of a specific job.
    Access is limited to logged in users with the 'view_contract' permission.
    """
    model = Contract
    template_name = "detail_con_and_subcon/detail_contract.html"
    permission_required = 'viewer.view_contract'


class ContractCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    """
    View to create a new order.
    """
    template_name = 'forms/form.html'
    form_class = ContractForm
    success_url = reverse_lazy('navbar_contracts_all')
    permission_required = 'viewer.add_contract'

    def get_form_kwargs(self):
        """
        Ensures that a default customer is created if none already exists so that the database does not throw an error.
        """
        kwargs = super().get_form_kwargs()
        if Customer.objects.count() == 0:
            Customer.objects.create(first_name="John", last_name="Doe")
        return kwargs


class ContractUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = "forms/form.html"
    model = Contract
    form_class = ContractForm
    success_url = reverse_lazy("navbar_contracts_all")
    permission_required = 'viewer.change_contract'


class ContractDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    template_name = "forms/delete_confirmation.html"
    model = Contract
    permission_required = 'viewer.delete_contract'

    def post(self, request, *args, **kwargs):
        """
        A modification that will not allow the deletion of an order that has sub-orders.
        Args: request: HTTP request object
        Returns: redirects back to the page of all jobs, or display a warning message.
        """
        self.object = self.get_object()
        if self.object.subcontracts.exists():
            messages.warning(request, "Nemůžete smazat zakázku s aktivními podzakázkami.")
            return redirect('navbar_contracts_all')
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        """
        Specifies the forwarding address after a successful deletion, otherwise it reverts back to the default.
        """
        referer = self.request.POST.get('referer', None)
        if referer:
            return referer
        return reverse_lazy('navbar_contracts_all')

    def get_context_data(self, **kwargs):
        """
        Passes another context to the template and passes the current request to it.
        """
        context = super().get_context_data(**kwargs)
        context['request'] = self.request
        return context


class ContractListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    """
    View a list of jobs associated with the currently authenticated user.
    Only users with the 'view_contract' permission have access.
    Includes a search function that allows you to filter contracts by name.
    """
    model = Contract
    template_name = 'navbar/navbar_contracts.html'
    context_object_name = "contracts"
    permission_required = 'viewer.view_contract'

    def get_queryset(self):
        """
        Returns a filtered set of contract queries for the authenticated user and filters the contracts associated with
        the current user.
        """
        if self.request.user.is_authenticated:
            queryset = Contract.objects.filter(user=self.request.user)
            query = self.request.GET.get("query")
            if query:
                queryset = queryset.filter(contract_name__icontains=query)
            return sorted(queryset, key=lambda contract: contract.delta())
        return Contract.objects.none()

    def get_context_data(self, **kwargs):
        """
        Possibility to search in orders.
        """
        context = super().get_context_data(**kwargs)
        context["search_form"] = SearchForm()
        context["search_url"] = "navbar_contracts"
        context["show_search"] = True
        return context


class ContractAllListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    """
    View a list of all contracts regardless of the user.
    """
    model = Contract
    template_name = 'navbar/navbar_contracts_all.html'
    context_object_name = "contracts"
    permission_required = 'viewer.view_contract'

    def get_queryset(self):
        queryset = Contract.objects.all()
        query = self.request.GET.get("query")
        if query:
            queryset = queryset.filter(contract_name__icontains=query)
        return sorted(queryset, key=lambda contract: contract.delta())

    def get_context_data(self, **kwargs):
        """
        Possibility to search in orders.
        """
        context = super().get_context_data(**kwargs)
        context["search_form"] = SearchForm(self.request.GET or None)
        context["search_url"] = "navbar_contracts_all"
        context["show_search"] = True
        return context


@login_required
def contract_detail(request, contract_id):
    """
    Displays a detailed view of a specific job.
    """
    contract = get_object_or_404(Contract, id=contract_id)
    return render(request, 'deatil_con_and_subcon/detail_contract.html', {'contract': contract})