from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from viewer.forms import CommentForm
from viewer.models import Comment, SubContract


class CommentListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    """
    View the last five comments, sorted in descending order from the most recent.
    """
    model = Comment
    template_name = "homepages/comments_homepage.html"
    permission_required = 'viewer.view_comment'
    context_object_name = 'comments'

    def get_queryset(self):
        queryset = Comment.objects.all().order_by('-created')[:5]
        return queryset


class CommentCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    template_name = "forms/form.html"
    form_class = CommentForm
    permission_required = 'viewer.add_comment'

    def form_valid(self, form):
        """
        Assigns a comment to a subquery.
        """
        new_comment = form.save(commit=False)
        new_comment.subcontract = SubContract.objects.get(pk=int(self.kwargs["pk"]))
        new_comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        subcontract = SubContract.objects.get(pk=int(self.kwargs["pk"]))
        contract_id = subcontract.contract.pk
        return reverse_lazy('subcontract_detail', kwargs={'contract_pk': contract_id, "subcontract_number": subcontract.subcontract_number})
