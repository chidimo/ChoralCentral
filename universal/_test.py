"""tests"""

from django.template.defaultfilters import slugify

from django.test import TestCase

from .models_tests import AutoSlug, AutoMultipleSlug

class AutoSlugFieldTests(TestCase):

    def setUp(self):
        """
        Create an instance of the model without saving
        """
        self.instance = AutoSlug(name="Test auto slug field")

    def test_slug_field_value_a_correct(self):
        """Test slug field has expected value"""
        self.instance.save()
        self.assertEqual(self.instance.slug, slugify("Test auto slug field"))

    def test_slug_field_value_b_remain_unchanged_when_name_change(self):
        """Slug field value remain unchanged even if name changes"""
        self.instance.set_once = True
        self.instance.save()
        self.assertEqual(self.instance.slug, slugify("Test auto slug field"))

        self.instance.name = "Name has changed"
        self.instance.save()

        self.assertEqual(self.instance.name, "Name has changed")
        self.assertEqual(self.instance.slug, slugify("Test auto slug field"))

    def test_slug_field_value_c_changed_with_set_once_false(self):
        """Slug field value changed with name field value change when 'set_once' is False"""
        self.instance.save()
        self.assertTrue(self.instance._meta.get_field("slug").set_once)

        self.instance._meta.get_field("slug").set_once = False
        self.instance.name = "Name has changed"
        self.instance.save()

        self.assertFalse(self.instance._meta.get_field("slug").set_once)
        self.assertEqual(self.instance.slug, slugify("Name has changed"))

    def test_slug_field_value_d_only_accepts_boolean(self):
        """Test that 'set_once' attribute only accepts boolean values"""
        pass

    def test_slug_field_with_blank_set_using_field(self):
        """Test that slug is reset once formerly blank field takes on a value"""
        new = AutoSlug(name="")
        new.save()
        self.assertEqual("", new.name)
        new.name = "Assign name"
        new.save()
        # print(new._meta.get_field("slug").set_once)
        self.assertEqual(new.slug, slugify("Assign name"))

class AutoMultipleSlugFieldTests(TestCase):
    def setUp(self):
        self.instance = AutoMultipleSlug(
            name="Auto multiple slug field",
            url="https://www.somto.com")

    def test_slug_field_value_a_correct(self):
        """Test slug field has expected value"""
        self.instance.save()
        self.assertEqual(self.instance.slug, slugify(
            " ".join(["Auto multiple slug field", "https://www.somto.com"])
            ))

    def test_slug_field_value_b_remain_unchanged_on_field_change(self):
        """Slug field value remain unchanged even if other fields change"""
        self.instance.save()
        self.assertEqual(self.instance.slug, slugify(
            " ".join(["Auto multiple slug field", "https://www.somto.com"])
            ))

        self.instance.name="Name has changed"
        self.instance.url = "https://www.django-bible.com"
        self.instance.save()

        self.assertEqual(self.instance.name, "Name has changed")
        self.assertEqual(self.instance.url, "https://www.django-bible.com")

        self.assertEqual(self.instance.slug, slugify(
            " ".join(["Auto multiple slug field", "https://www.somto.com"])
            ))

    def test_slug_field_value_c_changed_with_set_once_false(self):
        """Slug field value changed with name field value change when 'set_once' is False"""
        self.instance.save()
        self.assertTrue(self.instance._meta.get_field("slug").set_once)

        self.instance._meta.get_field("slug").set_once = False
        self.assertFalse(self.instance._meta.get_field("slug").set_once)

        self.instance.name = "Name has changed"
        self.instance.url = "https://www.django-bible.com"
        self.instance.save()

        self.assertEqual(self.instance.name, "Name has changed")
        self.assertEqual(self.instance.url, "https://www.django-bible.com")

        self.assertEqual(self.instance.slug, slugify(
            " ".join(["Name has changed", "https://www.django-bible.com"])
            ))
