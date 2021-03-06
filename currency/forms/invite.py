# coding=utf-8
from datetime import datetime
import dateutil
from django import forms
from django.contrib.auth.models import Permission, Group
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from accounts.models import Category, Provider
from core.forms.BootstrapForm import BootstrapForm
from currency.models import GuestInvitation, INVITE_DURATION_MONTHS, GuestAccount
from management.models import Comission
from mes.settings import MEMBER_PROV


class GuestInviteForm(forms.ModelForm, BootstrapForm):

    invite_token = forms.CharField(required=False, max_length=150, widget=forms.HiddenInput())

    class Meta:
        model = GuestAccount
        exclude = ['active', 'expiration_date', 'registration_date', 'invited_by', 'address', 'province', 'postalcode', 'guest_reference', 'cif', 'contact_phone']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }


    def clean(self):
        data = self.cleaned_data

        email = self.cleaned_data.get('contact_email', '')
        if GuestAccount.objects.filter(contact_email=email).exists():
            self.add_error('contact_email',_('Ya hay una invitación con este email. Revisa tu email para acceder con tu usuario a la app'))
    

        invite_token = data.get('invite_token', '')
        if not GuestInvitation.objects.is_valid_token(invite_token):
            raise ValidationError(_('Token de invitación no válido'))

        return data

    def save(self, commit=True):

        invitation = GuestInvitation.objects.filter(token=self.cleaned_data.get('invite_token')).first()
        instance = forms.ModelForm.save(self, False)
        instance.invited_by = invitation.invited_by
        instance.token_used = invitation
        instance.registration_date = datetime.now()
        instance.expiration_date = datetime.now() + dateutil.relativedelta.relativedelta(months=INVITE_DURATION_MONTHS)

        # Do we need to save all changes now?
        if commit:
            instance.save()
            self.save_m2m()

            invitation.used = True
            invitation.save()

        return instance