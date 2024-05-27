from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver

from simpleapp.models import New, Article


@receiver(post_save, sender=New)
def new_created(instance, created, **kwargs):
    if not created:
        return

    emails = User.objects.filter(
        subscriptions__author=instance.author
    ).values_list('email', flat=True)

    subject = f'Свежая новость в категории {instance.author}'

    text_content = (
        f'Новость: {instance.title}\n'
        f'Автор: {instance.author}\n\n'
        f'Ссылка на новость: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )
    html_content = (
        f'Новость: {instance.title}<br>'
        f'Автор: {instance.author}<br><br>'
        f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
        f'Ссылка на новость</a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@receiver(post_save, sender=Article)
def article_created(instance, created, **kwargs):
    if not created:
        return

    emails = User.objects.filter(
        subscriptions__author=instance.author
    ).values_list('email', flat=True)

    subject = f'Свежая статья в категории {instance.author}'

    text_content = (
        f'Статья: {instance.title}\n'
        f'Автор: {instance.author}\n\n'
        f'Ссылка на статью: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )
    html_content = (
        f'Статья: {instance.title}<br>'
        f'Автор: {instance.author}<br><br>'
        f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
        f'Ссылка на статью</a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()