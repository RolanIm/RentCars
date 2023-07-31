from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (CreateView, UpdateView, DeleteView,
                                  ListView, DetailView)

from django.contrib.auth.mixins import LoginRequiredMixin

from ads.models import Ad


class OwnerAdView(View):
    """
    Subclass the View with overriding get method for searching and
    paginating ads.
    """

    template_name = reverse_lazy('ads:all')

    def get(self, request, ads_with_filter=None, statement=None):
        #  search
        str_val = request.GET.get('search', False)
        if str_val:
            if not statement:
                # multi-field search
                # __icontains for case-insensitive search
                q1 = Q(car__model_name__icontains=str_val)
                q2 = Q(car__make__name__icontains=str_val)
                q3 = Q(country__icontains=str_val)
                q4 = Q(city__icontains=str_val)
                q5 = Q(tags__name__in=[str_val])
                statement = q1 | q2 | q3 | q4 | q5
            # select_related() cashes query
            if ads_with_filter:
                query = ads_with_filter.filter(statement)
            else:
                query = Ad.objects.select_related().distinct().filter(statement)

        else:
            if ads_with_filter:
                query = ads_with_filter
            else:
                query = Ad.objects.all()

        #  shows up latest 10 ads on each page
        paginator = Paginator(query.order_by('-created_at'), 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        ctx = {'page_obj': page_obj}
        return render(request, self.template_name, ctx)


class OwnerListView(ListView):
    """
    Subclass the ListView to pass the request to the form.
    """


class OwnerDetailView(DetailView):
    """
    Subclass the DetailView to pass the request to the form.
    """


class OwnerCreateView(LoginRequiredMixin, CreateView):
    """
    Subclass of the CreateView to automatically pass the Request to the Form
    and add the owner to the saved object.
    """

    # Saves the form instance, sets the current object for the view,
    # and redirects to get_success_url().
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = self.request.user.owner
        obj.save()
        return super(OwnerCreateView, self).form_valid(form)


class OwnerUpdateView(LoginRequiredMixin, UpdateView):
    """
    Subclass the UpdateView to pass the request to the form and limit the
    queryset to the requesting user.
    """

    def get_queryset(self):
        """ Limit a User to only modifying their own data. """
        qs = super(OwnerUpdateView, self).get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerDeleteView(LoginRequiredMixin, DeleteView):
    """
    Subclass the DeleteView to restrict a User from deleting other
    user's data.
    """

    def get_queryset(self):
        qs = super(OwnerDeleteView, self).get_queryset()
        return qs.filter(owner=self.request.user)
