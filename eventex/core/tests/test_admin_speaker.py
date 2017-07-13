from unittest.mock import Mock

from django.test import TestCase
from eventex.core.admin import Speaker, SpeakerModelAdmin
from eventex.core.admin import Contact
from eventex.core.admin import admin


class SpeakerModelAdminTest(TestCase):
    def setUp(self):
        self.speaker = Speaker.objects.create(
            name='Arnaldinho',
            slug='arnaldinho',
            website='http://hbn.link/arnaldinho-site',
            photo='http://hbn.link/arnaldinho-pic',
            description='alien do evento'
        )
        Contact.objects.create(
            speaker=self.speaker,
            kind='P',
            value='21-988881111'
        )
        Contact.objects.create(
            speaker=self.speaker,
            kind='E',
            value='arnaldinho@email.com'
        )

        self.model_admin = SpeakerModelAdmin(Speaker, admin.site)
        self.queryset = Speaker.objects.all()

    def test_create(self):
        self.assertTrue(Speaker.objects.exists())

    def test_list_display(self):
        list_display = ['name', 'photo_img', 'website_link',
                        'email', 'phone']
        self.assertEqual(list_display, self.model_admin.list_display)

    def test_website_link(self):
         link = '<a href="{0}">{0}</a>'.format('http://hbn.link/arnaldinho-site')
         self.assertEqual(link, self.model_admin.website_link(self.queryset[0]))

    def test_photo_img(self):
        photo_img = '<img width="32px" src={} />'.format('http://hbn.link/arnaldinho-pic')
        self.assertEqual(photo_img, self.model_admin.photo_img(self.queryset[0]))

    def test_phone(self):
        self.assertEqual('21-988881111', self.model_admin.phone(self.queryset[0]).value)

    def test_email(self):
        self.assertEqual('arnaldinho@email.com', self.model_admin.email(self.queryset[0]).value)