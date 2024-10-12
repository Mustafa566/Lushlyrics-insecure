from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.default, name='default'),
    path("playlist/", views.playlist, name='your_playlists'),
    path("search/", views.search, name='search_page'),
    path("login/", views.login_view, name='login'),
    path("signup/", views.signup, name='signup'),
    path("logout/", views.logout_view, name='logout')
]