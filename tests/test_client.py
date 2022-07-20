from django.test import Client, TestCase


# Test Server Responses
class ClientTest(TestCase):
    def test_index_redirect(self):
        client = Client()
        response = client.get('/')
        self.assertRedirects(response, '/login?next=/')

    def test_login_page(self):
        client = Client()
        response = client.get('/login?next=/')
        self.assertEqual(response.status_code, 200)

    def test_default_login(self):
        client = Client()
        response = client.post('/login?next=/', {'username': 'admin', 'password': 'scoreboard'})
        self.assertEqual(response.status_code, 200)

    def test_context(self):
        client = Client()
        response = client.post('/login?next=/', {'username': 'admin', 'password': 'scoreboard'})
        self.assertListEqual(response.context['BOARDS'], [])
        self.assertRegex(response.context['VERSION'], r'^v[0-9]+.[0-9]+.[0-9]+')
        self.assertIsNotNone(response.context['UPDATE'])
