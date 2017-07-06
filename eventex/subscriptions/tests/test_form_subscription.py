from django.test import TestCase

from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.validators import validate_cpf


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

    def test_cpf_has_size_11_or_14(self):
        """ CPF must have size 11 or 14 """
        cpfs = ['123456789', '1234567890123']
        for cpf in cpfs:
            with self.subTest():
                form = self.make_validated_form(cpf=cpf)
                self.assertFormErrorCode(form, 'cpf', 'length')

        form = self.make_validated_form(cpf='123.456.789-123')
        self.assertFormErrorCode(form, 'cpf', 'max_length')

    def test_valid_digits_only_numbers(self):
        cpf = '52998224725'
        self.assertTrue(validate_cpf(cpf))

    def test_valid_digits_dot_hyphen(self):
        cpf = '529.982.247-25'
        self.assertTrue(validate_cpf(cpf))

    def test_check_repeated_number(self):
        form = self.make_validated_form(cpf=99999999999)
        self.assertFormErrorCode(form, 'cpf', 'rep_num')

    def test_sequencial_number(self):
        form = self.make_validated_form(cpf='123.456.789-12')
        self.assertFormErrorCode(form, 'cpf', 'invalid')

    def test_name_must_be_capitalized(self):
        """ Name must be captalized """
        form = self.make_validated_form(name="HERBERT fortes")
        self.assertEqual('Herbert Fortes', form.cleaned_data['name'])

    def test_email_is_optional(self):
        """ Email is optinal """
        form = self.make_validated_form(email='', cpf='52998224725')
        self.assertFalse(form.errors)

    def test_template_has_invalid_email(self):
        form = self.make_validated_form(email='asdf')
        # self.assertFormErrorMessage(form, 'email', 'Informe um endereço de email válido.')
        self.assertFormErrorCode(form, 'email', 'invalid')

    def test_phone_is_optional(self):
        """ Phone is optinal """
        form = self.make_validated_form(phone='', cpf='52998224725')
        self.assertFalse(form.errors)

    def test_must_inform_phone_or_email(self):
        """ Email and Phone are optional, but one must be informed """
        form = self.make_validated_form(email='', phone='', cpf='52998224725')
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
