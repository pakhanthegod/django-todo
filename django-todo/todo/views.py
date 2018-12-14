from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic.base import ContextMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Item
from .forms import ItemForm, CustomSignupForm


# TODO: learn how to write a mixin
# class AllowControlMixin:
#     def dispatch(self, request, *args, **kwargs):
#         obj = Item.objects.get(pk=kwargs['pk'])
#         if request.user.id == obj.user.id:
#             return View.dispatch(self, request, *args, **kwargs)
#         else:
#             return redirect('todo:index')


class ItemView(View, ContextMixin):
    model = Item
    form_class = ItemForm
    template_name = 'todo/index.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['form'] = self.form_class()
        print(request)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = get_object_or_404(get_user_model(), username=request.user)
            user_item = form.save(commit=False)
            user_item.user = user
            user_item.save()
            return self.get(request, *args, **kwargs)
        else:
            context = self.get_context_data()
            context['form'] = form
            return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = Item.objects.filter(user=self.request.user.id)
        return context


class ItemUpdateView(UpdateView):
    form_class = ItemForm
    template_name_suffix = '_update'
    success_url = reverse_lazy('todo:index')

    # TODO: Replace with mixin
    def get(self, request, *args, **kwargs):
        obj = Item.objects.get(pk=kwargs['pk'])
        if request.user.id != obj.user.id:
            return redirect('todo:index')
        return super().get(request, *args, **kwargs)

    def get_object(self):
        print(self.kwargs['pk'])
        return Item.objects.get(pk=self.kwargs['pk'])


class ItemDeleteView(DeleteView):
    success_url = reverse_lazy('todo:index')

    # TODO: Replace with mixin
    def get(self, request, *args, **kwargs):
        obj = Item.objects.get(pk=kwargs['pk'])
        if request.user.id != obj.user.id:
            return redirect('todo:index')
        return super().get(request, *args, **kwargs)

    def get_object(self):
        return Item.objects.get(pk=self.kwargs['pk'])


class UserSignupView(View, ContextMixin):
    template_name = 'registration/signup.html'
    form_class = CustomSignupForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context=self.get_context_data())
    
    def post(self, request, *args, **kwargs):
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно создали аккаунт.', extra_tags='alert alert-success')
            return redirect('login')
        else:
            context = self.get_context_data()
            context['form'] = form
            return render(request, self.template_name, context=context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        return context