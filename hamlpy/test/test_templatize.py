from __future__ import unicode_literals

import unittest

from hamlpy import Config


class TemplatizeTest(unittest.TestCase):

    def test_templatize(self):
        # patching of Django's templatize happens when our app is loaded
        Config.ready(None)

        from django.utils.translation import templatize

        # test regular Django tags
        output = templatize('{% trans "Foo" %}{% blocktrans %}\nBar\n{% endblocktrans %}', origin='test.html')
        self.assertRegexpMatches(output, r"gettext\(u?'Foo'\)")
        self.assertRegexpMatches(output, r"gettext\(u?'\\nBar\\n'\)")

        # test Haml tags with HTML origin
        output = templatize('- trans "Foo"\n- blocktrans\n  Bar\n', origin='test.haml')
        self.assertRegexpMatches(output, r"gettext\(u?'Foo'\)")
        self.assertRegexpMatches(output, r"gettext\(u?'\\n  Bar\\n'\)")

        # test Haml tags and HTML origin
        self.assertNotIn('gettext', templatize('- trans "Foo"\n- blocktrans\n  Bar\n', origin='test.html'))

        # test Haml tags and no origin
        self.assertNotIn('gettext', templatize('- trans "Foo"\n- blocktrans\n  Bar\n'))
