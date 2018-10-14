from django.urls import path
from contact_box.views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('show/<int:id_person>', Show.as_view(), name='person-specific'),
    path('new/', NewPerson.as_view(), name='person-add'),

]

