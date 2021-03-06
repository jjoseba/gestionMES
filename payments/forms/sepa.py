from django import forms
from django.conf import settings

from core.forms.BootstrapForm import BootstrapForm
from payments.models import SepaPaymentsBatch, PendingPayment, SepaBatchResult


class SepaBatchForm(forms.ModelForm, BootstrapForm):
    payments = forms.ModelMultipleChoiceField(queryset=PendingPayment.objects.filter(), required=False, )
    payments_order = forms.CharField(widget=forms.HiddenInput())
    required_fields = []

    class Meta:
        model = SepaPaymentsBatch
        exclude = ['sepa_file', 'amount', 'attempt']


    def save(self, commit=True):

        instance = forms.ModelForm.save(self, False)
        # Prepare a 'save_m2m' method for the form,
        def save_m2m():
           paymentsOrder = self.cleaned_data['payments_order']
           paymentsOrder = paymentsOrder.split(settings.INLINE_INPUT_SEPARATOR)
           print(paymentsOrder)
           for payment in self.cleaned_data['payments'].all():
               order = paymentsOrder.index(str(payment.pk))
               print(payment)
               print(payment.pk)
               print(order)
               SepaBatchResult.objects.create(payment=payment, order=order, batch=instance)

        self.save_m2m = save_m2m

        # Do we need to save all changes now?
        if commit:
            instance.save()
            self.save_m2m()

            total_amount = 0
            for payment in instance.payments.all():
                total_amount += payment.amount
            instance.amount = total_amount
            instance.save()

            instance.preprocess_batch()
            instance.generate_batch()


        return instance

