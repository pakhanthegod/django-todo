import unittest

from django.urls import reverse
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User

from todo.models import Item
from todo.forms import CustomSignupForm, CustomAuthForm


class ItemTest(TestCase):
    def create_item(self, text='Test text'):
        user = User.objects.create_user('test', 'test@example.com', 'test1234')
        item = Item.objects.create(user=user, text=text)

        return item

    def test_item_creation(self):
        item = self.create_item()
        self.assertTrue(isinstance(item, Item))


class GetTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_index(self):
        response = self.client.get(reverse('login'))

        self.assertEqual(response.status_code, 200)
    
    def test_signup(self):
        response = self.client.get(reverse('signup'))

        self.assertEqual(response.status_code, 200)
    
    def test_todo(self):
        response = self.client.get(reverse('todo:index'))

        self.assertEqual(response.status_code, 302)


class FormTest(TestCase):
    def create_item(self, text='Test text'):
        user = User.objects.create_user('test', 'test@example.com', 'test1234')
        item = Item.objects.create(user=user, text=text)

        return item

    def test_valid_signup_form(self):
        data = {
            'username': 'test',
            'password1': 'bear1234@',
            'password2': 'bear1234@',
        }
        form = CustomSignupForm(data)
        self.assertTrue(form.is_valid())

    def test_invalid_signup_form(self):
        data = {
            'username': 'test',
            'password1': 'bear1234',
            'password2': 'bear1234@',
        }
        form = CustomSignupForm(data)
        self.assertFalse(form.is_valid())

    def test_valid_login_form(self):
        user = User.objects.create_user('test', 'test@example.com', 'bear1234@')
        data = {
            'username': 'test',
            'password': 'bear1234@',
        }
        form = CustomAuthForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_login_form(self):
        data = {
            'username': 'test',
            'password': '',
        }
        form = CustomAuthForm(data=data)
        self.assertFalse(form.is_valid())
