from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from viewer.models import Contract, SubContract, Comment, User, Event
from django.db.models import Q
from datetime import date
from viewer.views.utils import User


class HomepageView(LoginRequiredMixin, TemplateView):
    """
    View for homepages, user must be logged in.
    Displays projects, subprojects, events and comments in relation to the currently logged in user.
    Only the 5 most recent items are displayed and only the current day's events.
    """
    template_name = 'base_and_homepage/homepage.html'

    def get_context_data(self, **kwargs):
        """
        Retrieves contextual data to be displayed on the home page.
        """
        contracts = Contract.objects.filter(user=self.request.user)
        subcontracts = SubContract.objects.filter(user=self.request.user)
        sorted_contracts = sorted(contracts, key=lambda contract: contract.delta())
        sorted_subcontracts = sorted(subcontracts, key=lambda subcontract: subcontract.delta)
        limited_subcontracts = sorted_subcontracts[:5]
        today = date.today()

        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.all().order_by('-created')[:5]
        context['users'] = User.objects.all()
        context['contracts'] = sorted_contracts
        context['subcontracts'] = limited_subcontracts

        context['events'] = Event.objects.filter(
            Q(start_time__date=today) |
            Q(end_time__date=today) |
            Q(start_time__date__lt=today, end_time__date__gt=today)
        ).order_by('start_time')
        return context