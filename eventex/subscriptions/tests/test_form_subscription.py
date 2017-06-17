from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm
from django.shortcuts import resolve_url as r

class SubscriptionFormTest(TestCase):
    def test_form_has_fields(self):
        """ Form must have 4 fields"""
        form = SubscriptionForm()
        expected = ['name', 'cpf', 'email', 'phone']
        self.assertSequenceEqual(expected, list(form.fields))

    def test_cpf_is_digit(self):
        """ CPF must only accept digits """
        form = self.make_validated_form(cpf='ABCD5678901')
        self.assertFormErrorCode(form, 'cpf', 'digits')

    def test_cpf_has_11_digits(self):
        """ CPF must have 11 digits """
        form = self.make_validated_form(cpf='1234')
        self.assertFormErrorCode(form, 'cpf', 'length')

    def test_name_must_be_capitalized(self):
        """ Name must be captalized """
        form = self.make_validated_form(name="HERBERT fortes")
        self.assertEqual('Herbert Fortes', form.cleaned_data['name'])

    def test_email_is_optional(self):
        """ Email is optinal """
        form = self.make_validated_form(email='')
        self.assertFalse(form.errors)

    def test_template_has_invalid_email(self):
        form = self.make_validated_form(email='asdf')
        #self.assertFormErrorMessage(form, 'email', 'Informe um endereço de email válido.')
        self.assertFormErrorCode(form, 'email', 'invalid')

    def test_phone_is_optional(self):
        """ Phone is optinal """
        form = self.make_validated_form(phone='')
        self.assertFalse(form.errors)

    def test_must_inform_phone_or_email(self):
        """ Email and Phone are optional, but one must be informed """
        form = self.make_validated_form(email='', phone='')
        self.assertListEqual(['__all__'], list(form.errors))

    def assertFormErrorCode(self, form, field, code):
        errors = form.errors.as_data()
        errors_list = errors[field]
        exception = errors_list[0]
        self.assertEqual(code, exception.code)

    def assertFormErrorMessage(self, form, field, msg):
         errors = form.errors
         errors_list = errors[field]
         self.assertListEqual([msg], errors_list)

    def make_validated_form(self, **kwargs):
        valid = dict(name='Herbert Fortes', cpf='12345678901',
                     email='terberh@gmail.com', phone='21-988881111')
        data = dict(valid, **kwargs)
        form = SubscriptionForm(data)
        form.is_valid()
        return form
