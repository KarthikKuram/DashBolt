from django.urls import path

from users import views

urlpatterns = [
    path('',views.Login_page.as_view(), name="login_page"),
    path('register',views.Register_page.as_view(), name="register_page"),
    path('dashboard',views.Dashboard_page, name="dashboard"),
    path('logout',views.Logout_page.as_view(), name="logout_page"),
]