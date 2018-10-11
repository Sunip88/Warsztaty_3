from django.shortcuts import render, HttpResponse
from .models import Person
# Create your views here.


def home(request):
    persons = Person.objects.all()
    return render(request, 'contact_box/home.html', {'persons': persons})


def person_specifics(request, id_person):
    persons = Person.objects.all()
    person_spec = Person.objects.get(id=id_person)
    return render(request, 'contact_box/person_specs.html', {'persons': persons, 'person_spec': person_spec})