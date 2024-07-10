from allauth.account.adapter import DefaultAccountAdapter
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .tasks import send_email_task


class MyAccountAdapter(DefaultAccountAdapter):
    def send_mail(self, template_prefix, email, context):
        subject = render_to_string(f'{template_prefix}_subject.txt', context).strip()
        body = render_to_string(f'{template_prefix}_message.txt', context)
        body_text = strip_tags(body)
        from_email = 'sportgoodsstore.my@gmail.com'
        send_email_task.delay(subject, body_text, from_email, [email])
