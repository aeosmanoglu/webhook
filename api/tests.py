from django.test import TestCase, Client
from django.urls import reverse


# Create your tests here.
class HookTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('hook')

    def test_hook_endpoint_with_valid_request(self):
        # Geçerli bir istek hazırla
        appname = 'myapp'
        ids = ['1', '2', '3']
        payload = {'message': 'Test message'}
        query_string = 'appname={}&ids={}'.format(appname, '&id='.join(ids))
        headers = {'content-type': 'application/json'}
        print('{}?{}'.format(self.url, query_string))

        # Endpoint'e isteği gönder ve yanıtı kontrol et
        response = self.client.post('{}?{}'.format(self.url, query_string), payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'success': 'Message send'})

    def test_hook_endpoint_with_invalid_request(self):
        # Geçersiz bir istek hazırla
        payload = {}
        query_string = 'appname=myapp'
        headers = {'content-type': 'application/json'}

        # Endpoint'e isteği gönder ve yanıtı kontrol et
        response = self.client.post('{}?{}'.format(self.url, query_string), payload, **headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'error': 'at least one id is required'})

    def test_hook_endpoint_with_missing_appname(self):
        # Geçersiz bir istek hazırla
        payload = {'message': 'Test message'}
        query_string = 'id=1'
        headers = {'content-type': 'application/json'}

        # Endpoint'e isteği gönder ve yanıtı kontrol et
        response = self.client.post('{}?{}'.format(self.url, query_string), payload, **headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'error': 'appname is required'})

    def test_hook_endpoint_with_invalid_method(self):
        # Geçersiz bir istek hazırla
        payload = {'message': 'Test message'}
        query_string = 'appname=myapp&id=1'
        headers = {'content-type': 'application/json'}

        # Endpoint'e isteği gönder ve yanıtı kontrol et
        response = self.client.get('{}?{}'.format(self.url, query_string), payload, **headers)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json(), {'error': 'Method Not Allowed'})
