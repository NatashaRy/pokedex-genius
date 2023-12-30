from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from .models import pokedexUser
from .forms import UserProfileForm
from django.urls import reverse


# Model tests
class UserModelTestCase(TestCase):
    def setUp(self):
        self.user = pokedexUser.objects.create_user(username='testuser',
                                                    password='password')

    def test_user_creation(self):
        """Test that a user is created successfully."""
        self.assertEqual(self.user.username, 'testuser')

    def test_user_str_representation(self):
        """Test the __str__ method of the user model."""
        self.assertEqual(str(self.user), 'testuser')


# Views tests
class ProfileViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = pokedexUser.objects.create(username='testuser')
        self.client.login(username='testuser', password='password')

    def test_profile_view_accessible(self):
        """Test that the profile view is accessible."""
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_profile_view_content(self):
        """Test the content displayed on the profile view."""
        response = self.client.get(reverse('profile'))
        self.assertContains(response, 'Welcome to Your Profile')


class UpdateProfileViewTestCase(TestCase):
    def test_update_profile_view_accessible(self):
        """Test that the update profile view is accessible."""
        response = self.client.get(reverse('update_profile'))
        self.assertEqual(response.status_code, 200)


# Form tests
class UserProfileFormTest(TestCase):
    def test_valid_data(self):
        form_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'date_of_birth': '1990-01-01',
            'website_url': 'https://example.com',
            'bio': 'Test bio',
            'go_trainer_id': '1234567890',
        }
        form = UserProfileForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        form = UserProfileForm(data={})
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)  # Form should have errors


# Integration tests
class ProfileIntegrationTestCase(TestCase):
    def test_update_profile(self):
        """Test updating the user's profile."""
        User = get_user_model()
        user = User.objects.create(username='testuser',
                                   password='password')
        self.client.login(username='testuser',
                          password='password')

        form_data = {
            'date_of_birth': '1990-01-01',
            'website_url': 'https://example.com',
            'bio': 'A test bio.',
        }
        response = self.client.post(reverse('update_profile'), data=form_data)

        # Verify that the user's profile has been updated
        updated_user = User.objects.get(username='testuser')
        self.assertEqual(updated_user.date_of_birth, '1990-01-01')
        self.assertEqual(updated_user.website_url, 'https://example.com')
        self.assertEqual(updated_user.bio, 'A test bio.')

        # Verify the response status and redirection
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('profile'))
