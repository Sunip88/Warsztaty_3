from django import forms
from .models import Person, Address, Email, PhoneNumber, Groups


class AddPersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'surname', 'description', 'image']
        labels = {
            'name': 'Imię',
            'surname': 'Nazwisko',
            'description': 'Opis',
            'image': 'Zdjęcie',
        }


class AddressForm(forms.ModelForm):
    flat_number = forms.CharField(required=False)
    class Meta:
        model = Address
        fields = ['city', 'street', 'street_number', 'flat_number']
        labels = {
            'city': 'Miasto',
            'street': 'Ulica',
            'street_number': 'Numer domu',
            'flat_number': 'Numer mieszkania',
        }


class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ['email_address', 'email_type']
        labels = {
            'email_address': 'Adres email',
            'email_type': 'Typ adresu',
        }


class PhoneNumberForm(forms.ModelForm):
    class Meta:
        model = PhoneNumber
        fields = ['phone_number', 'type_number']
        labels = {
            'phone_number': 'numer telefonu',
            'type_number': 'typ numeru'
        }


class AddGroupForm(forms.ModelForm):
    class Meta:
        model = Groups
        fields = ['title', 'description']
        labels = {
            'title': 'Tytuł',
            'description': 'Opis'
        }


class SearchGroupForm(forms.Form):
    name = forms.CharField(max_length=32, required=False, label='Imię')
    surname = forms.CharField(max_length=32, required=False, label='Nazwisko')
