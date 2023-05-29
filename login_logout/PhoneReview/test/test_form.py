from django.test import TestCase
from addgame.forms import UserForm
class TestRegistrationForm(TestCase):
def test_registration_form_valid(self):
valid_data = {
    "userName":"user1",
    "password": "secret",
}
form = UserForm(data=valid_data)
form.is_valid()
self.assertFalse(form.errors)
def test_registration_form_invalid(self):
invalid_data = {
    "username":"user1",
    "email": "user@mail.com",
    "password": "secret",
}
form = UserForm(data=invalid_data)
form.is_valid()
self.assertTrue(form.errors, msg="Gmail only")