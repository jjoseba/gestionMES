# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django_filters
from django.shortcuts import get_object_or_404
from django.views.generic import UpdateView
from django_filters.views import FilterView
from filters.views import FilterMixin
from django.utils.translation import gettext as _

from core.filters.LabeledOrderingFilter import LabeledOrderingFilter
from core.filters.SearchFilter import SearchFilter
from core.forms.BootstrapModelForm import BootstrapModelForm
from core.forms.password import PasswordForm
from core.forms.profile import ProfileForm
from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.models import User


class UserForm(BootstrapModelForm):
    field_order = ['o', 'search', 'is_active', ]


class UserFilter(django_filters.FilterSet):

    search = SearchFilter(names=['username', 'first_name', 'last_name', 'email'], lookup_expr='in', label=_('Buscar...'))
    o = LabeledOrderingFilter(fields=['username', 'last_login', 'date_joined'])

    class Meta:
        model = User
        form = UserForm
        fields = { 'is_active':['exact'],  }


class UsersListView(FilterMixin, FilterView, AjaxTemplateResponseMixin):

    queryset = User.objects.all()
    model = User
    template_name = 'user/list.html'
    ajax_template_name = 'user/query.html'
    filterset_class = UserFilter
    paginate_by = 15


class UserDetailView(UpdateView):
    template_name = 'user/detail.html'
    password_form = PasswordForm
    form_class = ProfileForm
    profile_form = ProfileForm
    success_url = '/dashboard'
    model = User

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        user = self.get_object()
        if 'password_form' not in context:
            context['password_form'] = self.password_form(user=user)
        if 'profile_form' not in context:
            context['profile_form'] = self.profile_form(instance=user)

        context['profile_tab'] = True
        return context

    def form_invalid(self, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'profile_form' in request.POST:
            form_class = self.profile_form
            form_name = 'profile_form'
            form = self.profile_form(**self.get_form_kwargs())
        else:
            form_class = self.password_form
            form_name = 'password_form'
            form = self.password_form(user=self.object, **self.get_form_kwargs())

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(**{form_name: form})
