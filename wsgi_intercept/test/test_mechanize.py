from urllib.error import URLError
from wsgi_intercept import testing
from wsgi_intercept.testing import unittest
from wsgi_intercept.test import base

try:
    import mechanize
    has_mechanize = True
except ImportError:
    has_mechanize = False
_skip_message = "mechanize is not installed"


@unittest.skipUnless(has_mechanize, _skip_message)
class MechanizeHttpTestCase(base.BaseTestCase):
    port = 80

    def setUp(self):
        super(MechanizeHttpTestCase, self).setUp()
        from wsgi_intercept.mechanize_intercept import install
        from wsgi_intercept.mechanize_intercept import uninstall
        install()
        self.addCleanup(uninstall)

    def make_one(self, *args):
        from mechanize import Browser
        return Browser(*args)

    def test_intercepted(self):
        b = self.make_one()
        b.open(self.url)
        self.assertTrue(testing.success())

    @unittest.skipIf(*testing.funky_dns_resolution)
    def test_intercept_removed(self):
        from wsgi_intercept import remove_wsgi_intercept
        remove_wsgi_intercept()
        b = self.make_one()
        with self.assertRaises(URLError):
            b.open(self.url)


@unittest.skipUnless(has_mechanize, _skip_message)
class MechanizeHttpsTestCase(MechanizeHttpTestCase):
    port = 443
