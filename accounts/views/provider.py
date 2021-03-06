# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django_filters
from django.conf import settings
from django.contrib import messages
from django.http import Http404
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import UpdateView, CreateView
from django_filters.views import FilterView
from filters.views import FilterMixin

from accounts.forms.provider import ProviderForm, ProviderSignupForm
from accounts.mixins.entity_collab import EntityCollabFormMixin
from accounts.mixins.feecomments import FeeCommentsMixin
from accounts.mixins.signup import SignupFormMixin, SignupUpdateMixin
from accounts.models import Provider, SignupProcess, Category, ACTIVE
from core.filters.LabeledOrderingFilter import LabeledOrderingFilter
from core.filters.SearchFilter import SearchFilter
from core.forms.BootstrapForm import BootstrapForm
from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.mixins.ExportAsCSVMixin import ExportAsCSVMixin
from core.mixins.ListItemUrlMixin import ListItemUrlMixin
from core.mixins.TabbedViewMixin import TabbedViewMixin
from core.mixins.XFrameExemptMixin import XFrameOptionsExemptMixin
from payments.models import FeeRange, PendingPayment
from social_balance.models import EntitySocialBalance, SocialBalanceBadge


class ProviderFilterForm(BootstrapForm):
    field_order = ['o', 'search', 'status', ]


class ProviderFilter(django_filters.FilterSet):

    search = SearchFilter(names=['address', 'cif', 'name', 'business_name', 'contact_email'], lookup_expr='in', label=_('Buscar...'))
    o = LabeledOrderingFilter(fields=['name', 'start_year', 'registration_date'], field_labels={'name':'Nombre', 'start_year':'Año de inicio', 'registration_date':'Fecha de alta'})

    class Meta:
        model = Provider
        form = ProviderFilterForm
        fields = { 'status':['exact'], }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.initial['status'] = ACTIVE


class ProvidersListView(FilterMixin, FilterView, ExportAsCSVMixin, ListItemUrlMixin, AjaxTemplateResponseMixin):

    model = Provider
    queryset = Provider.objects.all().prefetch_related('app_user')
    objects_url_name = 'provider_detail'
    template_name = 'provider/list.html'
    ajax_template_name = 'provider/query.html'
    filterset_class = ProviderFilter
    paginate_by = 15

    csv_filename = 'proveedoras'
    available_fields = ['cif', 'name', 'business_name', 'public_address', 'address',  'contact_email', 'contact_phone', 'contact_person', 'territory',
                        'description', 'short_description', 'registered_in_app', 'num_workers', 'aprox_income', 'current_fee', 'has_logo',
                        'postalcode', 'city', 'address', 'province', 'iban_code', 'registration_date', 'is_physical_store',
                        'bonus_percent_entity', 'bonus_percent_general', 'max_percent_payment', 'start_year', 'facebook_link', 'webpage_link', 'twitter_link', 'instagram_link',
                        'telegram_link', 'category_list']
    field_labels = {'registered_in_app': 'Registrada en la app', 'current_fee': 'Cuota anual', 'has_logo':'Tiene logo', 'category_list':'Categorías'}


class ProviderDetailView(TabbedViewMixin, FeeCommentsMixin, EntityCollabFormMixin, UpdateView):
    template_name = 'provider/detail.html'
    default_tab = 'details'
    available_tabs = ['details', 'payments', 'balances', 'currency']
    form_class = ProviderForm
    model = Provider

    def get_success_url(self):
        return reverse('accounts:provider_detail', kwargs={'pk': self.object.pk})

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def form_valid(self, form):
        response = super(ProviderDetailView, self).form_valid(form)
        messages.success(self.request, _('Datos actualizados correctamente.'))
        return response

    def get_context_data(self, **kwargs):
        context = super(ProviderDetailView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['payments'] = PendingPayment.objects.filter(account=self.object)
        context['signup'] = self.object.signup_process.first()
        context['social_balances'] = EntitySocialBalance.objects.filter(entity=self.object).order_by('year')
        context['current_balance'] = EntitySocialBalance.objects.filter(entity=self.object, year=settings.CURRENT_BALANCE_YEAR).first()
        context['current_badge'] =  SocialBalanceBadge.objects.filter(year=settings.CURRENT_BALANCE_YEAR).first()
        context['profile_tab'] = True

        return context

class ProviderSignup(XFrameOptionsExemptMixin, SignupFormMixin, CreateView):

    form_class = ProviderSignupForm
    model = Provider
    template_name = 'provider/create.html'

    def form_valid(self, form):
        response = super(ProviderSignup, self).form_valid(form)
        process = SignupProcess.objects.create_process(account=self.object)
        process.form_filled(self.object, form)
        return response

    def get_context_data(self, **kwargs):
        context = super(ProviderSignup, self).get_context_data(**kwargs)

        context['worker_ranges'] = FeeRange.objects.order_by('min_num_workers').values('min_num_workers', 'max_num_workers').distinct()
        context['income_ranges'] = FeeRange.objects.order_by('min_income').values('min_income', 'max_income').distinct()
        context['fees'] = FeeRange.objects.all()
        context['categories'] = Category.objects.all()

        return context


    def get_success_url(self):
        if self.request.user.is_authenticated:
            messages.success(self.request, _('Proceso de acogida añadido correctamente.'))
            return reverse('accounts:signup_list')
        else:
            return reverse('accounts:signup_success')


class ProviderUpdateView(SignupUpdateMixin, UpdateView):
    template_name = 'provider/edit.html'
    form_class = ProviderSignupForm
    model = Provider

    def get_context_data(self, **kwargs):
        context = super(ProviderUpdateView, self).get_context_data(**kwargs)
        context['worker_ranges'] = FeeRange.objects.order_by('min_num_workers').values('min_num_workers', 'max_num_workers').distinct()
        context['income_ranges'] = FeeRange.objects.order_by('min_income').values('min_income', 'max_income').distinct()
        context['fees'] = FeeRange.objects.all()
        context['categories'] = Category.objects.all()
        return context
