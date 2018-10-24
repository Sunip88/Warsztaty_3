from django import forms
from .models import Person, Address, Email, PhoneNumber, Groups


class AddPersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'surname', 'description', 'image']


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['city', 'street', 'street_number', 'flat_number']

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        self.fields['city'].required = False
        self.fields['street'].required = False
        self.fields['street_number'].required = False
        self.fields['flat_number'].required = False

class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ['email_address', 'email_type']

    def __init__(self, *args, **kwargs):
        super(EmailForm, self).__init__(*args, **kwargs)
        self.fields['email_address'].required = False
        self.fields['email_type'].required = False


class PhoneNumberForm(forms.ModelForm):
    class Meta:
        model = PhoneNumber
        fields = ['phone_number', 'type_number']

    def __init__(self, *args, **kwargs):
        super(PhoneNumberForm, self).__init__(*args, **kwargs)
        self.fields['phone_number'].required = False
        self.fields['type_number'].required = False


class AddGroupForm(forms.ModelForm):
    class Meta:
        model = Groups
        fields = ['title', 'description']
