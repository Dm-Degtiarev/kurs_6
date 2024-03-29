from django.contrib.auth import login
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView, \
    PasswordResetDoneView, PasswordResetCompleteView
from django.core.mail import send_mail
from django.forms import inlineformset_factory, modelformset_factory, BaseModelFormSet
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.conf import settings
from django.views.generic import TemplateView, CreateView, ListView, DetailView, DeleteView, UpdateView
from blog.models import Blog
from mailing.forms import UserAuthenticationForm, UserRegistartionForm, UserPasswordResetForm, UserResetConfirmForm, \
    MailingForm, MailingMessageForm, ClientForm, UserForm
from mailing.models import Mailing, MailingMessage, MailingTrying, Client, User
# from mailing.services import get_cache


class UserListView(PermissionRequiredMixin, ListView):
    model = User
    permission_required = 'mailing.setting_the_user_status'
    template_name = 'mailing/user/user_list.html'

class UserLoginView(LoginView):
    form_class = UserAuthenticationForm
    template_name = 'mailing/user/user_login.html'
    extra_context = {
        'title': 'Авторизация'
    }

    def get_success_url(self):
        return reverse_lazy('mailing:home')

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('mailing:login')

class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'mailing/user/user_update_form.html'
    success_url = reverse_lazy('mailing:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['title'] = f'Профиль | {self.object}'

        return context

class UserRegistrationView(CreateView):
    form_class = UserRegistartionForm
    template_name = 'mailing/user/user_registration.html'
    success_url = reverse_lazy('mailing:verify')
    extra_context = {
        'title': 'Регистрация'
    }

    def form_valid(self, form):
        responce = super().form_valid(form)
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        topic = 'Верификация Skychimp'
        message = f'Добрый день, {user.first_name}! Подтвердите свою учетную запись, перейдя по этой ссылке: ' \
                  f'http://37.143.12.161{reverse_lazy("mailing:verify_account", kwargs={"user_pk": user.pk})}.'
        from_email = settings.EMAIL_HOST_USER
        recipients = [user.email]
        send_mail(
            subject=topic,
            message=message,
            from_email=from_email,
            recipient_list=recipients,
            fail_silently=False
        )

        return responce


def verify_account(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    user.is_active = True
    user.save()
    login(request, user)
    return redirect(to=reverse('mailing:login'))

class UserVerificationView(TemplateView):
    template_name = 'mailing/user/user_registration_verify.html'
    extra_context = {
        'title': 'Верификация'
    }

class UserPasswordResetView(PasswordResetView):
    form_class = UserPasswordResetForm
    template_name = 'mailing/user/user_password_reset_form.html'
    success_url = reverse_lazy('mailing:password_reset_done')
    email_template_name = 'mailing/user/user_email_reset.html'
    from_email = settings.EMAIL_HOST_USER
    extra_context = {
        'title': 'Восстановление пароля'
    }

class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'mailing/user/user_password_reset_done.html'
    extra_context = {
        'title': 'Письмо отправлено'
    }

class UserPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = UserResetConfirmForm
    template_name = 'mailing/user/user_password_reset_confirm.html'
    success_url = reverse_lazy('mailing:password_reset_complete')
    extra_context = {
        'title': 'Новый пароль'
    }

class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'mailing/user/user_password_reset_complete.html'
    extra_context = {
        'title': 'Пароль изменен'
    }

class IndexView(TemplateView):
    template_name = 'mailing/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'
        context['total_mailings'] = Mailing.objects.count()
        context['total_active_mailings'] = Mailing.objects.filter(active_flg=True).count()
        context['unique_mailings_clients'] = Mailing.objects.values('client').distinct().count()
        context['three_random_blogs'] = Blog.objects.order_by('?')[:3]
        context['success_mailings'] = MailingTrying.objects.filter(status='success').count()
        context['error_mailings'] = MailingTrying.objects.filter(status='error').count()

        return context

class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'
    # queryset = get_cache(Mailing)
    extra_context = {
        'title': 'Рассылки'
    }

class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = MailingForm(instance=self.object)
        context['title'] = context['object']

        MailingMessageFormSet = inlineformset_factory(
            Mailing,
            MailingMessage,
            form=MailingMessageForm,
            extra=0,
            can_delete=False
        )
        if self.request.method == 'POST':
            context['formset'] = MailingMessageFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = MailingMessageFormSet(instance=self.object)

        return context


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_mailingmessage_formset.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        mailing = form.save()

        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            mailing.author = self.request.user
            mailing.save()

            return redirect(self.get_success_url())

        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Создать рассылку'
        MailingMessageFormSet = inlineformset_factory(
            Mailing,
            MailingMessage,
            form=MailingMessageForm,
            extra=1,
            can_delete=False
        )
        if self.request.method == 'POST':
            context_data['formset'] = MailingMessageFormSet(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = MailingMessageFormSet(instance=self.object)

        return context_data

class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Удалить | {context['object']}"

        return context

class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_mailingmessage_formset.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user

        if not user.has_perm('mailing.setting_the_mailing_status'):
            form.fields.pop('active_flg')
        else:
            form.fields = {'active_flg': form.fields['active_flg']}

        return form

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        mailing = self.get_object()
        MailingMessageFormSet = inlineformset_factory(
            Mailing,
            MailingMessage,
            form=MailingMessageForm,
            extra=0,
            can_delete=False
        )
        if self.request.method == 'POST':
            context_data['formset'] = MailingMessageFormSet(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = MailingMessageFormSet(instance=self.object)

        context_data['title'] = f'Изменить | {mailing.name}'

        return context_data

class ClientListView(ListView):
    model = Client
    form_class = ClientForm
    extra_context = {
        'title': 'Клиенты'
    }

class ClientDetailView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing/client_mailing_formset.html'
    success_url = reverse_lazy('mailing:client_list')

    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        client = self.object

        MailingFormSet = modelformset_factory(
            Mailing,
            form=MailingForm,
            extra=0,
            can_delete=False,
            formset=BaseModelFormSet
        )
        if self.request.POST:
            formset = MailingFormSet(
                self.request.POST,
                prefix='mailing',
                queryset=Mailing.objects.filter(client=client)
            )
        else:
            initial_data = [{'client': client}]
            formset = MailingFormSet(
                initial=initial_data,
                prefix='mailing',
                queryset=Mailing.objects.filter(client=client)
            )

        for form in formset.forms:
            form.fields['client'].initial = client

        context_data['formset'] = formset
        context_data['title'] = f'Редактирование | {client.fio}'

        return context_data

class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing/client_detail.html'
    success_url = reverse_lazy('mailing:client_list')
    extra_context = {
        'title': 'Создать клиента'
    }

    def form_valid(self, form):
        client = form.save()
        client.user = self.request.user
        client.author = self.request.user
        client.save()

        return super().form_valid(form)

class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:client_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Удалить: {context['object']}"

        return context

class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    success_url = reverse_lazy('mailing:client_list')
    template_name = 'mailing/client_detail.html'
    form_class = ClientForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client = self.get_object()
        context['title'] = f'Редактирование | {client.fio}'

        return context

class MailingReportView(LoginRequiredMixin, TemplateView):
    template_name = 'mailing/mailing_trying_report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Отчет по рассылкам'
        context['mailing_tryings'] = MailingTrying.objects.order_by('-trying_date', 'mailing').all()

        return context


@permission_required(perm='mailing.setting_the_user_status')
def set_user_status(request, pk):
    obj = get_object_or_404(User, pk=pk)
    if obj.is_superuser:
        return HttpResponseForbidden()
    if obj.is_active:
        obj.is_active = False
    else:
        obj.is_active = True
    obj.save()

    return redirect(request.META.get('HTTP_REFERER'))