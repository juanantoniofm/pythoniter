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
import webapp2
import jinja2
import logging

import StringIO
import pythontidy as pt
template_path=os.path.dirname(__file__) + "/templates"
jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_path))
logging.debug("The path for templates is")
logging.debug(template_path)

class MainHandler(webapp2.RequestHandler):

    def renderAndWrite(self, values, template="formater.html"):
        """render values in the template"""
        template = jinja_environment.get_template(template)
        self.response.out.write(template.render(values))

    def formater(self, pythonshit):
        #- receive text in string format
        #- convert it to file-like object
        inf = StringIO.StringIO()
        ouf = StringIO.StringIO()
        inf.write(pythonshit)
        inf.seek(0)
        #- pass it through the tidyer
        pt.tidy_up(inf, ouf)
        pythonshit = ouf.getvalue()
        #- return the output as string
        return pythonshit

    def post(self):
        """get receive text and prettyprint it"""
        #- take the text from the request
        txt = self.request.get('chorizo')
        #- send it to the formater
        bonitico = self.formater(txt)
        #- and show a website with the pretty code 
        self.renderAndWrite({"codechunk": bonitico})
        
    def get(self):
        """shows just atext box for input"""
        self.renderAndWrite({"codechunk" : "Aqui pegar tu python fulero"})
        

class DownHandler(MainHandler):
    def post(self):
        self.renderAndWrite({"codechunk" :
                             self.formater(
                                 self.request.get('chorizo'))})
                             
    def get(self):
        self.response.out.write("""Visit this using POST to upload your code, and
                                download it as a file""")
        

class ZenHandler(MainHandler):
    def post(self):
        self.renderAndWrite({"codechunk" :
                             self.formater(
                                 self.request.get('chorizo'))},
                           "zen.html")
                             
    def get(self):
        self.renderAndWrite({"codechunk" : "Here goes your Python"},
                            "zen.html")



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/zen', ZenHandler),
    ('/down', DownHandler)
], debug=True)
