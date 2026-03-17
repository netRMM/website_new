from django.forms import ModelForm,TextInput
from django.utils.translation import gettext_lazy as _

from .models import Customer,ContactUs
from django import forms

from phonenumber_field.formfields import PhoneNumberField

class CustomerForm(ModelForm):
    phone_number = PhoneNumberField(widget=TextInput(
        attrs={
            'placeholder': _('Phone number'),
            'style': 'width: 100%;'  # This line sets the input field width to 100%
        }), 
        label=_("Phone number"), 
        required=True
    )
    country = forms.ChoiceField(
        choices=[("", "Select Country Name")] +
                list(Customer._meta.get_field('country').choices),
        widget=forms.Select(attrs={"class": "form-select validate"}),
        required=True
    )
    class Meta:
        model = Customer
        fields = [
            'firstname',
            'lastname',
            'company_name',
            'bracket',
            'email',
            'phone_number',
            'address',
            'country',
            'subdomain',
            'number_of_devices',
            'contact_mode',
        ]

class contactForm(ModelForm):
    class Meta:
        model = ContactUs
        fields = [
            'name',
            'email',
            'phone_number',
            'company_name',
            'message'
        ]