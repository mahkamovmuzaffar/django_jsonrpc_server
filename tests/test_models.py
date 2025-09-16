from django.test import TestCase
from v1.models import Partner, AccessToken


class PartnerModelTests(TestCase):

# Create your tests here.
    def test_create_partner(self):
        user = Partner.objects.create_user(username="user1", password="secret")
        self.assertTrue(user.check_password("secret"))
        self.assertTrue(user.secret is not None)
        self.assertTrue(user.path_to_protected_zip.exists())

    def test_token_generation(self):
        user = Partner.objects.create_user(username="user2", password="test")
        token = AccessToken.objects.create(Partner=user)
        token.generate()
        self.assertTrue(token.key)
        self.assertIn("access_token", token.rpc_result()["result"])
