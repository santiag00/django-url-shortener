from django.test import TestCase
from api.models import ShortURL, TargetDevice
import shortuuid
import json


class URLShortenerTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.joor_uuid = shortuuid.uuid()
        cls.joor_short_url = ShortURL.objects.create(
            short_url=cls.joor_uuid,
            target_url="http://facebook.com"
        )
        TargetDevice.objects.create(
            url="http://m.facebook.com",
            device_type=TargetDevice.MOBILE,
            short_url=cls.joor_short_url
        )

    def test_api_can_shorten_url(self):
        params = {
            'data': {
                'url': 'http://www.example.com',
                'devices': {
                    'mobile': 'http://m.example.com'
                }
            }
        }
        response = self.client.post('/api/', json.dumps(params), content_type="application/json")
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content.decode('utf8'))
        self.assertIsInstance(result['data']['short_url'], type(shortuuid.uuid()))

    def test_api_can_return_urls(self):
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content.decode('utf8'))
        self.assertEqual(len(result['data']), 1)

    def test_api_can_redirect(self):
        response = self.client.get('/{0}/'.format(self.joor_uuid))
        self.assertEqual(response.status_code, 302)
