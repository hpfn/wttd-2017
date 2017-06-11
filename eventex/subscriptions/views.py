from django.conf import settings
from django.core import mail
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template.loader import render_to_string

from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


def subscribe(request):
    if request.method == 'POST':
        return create(request)
    else:
        return new(request)


def create(request):
    form = SubscriptionForm(request.POST)
    if not form.is_valid():
        return render(request, 'subscriptions/subscription_form.html', {'form': form})

    subscription = Subscription.objects.create(**form.cleaned_data)

    _send_mail(
        'subscriptions/subscription_email.txt',
        {'subscription': subscription},
        'Confirmação de Inscrição',
        settings.DEFAULT_FROM_EMAIL,
        subscription.email
    )

    return HttpResponseRedirect('/inscricao/{}/'.format(subscription.pk))


def new(request):
    context = {'form': SubscriptionForm()}
    return render(request, 'subscriptions/subscription_form.html', context)

def detail(request, pk):
    try:
        subscription = Subscription.objects.get(pk=pk)
    except Subscription.DoesNotExist:
        raise Http404
    except ValidationError:
        raise Http404

    return render(request, 'subscriptions/subscription_detail.html',
                  {'subscription': subscription} )


def _send_mail(template_name, context, subject, from_, to_):
    body = render_to_string(template_name, context)
    mail.send_mail(subject, body, from_, [from_, to_])
