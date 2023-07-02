from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import IndexView, MailingListView, UserLoginView, UserRegistrationView, UserLogoutView, \
    UserPasswordResetView, UserPasswordResetDoneView, UserPasswordResetConfirmView, UserPasswordResetCompleteView, \
    MailingDetailView, MailingCreateView, MailingDeleteView, MailingUpdateView, ClientListView, ClientCreateView, \
    ClientDeleteView, ClientDetailView, ClientUpdateView, verify_account, UserVerificationView, UserUpdateView, \
    MailingReportView


app_name = MailingConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('report/', MailingReportView.as_view(), name='mailing_report'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('verification/', UserVerificationView.as_view(), name='verify'),
    path('verify/<int:user_pk>/', verify_account, name='verify_account'),
    path('profile/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('mailing/', MailingListView.as_view(), name='mailing_list'),
    path('mailing/create', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailing/delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('mailing/update/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('clients/', ClientListView.as_view(), name = 'client_list'),
    path('clients/create', ClientCreateView.as_view(), name = 'client_create'),
    path('clients/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    path('clients/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('password/reset/', UserPasswordResetView.as_view(), name='password_reset'),
    path('password/reset/done/', UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password/reset/confirm/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password/reset/complete/', UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
