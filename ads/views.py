from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db.utils import IntegrityError
from django.urls import reverse_lazy, reverse
from django.views import View

from .models import Ad, Comment, Fav
from .owner import (OwnerDeleteView,
                    OwnerDetailView, OwnerAdView)
from .forms import MakeForm, AdForm, CarForm, CommentForm

import random


class AdListView(OwnerAdView):
    """
    View for showing all ads on the main page.
    """

    def get(self, request, *args, **kwargs):
        # select_related() cashes query
        all_ads = Ad.objects.all().select_related().distinct()
        return super().get(request, ads=all_ads)


class AdDetailView(OwnerDetailView):
    """
    View for showing detail page of ads.
    """

    def get(self, request, *args, **kwargs):
        if args:
            pk = args[0]
        else:
            pk = kwargs.get('pk')
        x = get_object_or_404(Ad, id=pk)
        # comments current ad
        comments_filtered = Comment.objects.filter(ad=x)
        comments = comments_filtered.order_by('-updated_at')
        comment_form = CommentForm()

        favorites = list()
        if request.user.is_authenticated:
            # rows = [{'id': 2}, {'id': 4} ... ]  (A list of rows)
            rows = request.user.favorite_ads.values('id')
            # favorites = [2, 4, ...] using list comprehension
            favorites = [row['id'] for row in rows]

        # colors list for random tag color.
        colors = ['primary', 'success', 'danger', 'warning', 'dark', 'info']
        tags_with_colors = []
        tags = x.tags.all()
        # tags_with_colors is [(tag, color), ...]
        for i in range(len(tags)):
            if i < len(colors):
                color = colors[i]
            else:
                color = random.choice(colors)
            tags_with_colors.append((tags[i], color))

        ctx = {
            'ad': x,
            'favorites': favorites,
            'colors': colors,
            'comments': comments,
            'form': comment_form,
            'tags_with_colors': tags_with_colors
        }
        return render(request, 'ads/ad_detail.html', ctx)


class AdCreateView(LoginRequiredMixin, View):
    """
    View for creating ads.
    """

    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:all')

    def get(self, request):
        ad_form = AdForm()
        car_form = CarForm()
        make_form = MakeForm()
        forms = [ad_form, make_form, car_form]
        ctx = {
            'forms': forms
        }
        return render(request, self.template_name, ctx)

    def post(self, request):
        make_form = MakeForm(request.POST or None)
        car_form = CarForm(request.POST or None)
        ad_form = AdForm(request.POST, request.FILES or None)

        statement = (
                ad_form.is_valid()
                and car_form.is_valid()
                and make_form.is_valid()
        )
        if not statement:
            forms = [ad_form, make_form, car_form]
            ctx = {
                'forms': forms
            }
            return render(request, self.template_name, ctx)

        # Add make to the model Car before saving
        car = car_form.save(commit=False)
        make = make_form.save()
        car.make = make
        car.save()
        # Add owner and phone number to the model Ad before saving
        ad = ad_form.save(commit=False)
        ad.owner = self.request.user
        ad.car = car
        ad.save()
        ad_form.save()
        return redirect(self.success_url)


class AdUpdateView(LoginRequiredMixin, View):
    """
    View for updating information about an ad.
    """

    template_name = 'ads/ad_form.html'

    def get(self, request, pk):
        ad = get_object_or_404(Ad, id=pk, owner=self.request.user)
        ad_form = AdForm(instance=ad)
        car_form = CarForm(instance=ad.car)
        make_form = MakeForm(instance=ad.car.make)
        forms = [ad_form, make_form, car_form]
        ctx = {
            'forms': forms,
            'is_edit': True
        }
        return render(request, self.template_name, ctx)

    def post(self, request, pk):

        ad = get_object_or_404(Ad, id=pk, owner=self.request.user)
        ad_form = AdForm(request.POST, request.FILES or None, instance=ad)
        car_form = CarForm(request.POST, instance=ad.car)
        make_form = MakeForm(request.POST, instance=ad.car.make)

        statement = (
                ad_form.is_valid()
                and car_form.is_valid()
                and make_form.is_valid()
        )
        if not statement:
            forms = [ad_form, make_form, car_form]
            ctx = {
                'forms': forms
            }
            return render(request, self.template_name, ctx)

        ad_form.save()
        make_form.save()
        car_form.save()
        success_url = reverse('ads:ad_detail', args=[pk])
        return redirect(success_url)


class AdDeleteView(OwnerDeleteView):
    model = Ad
    success_url = reverse_lazy('ads:all')


class AdFavoritesView(LoginRequiredMixin, OwnerAdView):
    """
    Adding an advertisement to favorites.
    """

    template_name = 'ads/favorite_ads.html'

    def get(self, request, *args, **kwargs):
        # select_related() cashes query
        favorite_ads = request.user.favorite_ads
        return super().get(request, ads=favorite_ads)


class AdProfileView(OwnerAdView):
    template_name = 'ads/ad_profile.html'

    def get(self, request, *args, **kwargs):
        if args:
            username = args[0]
        else:
            username = kwargs.get('username')
        # getting user by username
        owner = User.objects.filter(username=username)[0]
        # owner's ads
        ads_filtered = Ad.objects.filter(owner__username=username)
        owner_ads = ads_filtered.order_by('-created_at')
        context = {'owner': owner}
        if owner_ads:
            # select_related() cashes query
            ads = owner_ads.select_related().distinct()
            context['ads'] = ads
            return super().get(request, ads=ads, ctx=context)
        return super().get(request, empty_profile=True, ctx=context)


class CommentCreateView(LoginRequiredMixin, View):
    """
    View for creating comments.
    """

    @staticmethod
    def post(request, *args, **kwargs):
        if args:
            pk = args[0]
        else:
            pk = kwargs.get('pk')
        ad_obj = get_object_or_404(Ad, id=pk)
        comment = Comment(
            text=request.POST['comment'],
            owner=request.user,
            ad=ad_obj
        )
        comment.save()
        return redirect(reverse(
            'ads:ad_detail',
            args=[pk]))


class CommentDeleteView(OwnerDeleteView):
    model = Comment

    def get_success_url(self):
        ad = self.object.ad
        return reverse(
            'ads:ad_detail',
            args=[ad.id])


def stream_file(request, pk):
    # load picture data
    ad = get_object_or_404(Ad, id=pk)
    response = HttpResponse()
    response['Content-Type'] = ad.content_type
    response['Content-Length'] = len(ad.picture)
    response.write(ad.picture)
    return response


@method_decorator(csrf_exempt, name='dispatch')
class AddFavoriteView(LoginRequiredMixin, View):

    @staticmethod
    def post(request, pk):
        ad = get_object_or_404(Ad, id=pk)
        fav = Fav(owner=request.user, ad=ad)
        try:
            fav.save()  # In case of duplicate key
        except IntegrityError:
            pass
        return HttpResponse()


@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(LoginRequiredMixin, View):

    @staticmethod
    def post(request, pk):
        ad = get_object_or_404(Ad, id=pk)
        try:
            Fav.objects.get(owner=request.user, ad=ad).delete()
        except Fav.DoesNotExist:
            pass
        return HttpResponse()
