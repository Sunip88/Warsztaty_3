from django.db import models
from PIL import Image


class Person(models.Model):
    name = models.CharField(max_length=32)
    surname = models.CharField(max_length=32)
    description = models.TextField(null=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.name} {self.surname} Profile'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Address(models.Model):
    city = models.CharField(max_length=64)
    street = models.CharField(max_length=64)
    street_number = models.CharField(max_length=8)
    flat_number = models.CharField(max_length=8, null=True)
    persons = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.city}, {self.street}, {self.street_number}, {self.flat_number}'


class PhoneNumber(models.Model):
    TYPE_NUMBER_CHOICES = [
        (0, 'Mobile'),
        (1, 'Work'),
        (2, 'Home'),
        (3, 'Work Fax'),
        (4, 'Home Fax'),
        (5, 'Other')
    ]

    phone_number = models.PositiveIntegerField()
    type_number = models.IntegerField(choices=TYPE_NUMBER_CHOICES)
    persons = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.phone_number}, {self.type_number}'


class Email(models.Model):
    EMAIL_TYPE_CHOICES = [
        (0, 'Home'),
        (1, 'Work'),
        (2, 'Other')
    ]

    email_address = models.EmailField(max_length=70)
    email_type = models.IntegerField(choices=EMAIL_TYPE_CHOICES)
    persons = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.email_address}, {self.email_type}'


class Groups(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(null=True)
    persons = models.ManyToManyField(Person, related_name='group')

    def __str__(self):
        return f'{self.title}'
