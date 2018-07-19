from django.core import mail
from django.http import HttpResponse
from django.shortcuts import resolve_url as r
from django.test import TestCase
from django.test.utils import ContextList

from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


class SubscriptionsNewGet(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('subscriptions:new'))

    def test_get(self):
        """ GET /inscricao/ mus return status code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """ Must use subscriptions/subscription_form.html"""
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_html(self):
        """ Must contain input tags"""
        tags = (
            ('<form', 1),
            ('<input', 6),
            ('type="text"', 3),
            ('type="email"', 1),
            ('type="submit"', 1)
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)

    def test_csrf(self):
        """ Html must contain csrf"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_resp_is_httpresponse_instance(self):
        """ resp_is_httpresponse_instance """
        self.assertTrue(isinstance(self.resp, HttpResponse))

    def test_resp_instance_context(self):
        """ sefl.resp has context attr"""
        self.assertTrue(hasattr(self.resp, 'context'))

    def test_context_type(self):
        """ what is context ? """
        self.assertIsInstance(self.resp.context, ContextList)


#     def test_get_context_item(self):
#         self.assertTrue(self.resp.context.get('form'))
#
#     def test_has_form(self):
#         """ Context must have subscription form"""
#         form = self.resp.context['form']
#         self.assertIsInstance(form, SubscriptionForm)
#
#     def test_context_has(self):
#         """ Assert value in context """
#         self.assertTrue(hasattr(self.resp.context['form'], 'fields'))
#
#     def test_context_form_attr(self):
#         self.assertIn('name', self.resp.context['form'].fields)
#
#     def test_fields_type(self):
#         """ No arquivo forms fields é uma lista """
#         self.assertIsInstance(self.resp.context['form'].fields, OrderedDict)
#
#     def test_get_one_item_from_fields(self):
#         """ Pega um item presente em fields """
#         self.assertTrue(self.resp.context['form'].fields.get('name'))
#

class SubscriptionsNewPostValid(TestCase):
    def setUp(self):
        data = dict(name='Herbert Fortes', cpf='529.982.247-25', email='terberh@gmail.com',
                    phone='21-99921-6226')
        self.resp = self.client.post(r('subscriptions:new'), data)
        self.uuid_pk = Subscription.objects.first().uuid_pk

    def test_post(self):
        """ Valid POST should redirect to /inscricao/uuid/"""
        self.assertRedirects(self.resp, r('subscriptions:detail', self.uuid_pk))

    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_save_subscription(self):
        self.assertTrue(Subscription.objects.exists())


class SubscriptionsNewPostInvalid(TestCase):
    def setUp(self):
        self.resp = self.client.post(r('subscriptions:new'), {})

    def test_post(self):
        """ Invalid POST should not rediect"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_errors(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)

    def test_dont_save_subscription(self):
        self.assertFalse(Subscription.objects.exists())


class TemplateRegressionTest(TestCase):
    def test_template_has_non_field_errors(self):
        invalid_data = dict(name='Herbert Fortes', cpf='12345678901')
        response = self.client.post(r('subscriptions:new'), invalid_data)

        self.assertContains(response, '<ul class="errorlist nonfield">')

    def test_template_has_email_error(self):
        invalid_data = dict(name='Herbert Fortes', cpf='12345678901', email='asdf')
        response = self.client.post(r('subscriptions:new'), invalid_data)

        self.assertContains(response, '<ul class="errorlist"><li>Informe um endereço de email válido.</li></ul>')
