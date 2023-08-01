from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db.utils import IntegrityError
from django.urls import reverse_lazy, reverse
from django.views import View

from .models import Ad, Comment, Fav
from .owner import (OwnerListView, OwnerDeleteView,
                    OwnerDetailView, OwnerAdView)
from .forms import MakeForm, AdForm, CarForm, CommentForm

from django.contrib.auth.mixins import LoginRequiredMixin


class AdListView(OwnerAdView, OwnerListView):
    model = Ad

    def get(self, request, *args, **kwargs):
        super().get(self, request)


class AdDetailView(OwnerDetailView):

    def get(self, request, *args, **kwargs):
        if args:
            pk = args[0]
        else:
            pk = kwargs.get('pk')
        x = get_object_or_404(Ad, id=pk)
        comments = Comment.objects.filter(ad=x).order_by('-created_at')
        comment_form = CommentForm()

        favorites = list()
        if request.user.is_authenticated:
            # rows = [{'id': 2}, {'id': 4} ... ]  (A list of rows)
            rows = request.user.favorite_ads.values('id')
            # favorites = [2, 4, ...] using list comprehension
            favorites = [row['id'] for row in rows]
        ctx = {
            'ad': x,
            'comments': comments,
            'comment_form': comment_form,
            'favorites': favorites
        }
        return render(request, 'ads/ad_detail.html', ctx)


class AdCreateView(LoginRequiredMixin, View):
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:all')

    def get(self, request):
        ad_form = AdForm()
        car_form = CarForm()
        make_form = MakeForm()
        ctx = {'ad_form': ad_form, 'car_form': car_form, 'make_form': make_form}
        return render(request, self.template_name, ctx)

    def post(self, request):
        owner_car = request.user.owner_car
        ad_form = AdForm(request.POST, request.FILES or None)
        car_form = CarForm(request.POST, instance=owner_car)
        make_form = MakeForm(
            request.POST,
            instance=owner_car.make
        )

        statement = (
                ad_form.is_valid()
                and car_form.is_valid()
                and make_form.is_valid()
        )
        if not statement:
            ctx = {
                'ad_form': ad_form,
                'car_form': car_form,
                'make_form': make_form
            }
            return render(request, self.template_name, ctx)

        # Add owner and phone number to the model Ad before saving
        ad = ad_form.save(commit=False)
        ad.owner = self.request.user
        ad.phone = self.request.user.owner.phone
        ad.save()
        ad_form.save()
        # Add make to the model Car before saving
        car = car_form.save(commit=False)
        make = make_form.save()
        car.make = make
        car.save()
        return redirect(self.success_url)


class AdUpdateView(LoginRequiredMixin, View):
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:all')

    def get(self, request, pk):
        ad = get_object_or_404(Ad, id=pk, owner=self.request.user)
        ad_form = AdForm(instance=ad)
        car_form = CarForm(instance=ad.car)
        make_form = MakeForm(instance=ad.car.make)
        ctx = {'ad_form': ad_form, 'car_form': car_form, 'make_form': make_form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
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
            ctx = {
                'ad_form': ad_form,
                'car_form': car_form,
                'make_form': make_form
            }
            return render(request, self.template_name, ctx)

        ad_form.save()
        make_form.save()
        car_form.save()
        return redirect(self.success_url)


class AdDeleteView(OwnerDeleteView):
    model = Ad


class AdFavoritesView(LoginRequiredMixin, OwnerAdView):
    template_name = reverse_lazy('ads:favorites')

    def get(self, request, *args, **kwargs):
        # select_related() cashes query
        favorite_ads = request.user.favorite_ads.value('ad')
        ads = favorite_ads.select_related().distinct()
        super().get(self, ads_with_filter=ads, statement=None)


class AdProfileView(LoginRequiredMixin, OwnerAdView):
    template_name = reverse_lazy('ads:profile')

    def get(self, request, *args, **kwargs):
        # select_related() cashes query
        ads = request.user.ads.select_related().distinct()
        super().get(self, ads_with_filter=ads, statement=None)


class CommentCreateView(LoginRequiredMixin, View):

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
        return redirect(reverse('ads:ad_detail', args=[pk]))


class CommentDeleteView(OwnerDeleteView):
    model = Comment

    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
    def get_success_url(self):
        ad = self.object.ad
        return reverse('ads:ad_detail', args=[ad.id])


def stream_file(request, pk):
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
        fav = Fav(user=request.user, ad=ad)
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
            Fav.objects.get(user=request.user, ad=ad).delete()
        except Fav.DoesNotExist:
            pass
        return HttpResponse()
