from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("addData", views.addData, name="addData"),
    path("saveData", views.saveData, name="saveData"),
    path("editData/<int:id>", views.editData, name="editData"),
]