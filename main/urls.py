from django.urls import path
from main.views import show_main, create_shoes, show_shoes, show_xml, \
    show_json, show_xml_by_id, show_json_by_id, register, login_user, \
    logout_user, edit_shoes, delete_shoes

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-shoes/', create_shoes, name='create_shoes'),
    path('shoes/<str:id>/', show_shoes, name='show_shoes'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:shoes_id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:shoes_id>/', show_json_by_id, name='show_json_by_id'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('shoes/<uuid:id>/edit', edit_shoes, name='edit_shoes'),
    path('shoes/<uuid:id>/delete', delete_shoes, name='delete_shoes'),
]