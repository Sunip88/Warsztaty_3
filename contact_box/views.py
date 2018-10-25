from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import Person, Email, Address, PhoneNumber, Groups
from django.views import View
from django.views.generic import CreateView
from .forms import AddPersonForm, AddressForm, EmailForm, PhoneNumberForm, AddGroupForm
from django.forms import formset_factory
from django.contrib import messages
# Create your views here.


class Home(View):
    def get(self, request):
        persons = Person.objects.all()
        return render(request, 'contact_box/home.html', {'persons': persons})


class Show(View):
    def get(self, request):
        persons = Person.objects.all().order_by('name')
        return render(request, 'contact_box/person.html', {'persons': persons})


class ShowSpecific(View):
    def get(self, request, id_person):
        persons = Person.objects.all()
        person_spec = Person.objects.get(id=id_person)
        return render(request, 'contact_box/person_specs.html', {'persons': persons, 'person_spec': person_spec})


class NewPerson(View):
    form_class = AddPersonForm
    # form_class_address = AddressForm
    # form_class_address = formset_factory(AddressForm, extra=2)
    # form_class_email = EmailForm
    # form_class_phone = PhoneNumberForm

    def get(self, request):
        persons = Person.objects.all()
        return render(request, 'contact_box/person_add.html',
                      {'form_p': self.form_class, 'persons': persons})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_person = form.save()
            messages.success(request, f'Osoba o imieniu - {new_person.name} oraz nazwisku - {new_person.surname} zostala dodana')
            return redirect('person-specific', id_person=new_person.id)
        return HttpResponse('Nieprawidłowe dane')


class EditPerson(View):
    form_class = AddPersonForm
    # form_class_address = AddressForm
    form_class_address = formset_factory(AddressForm, extra=1)
    form_class_email = formset_factory(EmailForm, extra=1)
    form_class_phone = formset_factory(PhoneNumberForm, extra=1)
    # form_class_email = EmailForm

    # form_class_phone = PhoneNumberForm

    def initial_address(self, address):
        initial = []
        for one_address in address:
            initial_address = {'id': one_address.id, 'city': one_address.city, 'street': one_address.street,
                               'street_number': one_address.street_number, 'flat_number': one_address.flat_number}
            initial.append(initial_address)
        return initial


    def get(self, request, person_id):
        persons_nav = Person.objects.all()
        person = Person.objects.get(id=person_id)
        address = person.address_set.all()
        email = person.email_set.all()
        phone = person.phonenumber_set.all()

        initial_person = {'name': person.name, 'surname': person.surname, 'description': person.description,
                          'image': person.image}
        form_db_person = self.form_class(initial=initial_person)

        if address:
            # initial = []
            # for one_address in address:
            #     initial_address = {'city': one_address.city, 'street': one_address.street,
            #                        'street_number': one_address.street_number, 'flat_number': one_address.flat_number}
            #     initial.append(initial_address)
            form_db_address = self.form_class_address(initial=self.initial_address(address), prefix='address')
        else:
            form_db_address = self.form_class_address(prefix='address')

        if email:
            initial = []
            for one_email in email:
                initial_email = {'email_address': one_email.email_address, 'email_type': one_email.email_type}
                initial.append(initial_email)
            form_db_email = self.form_class_email(initial=initial)
        else:
            form_db_email = self.form_class_email

        if phone:
            initial = []
            for one_phone in phone:
                initial_phone = {'phone_number': one_phone.phone_number, 'type_number': one_phone.type_number}
                initial.append(initial_phone)
            form_db_phone = self.form_class_phone(initial=initial)
        else:
            form_db_phone = self.form_class_phone

        return render(request, 'contact_box/person_modify.html',
                      {'form_p': form_db_person, 'form_a': form_db_address, 'form_e': form_db_email,
                       'form_phone': form_db_phone, 'persons': persons_nav})

    def post(self, request, person_id):
        button = request.POST.get('button')
        person = Person.objects.get(id=person_id)
        address = person.address_set.all()
        email = person.email_set.all()
        phone = person.phonenumber_set.all()
        if button == 'person':
            form = self.form_class(request.POST, instance=person)
            if form.is_valid():
                form.save()
        elif button == 'address':
            form_a = self.form_class_address(request.POST, prefix='address', initial=self.initial_address(address))
            if form_a.is_valid():
                for form in form_a:
                    if form.is_valid() and form.has_changed(): # naprawić problemuy
                        form_city = form.cleaned_data['city']
                        form_street = form.cleaned_data['street']
                        form_street_number = form.cleaned_data['street_number']
                        form_flat_number = form.cleaned_data['flat_number']
                        if form_city and form_street and form_street_number and form_flat_number:
                            form_id = form.cleaned_data['id']
                            address_db_obj = Address.objects.filter(id=form_id)
                            if len(address_db_obj) > 0:
                                one_address = address_db_obj.first()
                                one_address.flat_number = form_flat_number
                                one_address.city = form_city
                                one_address.street_number = form_street_number
                                one_address.street = form_street
                                one_address.save()
                            else:
                                form.instance.persons = person
                                form.save()
                        # elif form.is_valid() and form.empty_permitted:
                        #     form.instance.persons = person
                        #     form.save()

        elif button == 'email':
            pass
        elif button == 'phone':
            pass



            form_e = self.form_class_email(request.POST, instance=email)
            form_phone = self.form_class_phone(request.POST, instance=phone)
            if form_a.is_valid() and form_e.is_valid() and form_phone.is_valid():
                if address:
                    form_a.save()
                else:
                    form_a.instance.persons = person
                    form_a.save()

                if email:
                    form_e.save()
                else:
                    form_e.instance.persons = person
                    form_e.save()

                if phone:
                    form_phone.save()
                else:
                    form_phone.instance.persons = person
                    form_phone.save()

        return redirect('show-all')


# edycja zrobiona tylko dla jednego adresu, miasta i telefonu


def delete_person(request, person_id):
    person = get_object_or_404(Person, id=person_id)
    person.delete()
    messages.success(request, 'Dane osoby zostały usunięte')
    return redirect('show-all')


class ShowGroups(View):
    def get(self, request):
        groups = Groups.objects.all()
        return render(request, 'contact_box/groups.html', {'groups': groups})


class NewGroup(View):
    form_class = AddGroupForm

    def get(self, request):
        groups = Groups.objects.all()
        return render(request, 'contact_box/group_add.html',
                      {'form': self.form_class, 'groups': groups})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_group = form.save()
            messages.success(request, f'Grupa o nazwie {new_group.title} zostala stworzona')
            return redirect('group-specific', id_group=new_group.id)
        return HttpResponse('Nieprawidłowe dane')


class ShowSpecificGroup(View):
    def get(self, request, id_group):
        groups = Groups.objects.all()
        group_spec = Groups.objects.get(id=id_group)
        person_on = list(group_spec.persons.all())
        return render(request, 'contact_box/groups_specs.html', {'groups': groups, 'group_spec': group_spec, 'persons': person_on})


class EditGroup(View):
    form_class = AddGroupForm

    def get(self, request, group_id):
        groups = Groups.objects.all()
        group = get_object_or_404(Groups, id=group_id)
        initial_person = {'title': group.title, 'description': group.description}
        form_db_person = self.form_class(initial=initial_person)
        persons = list(Person.objects.all())
        person_on = list(group.persons.all())

        return render(request, 'contact_box/group_modify.html',
                      {'form': form_db_person, 'groups': groups, 'person_on': person_on, 'persons': persons})

    def post(self, request, group_id):
        group = get_object_or_404(Groups, id=group_id)
        button = request.POST.get('button')
        if button == 'group':
            form = self.form_class(request.POST, instance=group)
            if form.is_valid():
                form.save()
                messages.success(request, f'Grupa zostala zmodyfikowana')
        elif button == 'person':
            i = 0
            persons = [int(x) for x in request.POST.getlist('person')]
            for person in persons:
                person_db = Person.objects.get(id=person)
                person_group_db = group.persons.filter(id=person_db.id)
                if len(person_group_db) == 0:
                    group.persons.add(person_db)
                    i += 1
            person_on = list(group.persons.all())
            for person in person_on:
                if person.id not in persons:
                    person.delete()
            if i > 0:
                messages.success(request, f'Dodano do grupy kontakty w liczbie {i}')

        return redirect('group-specific', id_group=group.id)


def delete_group(request, group_id):
    group = get_object_or_404(Groups, id=group_id)
    group.delete()
    messages.success(request, 'Grupa została usunięta')
    return redirect('show-all-groups')