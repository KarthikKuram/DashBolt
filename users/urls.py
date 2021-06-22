from django.urls import path
from django.contrib.auth import views as auth_views
from users import views

urlpatterns = [
    path('',views.Login_page.as_view(), name='login_page'),
    path('register',views.Register_page.as_view(), name='register_page'),
    path('register_success',views.Register_success.as_view(), name='register_success'),
    path('logout',views.Logout_page.as_view(), name='logout_page'),
    path('password-reset',auth_views.PasswordResetView.as_view(template_name='users/password_reset.html',
                                                               subject_template_name='users/password_reset_subject.txt',
                                                               email_template_name='users/password_reset_email.html',
                                                               ),
         name='password_reset'),
    path('password-reset-done',auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete',auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    path('dashboard',views.Dashboard_page, name='dashboard'),
]