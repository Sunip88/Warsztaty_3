from django import forms
from .models import Person, Address, Email, PhoneNumber


class AddPersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'surname', 'description', 'image']


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['city', 'street', 'street_number', 'flat_number']


class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ['email_address', 'email_type']


class PhoneNumberForm(forms.ModelForm):
    class Meta:
        model = PhoneNumber
        fields = ['phone_number', 'type_number']

