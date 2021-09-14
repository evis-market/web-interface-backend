from django.urls import path

from users import views


urlpatterns = [
    path('signup', views.SignupView.as_view(), name='signup'),
    # path('send_email_confirmation', SendConfirmEmailView.as_view(), name='send_email_confirmation'),
    # path('confirm_email', ConfirmEmailView.as_view(), name='confirm_email'),
    # path('send_reset_password_email', SendResetPasswordEmailView.as_view(), name='send_reset_password_email'),
    # path('set_password_by_secret_code', SetPasswordBySecretCodeView.as_view(), name='set_password_by_secret_code'),
]
