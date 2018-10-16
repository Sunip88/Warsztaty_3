from django.urls import path
from contact_box.views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('show/<int:id_person>', ShowSpecific.as_view(), name='person-specific'),
    path('new/', NewPerson.as_view(), name='person-add'),
    path('show/', Show.as_view(), name='show-all'),
    path('modify/<int:person_id>/', EditPerson.as_view(), name='modify-person'),

]

