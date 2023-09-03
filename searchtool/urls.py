from django.urls import path
from . import views
from . import url_handlers

urlpatterns = [
    path("database_index/", views.DatabaseIndex.as_view(), name="database_index"),
    path("<int:pk>/database_detail/", views.CurrentDatabase.as_view(), name="database_detail"),
    path("create_database/", views.CreateDatabase.as_view(), name="create_database"),
    path("<int:pk>/edit/", views.EditDatabase.as_view(), name="edit_database"),
    path("registration/", views.UserViewRegister.as_view(), name="registration"),
    path("login/", views.UserViewLogin.as_view(), name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("", url_handlers.index_handler),
]