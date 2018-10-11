#!/usr/bin/python3.7
from django import template

register = template.Library()


@register.filter(name='person_address_all')
def movie_genre_all(person):
    return person.address_set.all()


@register.filter(name='person_phonenumber_all')
def movie_genre_all(person):
    return person.phonenumber_set.all()


@register.filter(name='person_email_all')
def movie_genre_all(person):
    return person.email_set.all()
