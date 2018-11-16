from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import Person, Email, Address, PhoneNumber, Groups
from django.views import View
from .forms import AddPersonForm, AddressForm, EmailForm, PhoneNumberForm, AddGroupForm, SearchGroupForm
from django.forms import inlineformset_factory
from django.contrib import messages


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
    form_class_address = AddressForm
    form_class_email = inlineformset_factory(Person, Email, EmailForm, extra=1)
    form_class_phone = inlineformset_factory(Person, PhoneNumber, PhoneNumberForm, extra=1)

    def get(self, request, person_id):
        persons_nav = Person.objects.all()
        addresses_all = Address.objects.all()
        person = get_object_or_404(Person, id=person_id)
        if person.addresses_id:
            address_person = person.addresses_id
        else:
            address_person = None
        form_db_person = self.form_class(instance=person)
        form_db_address = self.form_class_address(use_required_attribute=False)
        form_db_email = self.form_class_email(instance=person)
        form_db_phone = self.form_class_phone(instance=person)

        return render(request, 'contact_box/person_modify.html',
                      {'form_a': form_db_address, 'form_p': form_db_person, 'form_e': form_db_email,
                       'form_phone': form_db_phone, 'persons': persons_nav, 'addresses': addresses_all,
                       'address_person': address_person})

    def post(self, request, person_id):
        button = request.POST.get('button')
        person = Person.objects.get(id=person_id)
        counter = 0
        if button == 'person':
            form = self.form_class(request.POST, request.FILES, instance=person)
            if form.is_valid():
                temp = form.save()
                if temp:
                    counter += 1
        elif button == 'address':
            form_a = self.form_class_address(request.POST)
            if form_a.is_valid():
                temp = form_a.save()
                if temp:
                    temp.person_set.add(person)
                    counter += 1
            else:
                select_id = request.POST.get("address_select")
                if select_id != "0":
                    address_select = get_object_or_404(Address, id=select_id)
                    address_select.person_set.add(person)
                    counter += 1
                elif select_id == "0":
                    person.addresses = None
                    person.save()
                    counter += 1
        elif button == 'email':
            form_e = self.form_class_email(request.POST, instance=person)
            if form_e.is_valid():
                temp = form_e.save()
                if temp:
                    counter += 1
        elif button == 'phone':
            form_phone = self.form_class_phone(request.POST, instance=person)
            if form_phone.is_valid():
                temp = form_phone.save()
                if temp:
                    counter += 1
        if counter > 0:
            messages.success(request, 'Udało się zmodyfikować/dodać dane')
        else:
            messages.warning(request, 'Dane zostały błędnie wypełnione')
        return redirect('modify-person', person_id=person.id)


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
                    group.persons.remove(Person.objects.get(id=person.id))
            if i > 0:
                messages.success(request, f'Dodano do grupy kontakty w liczbie {i}')

        return redirect('group-specific', id_group=group.id)


def delete_group(request, group_id):
    group = get_object_or_404(Groups, id=group_id)
    group.delete()
    messages.success(request, 'Grupa została usunięta')
    return redirect('show-all-groups')


class SearchGroup(View):
    class_form = SearchGroupForm

    def get(self, request):
        return render(request, 'contact_box/search.html', {'form': self.class_form})

    def post(self, request):
        form = self.class_form(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            if name:
                result_person_name = Person.objects.filter(name__icontains=name)
            else:
                result_person_name = Person.objects.all()
            if surname:
                result_person_surname = Person.objects.filter(surname__icontains=surname)
            else:
                result_person_surname = Person.objects.all()
            result_persons = result_person_name.distinct() & result_person_surname.distinct()
            if not result_persons:
                messages.warning(request, 'Brak wyników wyszukiwania')
        return render(request, 'contact_box/search.html', {'form': self.class_form, 'persons': result_persons})


class Addresses(View):
    def get(self, request):
        addresses_db = Address.objects.all()
        return render(request, 'contact_box/addresses.html', {'addresses': addresses_db})


class NewAddresses(View):
    class_form = AddressForm

    def get(self, request):
        return render(request, 'contact_box/address_add.html', {'form': self.class_form})

    def post(self, request):
        form = self.class_form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Udało się stworzyć nowy adres')
        return redirect('show-all-address')


def delete_address(request, address_id):
    address_db = get_object_or_404(Address, id=address_id)
    address_db.delete()
    messages.success(request, 'Adres został usunięty')
    return redirect('show-all-address')


class EditAddress(View):
    form_class = AddressForm

    def get(self, request, address_id):
        address_db = get_object_or_404(Address, id=address_id)
        persons = address_db.person_set.all()
        initial_address = {'city': address_db.city, 'street': address_db.street,
                           'street_number': address_db.street_number, 'flat_number': address_db.flat_number}
        form = self.form_class(initial=initial_address)
        return render(request, 'contact_box/address_modify.html', {'form': form, 'persons': persons})

    def post(self, request, address_id):
        address_db = get_object_or_404(Address, id=address_id)
        form = self.form_class(request.POST, instance=address_db)
        if form.is_valid():
            form.save()
            messages.success(request, 'Adres zostal zmodyfikowany')
        return redirect('show-all-address')


class ShowPersonAddress(View):

    def get(self, request, address_id):
        address = get_object_or_404(Address, id=address_id)
        persons = address.person_set.all()
        return render(request, 'contact_box/address_persons.html', {'persons': persons, 'address': address})


# TODO stworzyc messega czy na pewno usunac chcesz adres gdy wiecej niz 0 mieszkancow
