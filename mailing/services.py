import schedule
from django.core.cache import cache
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from mailing.models import Mailing, MailingTrying, MailingMessage
from datetime import datetime, timedelta


def check_date(target_date, days):
    current_date = timezone.now()
    difference = current_date - target_date
    if difference > timedelta(days=days):
        return True
    else:
        return False


def create_mailing_dict(mail, topic, text):
    return {'mail': mail, 'topic': topic, 'text': text}


def send_message():
    mailing_list = create_mailing_list()

    if mailing_list:
        try:
            for mailing in mailing_list:
                send_mail(
                    subject=mailing['topic'],
                    message=mailing['text'],
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=mailing['recipients'],
                    fail_silently=False
                )

            MailingTrying.objects.create(
                trying_date=timezone.now(),
                mailing_id=mailing['mailing_id'],
                status='success',
                server_response='Отправлено'
            )

        except Exception as _ex:
            MailingTrying.objects.create(
                trying_date=timezone.now(),
                mailing_id=mailing['mailing_id'],
                status='error',
                server_response=str(_ex)
            )


def create_mailing_list():
    mailing_list = []
    mailings = Mailing.objects.filter(status='launched', active_flg=True)

    for mailing in mailings:
        if mailing.time <= datetime.now().time():
            messages = MailingMessage.objects.filter(mailing=mailing)
            for message in messages:
                message_topic = message.topic
                message_text = message.text

                last_try = MailingTrying.objects.filter(mailing=mailing, status='success').last()
                if last_try is None or check_date(last_try.trying_date, mailing.regularity):
                    mailing_dict = {
                        'mailing_id': mailing.id,
                        'topic': message_topic,
                        'text': message_text,
                        'recipients': []
                    }

                    clients = mailing.client.all()
                    for client in clients:
                        mailing_dict['recipients'].append(client.email)

                    mailing_list.append(mailing_dict)

    return mailing_list


def run_scheduler():
    schedule.every(10).seconds.do(send_message)


# CACHE FUNCS
def get_cache(model):
    queryset = model.objects.all()
    if settings.CACHE_ENABLE:
        key = 'mailing_cache'
        cache_model = cache.get(key)
        if cache_model is None:
            cache_model = queryset
            cache.set(key, cache_model)
        return cache_model
    return queryset