from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from .forms import OwnerForm, UserForm


class SignUpView(View):
    template_name = 'users/signup.html'
    success_url = reverse_lazy('ads:all')

    def get(self, request):
        user_form = UserForm()
        owner_form = OwnerForm()
        forms = [user_form, owner_form]
        ctx = {
            'forms': forms
        }
        return render(request, self.template_name, ctx)

    @transaction.atomic
    def post(self, request):
        user_form = UserForm(request.POST, instance=request.user)
        owner_form = OwnerForm(request.POST, instance=request.user.owner)

        if not (user_form.is_valid() and owner_form.is_valid()):
            forms = [user_form, owner_form]
            ctx = {
                'forms': forms
            }
            return render(request, self.template_name, ctx)

        owner = owner_form.save(commit=False)
        owner.user = request.user
        owner.save()
        user_form.save()
        return redirect(self.success_url)
