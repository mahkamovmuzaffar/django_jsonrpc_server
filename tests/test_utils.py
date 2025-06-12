from django.test import TestCase
from v1.utils.base_utils import card_mask


class MaskUtilsTest(TestCase):
    def test_card_mask_basic(self):
        result = card_mask("8600123412341234")
        self.assertEqual(result, "860012xxxxxx1234")
