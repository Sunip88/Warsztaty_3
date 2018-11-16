from django.urls import path
from contact_box.views import *

urlpatterns = [
    path('search/', SearchGroup.as_view(), name='search'),
    path('show/<int:id_person>', ShowSpecific.as_view(), name='person-specific'),
    path('new/', NewPerson.as_view(), name='person-add'),
    path('', Show.as_view(), name='show-all'),
    path('modify/<int:person_id>/', EditPerson.as_view(), name='modify-person'),
    path('delete/<int:person_id>/', delete_person, name='delete-person'),
    path('groups/', ShowGroups.as_view(), name='show-all-groups'),
    path('new_group/', NewGroup.as_view(), name='group-add'),
    path('show_group/<int:id_group>', ShowSpecificGroup.as_view(), name='group-specific'),
    path('modify_group/<int:group_id>/', EditGroup.as_view(), name='modify-group'),
    path('delete_group/<int:group_id>/', delete_group, name='delete-group'),
    path('address/', Addresses.as_view(), name='show-all-address'),
    path('delete_address/<int:address_id>/', delete_address, name='delete-address'),
    path('new_address/', NewAddresses.as_view(), name='address-add'),
    path('modify_address/<int:address_id>/', EditAddress.as_view(), name='modify-address'),
    path('show_persons_address/<int:address_id>/', ShowPersonAddress.as_view(), name='show-persons-address'),
]
