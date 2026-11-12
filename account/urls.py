from django.urls import path ,reverse_lazy
from . import views
from django.contrib.auth import views as auth_view
app_name = "accounts"

urlpatterns = [
    path('login/',views.login_user,name="login"),
    path('register/',views.register_user,name='register'),
    path("verify/code",views.verify_code,name="verify_code"),
    path('logout/',views.logout_user,name="logout"),
    #reset password
    path('password/reset/',auth_view.PasswordResetView.as_view(template_name="account/reset_password_view.html",success_url=reverse_lazy("accounts:password_reset_done"),email_template_name='account/password_reset_email.html'),name="password_reset"),
    path('password/reset/confrim/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name="account/password_reset_confirm.html",success_url=reverse_lazy("accounts:password_reset_complete")),name="password_reset_confirm"),
    path('password/reset/done/',auth_view.PasswordResetDoneView.as_view(template_name="account/reset_password_done.html",),name="password_reset_done"),
    path('reset/done/',auth_view.PasswordResetCompleteView.as_view(template_name="account/reset_password_complet.html",),name="password_reset_complete")
    
]
