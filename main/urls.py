from django.urls import path
from django.contrib.auth import views as auth_views
from .views import signup_view, login_view, ticket_view, index, delete_ticket
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='index'),
    path('signup/', views.signup_view, name='signup'),
    path('tickets/', ticket_view, name='tickets'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add-ticket/', views.add_ticket, name='add-ticket'),
    path('tickets/edit/<int:ticket_id>/', views.edit_ticket, name='edit'),
    path('tickets/delete/<int:ticket_id>/', delete_ticket, name='delete_ticket'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)