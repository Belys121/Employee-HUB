from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, FormView

from viewer.forms import SearchForm, SubContractForm
from viewer.models import SubContract, Contract


class SubContractAllListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    """
    This view loads and displays a list of all sub-deliveries.
    It supports filtering by subcontract name or parent contract.
    The results are ranked according to their own method (delta).
    """
    model = SubContract
    template_name = 'navbar/navbar_subcontracts.html'
    context_object_name = 'subcontracts'
    permission_required = 'viewer.view_subcontract'

    def get_queryset(self):
        queryset = SubContract.objects.all()
        query = self.request.GET.get("query")
        if query:
            queryset = queryset.filter(
                Q(subcontract_name__icontains=query) |
                Q(contract__contract_name__icontains=query)
            )
        sorted_queryset = sorted(queryset, key=lambda subcontract: subcontract.delta)
        return sorted_queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = SearchForm(self.request.GET or None)
        context["search_url"] = "navbar_subcontracts"
        context["show_search"] = True
        return context


class SubContractView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = SubContract
    template_name = 'homepages/subcontracts_homepage.html'
    permission_required = 'viewer.view_subcontract'


class SubContractCreateView(PermissionRequiredMixin, LoginRequiredMixin, FormView):
    template_name = 'forms/form.html'
    form_class = SubContractForm
    permission_required = 'viewer.add_subcontract'

    def form_valid(self, form):
        new_sub_contract = form.save(commit=False)
        new_sub_contract.contract = get_object_or_404(Contract, pk=int(self.kwargs["param"]))
        new_sub_contract.subcontract_number = SubContract.get_next_subcontract_number(new_sub_contract.contract)
        new_sub_contract.save()
        messages.success(self.request, 'Podzakázka byla úspěšně vytvořena.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('contract_detail', kwargs={'pk': self.kwargs['param']})


class SubContractUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = "forms/form.html"
    model = SubContract
    form_class = SubContractForm
    permission_required = 'viewer.change_subcontract'

    def get_object(self):
        """
        Finds a subcontract object based on the primary contract key and subcontract number specified in the URL.
        """
        contract_pk = self.kwargs.get("contract_pk")
        subcontract_number = self.kwargs.get("subcontract_number")
        return SubContract.objects.get(contract__pk=contract_pk, subcontract_number=subcontract_number)

    def get_success_url(self):
        """
        Defines the URL to redirect to after a successful update. Works with the job id and the custom subjob number.
        """
        return reverse_lazy('contract_detail', kwargs={'pk': self.kwargs['contract_pk']})


class SubContractDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    template_name = "forms/delete_confirmation.html"
    model = SubContract
    permission_required = 'viewer.delete_subcontract'

    def get_success_url(self):
        referer = self.request.POST.get('referer', None)
        if referer:
            return referer
        contract_id = self.object.contract.id
        return reverse_lazy('contract_detail', kwargs={'pk': contract_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request'] = self.request
        return context


class SubContractDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    """
    View sub-order details.
    """
    template_name = "detail_con_and_subcon/detail_subcontract.html"
    model = SubContract
    permission_required = 'viewer.view_subcontract'

    def get_object(self):
        contract_pk = self.kwargs.get("contract_pk")
        subcontract_number = self.kwargs.get("subcontract_number")
        return SubContract.objects.get(contract__pk=contract_pk, subcontract_number=subcontract_number)


@login_required
def show_subcontracts(request):
    """
    This function displays the sub-bids. The sub-orders are sorted based on the delta() method of the related order.
    """
    query = request.GET.get("query", "")
    subcontracts = SubContract.objects.filter(user=request.user)
    if query:
        subcontracts = subcontracts.filter(
            Q(subcontract_name__icontains=query)
        )
    sorted_subcontracts = sorted(subcontracts, key=lambda subcontract: subcontract.contract.delta())
    search_form = SearchForm(initial={'query': query})
    search_url = 'navbar_show_subcontracts'
    show_search = True

    return render(request, 'other/subcontract.html', {
        'subcontracts': sorted_subcontracts,
        'search_form': search_form,
        'search_url': search_url,
        'show_search': show_search,
    })


@login_required
def subcontract_detail(request, subcontract_id):
    """
    This function searches for a subcontract and its parent contract based on the specified subcontract_id.
    If the subcontract does not exist, a 404 error is displayed.
    """
    subcontract = get_object_or_404(SubContract, pk=subcontract_id)
    contract = subcontract.contract
    return render(request, 'detail_con_and_subcon/detail_subcontract.html',{'subcontract': subcontract, 'contract': contract})
