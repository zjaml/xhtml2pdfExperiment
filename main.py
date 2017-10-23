#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
from xhtml2pdf import pisa
import StringIO

from google.appengine.ext.webapp import template
import webapp2

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {
            'greetings': 'greetings',
            'url': 'url',
            'url_linktext': 'url_linktext',
        }

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        content = template.render(path, template_values)
        result = StringIO.StringIO()
        status = pisa.CreatePDF(content, result, link_callback=fetch_resources)
        self.response.headers['Content-Type'] = 'application/pdf'
        self.response.out.write(result.getvalue())


def fetch_resources(uri, rel):

    current_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_path, uri)

def html2pdf(data, filename, open_file=False):

    """
    Simple test showing how to create a PDF file from
    PML Source String. Also shows errors and tries to start
    the resulting PDF
    """

    pdf = pisa.CreatePDF(
        six.StringIO(data),
        file(filename, "wb"), link_callback=fetch_resources)

    if open_file and (not pdf.err):
        pisa.startViewer(filename)

    return not pdf.err

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
