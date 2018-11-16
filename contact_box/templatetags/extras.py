#!/usr/bin/python3.7
from django import template

register = template.Library()


@register.filter(name='person_address_all')
def person_address_all(person):
    return person.addresses


@register.filter(name='person_address_first')
def person_address_first(person):
    temp = person.address_set.first()
    if temp is None:
        temp = ''
    else:
        city = temp.city
        if city is None:
            city = 'brak'
        else:
            city += ', '
        street = temp.street
        if street is None:
            street = 'brak'
        else:
            street += ', '
        street_number = temp.street_number
        if street_number is None:
            street_number = 'brak'
        else:
            street_number += ', '
        flat_number = temp.flat_number
        if flat_number is None:
            flat_number = ''
        else:
            flat_number += ', '
        temp = city + street + street_number + flat_number
    return temp


@register.filter(name='person_phonenumber_all')
def person_phone_number_all(person):
    return person.phonenumber_set.all()


@register.filter(name='person_phonenumber_first')
def person_phone_number_all(person):
    temp = person.phonenumber_set.first()
    if temp is None:
        temp = ''
    else:
        number = temp.phone_number
        type_num = temp.get_type_number_display()
        temp = str(number) + ', ' + str(type_num)
    return temp


@register.filter(name='person_email_all')
def person_email_all(person):
    return person.email_set.all()


@register.filter(name='person_email_first')
def person_email_all(person):
    temp = person.email_set.first()
    if temp is None:
        temp = ''
    else:
        email = temp.email_address
        type_email = temp.get_email_type_display()
        temp = email + ', ' + type_email
    return temp


@register.filter(name='locatorsAddress')
def address_persons(address):
    return len(address.person_set.all())


@register.filter(name='person_groups')
def person_groups(person):
    return person.group.all()
