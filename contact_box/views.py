from django.shortcuts import render, HttpResponse, redirect
from .models import Person, Email, Address, PhoneNumber
from django.views import View
from django.views.generic import CreateView
from .forms import AddPersonForm, AddressForm, EmailForm, PhoneNumberForm
# Create your views here.


class Home(View):
    def get(self, request):
        persons = Person.objects.all()
        return render(request, 'contact_box/home.html', {'persons': persons})


class Show(View):
    def get(self, request):
        persons = Person.objects.all()
        return render(request, 'contact_box/person.html', {'persons': persons})


class ShowSpecific(View):
    def get(self, request, id_person):
        persons = Person.objects.all()
        person_spec = Person.objects.get(id=id_person)
        return render(request, 'contact_box/person_specs.html', {'persons': persons, 'person_spec': person_spec})


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
            if form_a.is_valid() and form_e.is_valid() and form_phone.is_valid():
                form_a.instance.persons = new_person
                form_e.instance.persons = new_person
                form_phone.instance.persons = new_person
                form_a.save()
                form_e.save()
                form_phone.save()

            return redirect('show-all')
        return HttpResponse('Nieprawidłowe dane')


class EditPerson(View):
    form_class = AddPersonForm
    form_class_address = AddressForm
    form_class_email = EmailForm
    form_class_phone = PhoneNumberForm

    def get(self, request, person_id):
        persons_nav = Person.objects.all()
        person = Person.objects.get(id=person_id)
        address = person.address_set.all().first() # temp
        email = person.email_set.all().first() # temp
        phone = person.phonenumber_set.all().first()

        initial_person = {'name': person.name, 'surname': person.surname, 'description': person.description, 'image': person.image}
        form_db_person = self.form_class(initial=initial_person)

        if address:
            initial_address = {'city': address.city, 'street': address.street, 'street_number': address.street_number,
                               'flat_number': address.flat_number}
            form_db_address = self.form_class_address(initial=initial_address)
        else:
            form_db_address = self.form_class_address
        if email:
            initial_email = {'email_address': email.email_address, 'email_type': email.email_type}
            form_db_email = self.form_class_email(initial=initial_email)
        else:
            form_db_email = self.form_class_email
        if phone:
            initial_phone = {'phone_number': phone.phone_number, 'type_number': phone.type_number}
            form_db_phone = self.form_class_phone(initial=initial_phone)
        else:
            form_db_phone = self.form_class_phone

        return render(request, 'contact_box/person_add.html',
                      {'form_p': form_db_person, 'form_a': form_db_address, 'form_e': form_db_email,
                       'form_phone': form_db_phone, 'persons': persons_nav})

    def post(self, request, person_id):
        person = Person.objects.get(id=person_id)
        address = person.address_set.all().first() # temp
        email = person.email_set.all().first() # temp
        phone = person.phonenumber_set.all().first()
        form = self.form_class(request.POST, instance=person)
        if form.is_valid():
            form.save()
            form_a = self.form_class_address(request.POST, instance=address)
            form_e = self.form_class_email(request.POST, instance=email)
            form_phone = self.form_class_phone(request.POST, instance=phone)
            if form_a.is_valid() and form_e.is_valid() and form_phone.is_valid():
                if address:
                    form_a.save()
                else:
                    new_address = form_a.save()
                    new_address_obj = Address.objects.get(id=new_address.pk)
                    new_address_obj.persons_id = person.id
                    new_address_obj.save()

                if email:
                    form_e.save()
                else:
                    new_email = form_e.save()
                    new_email_obj = Email.objects.get(id=new_email.pk)
                    new_email_obj.persons_id = person.id
                    new_email_obj.save()

                if phone:
                    form_phone.save()
                else:
                    new_phone = form_phone.save()
                    new_phone_obj = PhoneNumber.objects.get(id=new_phone.pk)
                    new_phone_obj.persons_id = person.id
                    new_phone_obj.save()

            return HttpResponse('gg dane')
        return HttpResponse('Nieprawidłowe dane')

# edycja zrobiona tylko dla jednego adresu, miasta i telefonu