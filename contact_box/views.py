from django.shortcuts import render, HttpResponse
from .models import Person
from django.views import View
from django.views.generic import CreateView
from .forms import AddPersonForm, AddressForm, EmailForm, PhoneNumberForm
# Create your views here.


class Home(View):
    persons = Person.objects.all()

    def get(self, request):
        return render(request, 'contact_box/home.html', {'persons': self.persons})


class Show(View):
    persons = Person.objects.all()

    def get(self, request, id_person):
        person_spec = Person.objects.get(id=id_person)
        return render(request, 'contact_box/person_specs.html', {'persons': self.persons, 'person_spec': person_spec})


class NewPerson(View):
    form_class = AddPersonForm
    form_class_address = AddressForm
    form_class_email = EmailForm
    form_class_phone = PhoneNumberForm

    def get(self, request):
        persons = Person.objects.all()
        return render(request, 'contact_box/person_add.html',
                      {'form_p': self.form_class, 'form_a': self.form_class_address, 'form_e': self.form_class_email,
                       'form_phone': self.form_class_phone, 'persons': persons})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            new_person = Person.objects.get(id=form.instance.id)
            form_a = self.form_class_address(request.POST)
            form_e = self.form_class_email(request.POST)
            form_phone = self.form_class_phone(request.POST)
            if form_a.is_valid() and form_e.is_valid():
                form_a.instance.persons = new_person
                form_e.instance.persons = new_person
                form_phone.instance.persons = new_person
                form_a.save()
                form_e.save()
                form_phone.save()

            return HttpResponse('gg dane')
        return HttpResponse('Nieprawidłowe dane')
