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
    form_class_address = inlineformset_factory(Person, Address, AddressForm, extra=1)
    form_class_email = inlineformset_factory(Person, Email, EmailForm, extra=1)
    form_class_phone = inlineformset_factory(Person, PhoneNumber, PhoneNumberForm, extra=1)

    def get(self, request, person_id):
        persons_nav = Person.objects.all()
        person = Person.objects.get(id=person_id)
        form_db_person = self.form_class(instance=person)
        form_db_address = self.form_class_address(instance=person)
        form_db_email = self.form_class_email(instance=person)
        form_db_phone = self.form_class_phone(instance=person)

        return render(request, 'contact_box/person_modify.html',
                      {'form_p': form_db_person, 'form_a': form_db_address, 'form_e': form_db_email,
                       'form_phone': form_db_phone, 'persons': persons_nav})

    def post(self, request, person_id):
        button = request.POST.get('button')
        person = Person.objects.get(id=person_id)
        counter = 0
        if button == 'person':
            form = self.form_class(request.POST, instance=person)
            if form.is_valid():
                temp = form.save()
                if temp:
                    counter += 1
        elif button == 'address':
            form_a = self.form_class_address(request.POST, instance=person)
            if form_a.is_valid():
                temp = form_a.save()
                if temp:
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
                    person.delete()
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
                result_name = Groups.objects.filter(persons__name__icontains=name)
            else:
                result_name = Groups.objects.all()
            if surname:
                result_surname = Groups.objects.filter(persons__surname__icontains=surname)
            else:
                result_surname = Groups.objects.all()
            result = result_name.distinct() & result_surname.distinct()
            if not result:
                messages.warning(request, 'Brak wyników wyszukiwania')
        return render(request, 'contact_box/search.html', {'form': self.class_form, 'groups': result})

