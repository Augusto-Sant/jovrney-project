from django.urls import path

from . import views


app_name = "accounts"

urlpatterns = [
    path("register/",views.register_view,name="register_view"),
    path("login/",views.user_login,name="login_view"),
    path('logout/',views.user_logout,name="logout"),
    path('profile/',views.ProfileView.as_view(),name="profile_view")
]