from __future__ import absolute_import, print_function, unicode_literals

import jinja2.ext
import os
import six

from hamlpy.compiler import Compiler, VALID_EXTENSIONS
from hamlpy.parser.generic import ParseException


class HamlPyExtension(jinja2.ext.Extension):

    def preprocess(self, source, name, filename=None):
        extension = os.path.splitext(name)[1][1:]

        if extension in VALID_EXTENSIONS:
            compiler = Compiler()
            try:
                return compiler.process(source)
            except ParseException as e:
                raise jinja2.TemplateSyntaxError(six.text_type(e), 1, name=name, filename=filename)
        else:
            return source