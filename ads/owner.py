from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.views import View
from django.views.generic import (CreateView, UpdateView, DeleteView,
                                  ListView, DetailView)

from django.contrib.auth.mixins import LoginRequiredMixin

from ads.models import Ad


class OwnerAdView(View):
    """
    Subclass of the View with overriding get method for searching and
    paginating ads.
    """

    template_name = 'ads/ad_list.html'

    def get(self, request, ads=None, ctx=None, empty_profile=False):
        query = page_obj = None

        if not empty_profile:
            #  search
            str_val = request.GET.get('search', False)
            if str_val:
                # multi-field search
                # __icontains for case-insensitive search
                q1 = Q(car__model_name__icontains=str_val)
                q2 = Q(car__make__name__icontains=str_val)
                q3 = Q(country__icontains=str_val)
                q4 = Q(city__icontains=str_val)
                q5 = Q(tags__name__in=[str_val])
                q6 = Q(price_per__icontains=str_val)
                statement = q1 | q2 | q3 | q4 | q5 | q6
                if ads:
                    query = ads.filter(statement)
                else:
                    # select_related() cashes query
                    ads = Ad.objects.select_related().distinct()
                    query = ads.filter(statement)
            else:
                if ads:
                    query = ads
                else:
                    query = Ad.objects.all().select_related().distinct()

            #  shows up latest 12 ads on each page
            paginator = Paginator(query.order_by('-created_at'), 12)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

        if page_obj:
            if ctx and query:
                ctx['page_obj'] = page_obj
            else:
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
