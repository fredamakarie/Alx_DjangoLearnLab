from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class AuthAndProfileTests(TestCase):
    def setUp(self):
        self.username = "testuser"
        self.password = "SecretPass123!"
        self.user = User.objects.create_user(username=self.username, password=self.password, email='test@example.com')

    def test_registration_creates_user_and_hashes_password(self):
        client = Client(enforce_csrf_checks=True)
        # GET to get CSRF cookie
        resp = client.get(reverse('register'))
        self.assertEqual(resp.status_code, 200)
        csrftoken = resp.cookies['csrftoken'].value

        reg_data = {
            'username': 'newuser',
            'password1': 'NewStrongPass!234',
            'password2': 'NewStrongPass!234',
            'csrfmiddlewaretoken': csrftoken
        }
        resp2 = client.post(reverse('register'), reg_data, follow=True)
        # registration usually redirects -> allow 200/302, check user exists
        self.assertTrue(User.objects.filter(username='newuser').exists())
        new_user = User.objects.get(username='newuser')
        self.assertTrue(new_user.check_password('NewStrongPass!234'))
        # Ensure password is not stored in plain text
        self.assertNotEqual(new_user.password, 'NewStrongPass!234')

    def test_registration_fails_without_csrf(self):
        client = Client(enforce_csrf_checks=True)
        resp = client.post(reverse('register'), {
            'username': 'nocsrf',
            'password1': 'a',
            'password2': 'a'
        })
        self.assertEqual(resp.status_code, 403)

    def test_login_requires_csrf_and_works_with_csrf(self):
        client = Client(enforce_csrf_checks=True)
        resp = client.get(reverse('login'))
        self.assertEqual(resp.status_code, 200)
        csrftoken = resp.cookies['csrftoken'].value

        login_data = {
            'username': self.username,
            'password': self.password,
            'csrfmiddlewaretoken': csrftoken
        }
        resp2 = client.post(reverse('login'), login_data, follow=True)
        # after login, the test client will have session auth
        user = resp2.context.get('user')
        # If redirect to a page without context, check session
        if user:
            self.assertTrue(user.is_authenticated)
        else:
            self.assertTrue('_auth_user_id' in client.session)

    def test_login_fails_without_csrf(self):
        client = Client(enforce_csrf_checks=True)
        resp = client.post(reverse('login'), {'username': self.username, 'password': self.password})
        self.assertEqual(resp.status_code, 403)

    def test_logout_logs_out_user(self):
        client = Client()
        client.login(username=self.username, password=self.password)  # helper bypasses CSRF
        # Ensure session has user
        self.assertIn('_auth_user_id', client.session)
        resp = client.get(reverse('logout'), follow=True)
        # After logout, session should not have auth id
        self.assertNotIn('_auth_user_id', client.session)

    def test_profile_edit_requires_login(self):
        client = Client()
        resp = client.get(reverse('profile-edit'))
        # not logged in -> redirect to login
        self.assertEqual(resp.status_code, 302)
        self.assertIn(reverse('login'), resp.url)

    def test_profile_edit_updates_data_and_requires_csrf(self):
        client = Client(enforce_csrf_checks=True)
        # log in user (login bypasses CSRF checks for convenience)
        client.login(username=self.username, password=self.password)
        resp = client.get(reverse('profile-edit'))
        self.assertEqual(resp.status_code, 200)
        csrftoken = resp.cookies['csrftoken'].value

        post_data = {
            'first_name': 'UpdatedName',
            'last_name': 'UpdatedLast',
            'email': 'updated@example.com',
            'csrfmiddlewaretoken': csrftoken
        }
        resp2 = client.post(reverse('profile-edit'), post_data, follow=True)
        self.assertEqual(resp2.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'UpdatedName')
        self.assertEqual(self.user.email, 'updated@example.com')

    def test_profile_edit_fails_without_csrf(self):
        client = Client(enforce_csrf_checks=True)
        client.login(username=self.username, password=self.password)
        resp = client.post(reverse('profile-edit'), {'first_name': 'X'})
        self.assertEqual(resp.status_code, 403)

    def test_forms_contain_csrf_input(self):
        client = Client()
        # registration page
        resp = client.get(reverse('register'))
        self.assertContains(resp, 'csrfmiddlewaretoken')
        # login page
        resp2 = client.get(reverse('login'))
        self.assertContains(resp2, 'csrfmiddlewaretoken')
        # profile-edit (must be logged in)
        client.login(username=self.username, password=self.password)
        resp3 = client.get(reverse('profile-edit'))
        self.assertContains(resp3, 'csrfmiddlewaretoken')
