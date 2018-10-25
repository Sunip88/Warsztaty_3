from django.urls import path
from contact_box.views import *

urlpatterns = [
    path('search/', Home.as_view(), name='search'), # TODO: search site
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
]

