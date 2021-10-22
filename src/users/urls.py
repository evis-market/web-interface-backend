from django.urls import path

from users import views


urlpatterns = [
    path('signup', views.SignupView.as_view(), name='signup'),
    path('send_email_confirmation', views.SendConfirmationEmailView.as_view(), name='send_confirmation_email'),
    path('my/profile', views.UserProfileView.as_view(), name='get_logged_in_user_profile'),
    path('my/password', views.UserUpdatePasswordView.as_view(), name='change_logged_in_user_password'),
    path('confirm_email', views.ConfirmEmailView.as_view(), name='confirm_email'),
    path('send_reset_password_email', views.SendResetPasswordEmailView.as_view(), name='send_reset_password_email'),
    path('set_password_by_secret_code', views.SetPasswordBySecretCodeView.as_view(),
         name='set_password_by_secret_code'),
]
