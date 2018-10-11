from django.urls import path
from contact_box.views import *

urlpatterns = [
    path('home/', home, name='home'),
    path('person/<int:id_person>', person_specifics, name='person-specific')

]

