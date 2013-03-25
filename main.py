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
import webapp2
import StringIO
import pythontidy as pt


class MainHandler(webapp2.RequestHandler):
 
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

    formCutre="""
        <form action="/" method="post">
        Autor-cantamornings: <input type="text" name="cantamornings">
        <br />
        <textarea name="chorizo" rows="10" cols="20">{0}</textarea>
        <br />

        <input type=submit value="bonitificar" >
        <br />
        </form>
        """

    def renderCutre(self, chorizo):
        """imprime un chorizo en html por pantalla """
        cutrangadaHTML="""
        <html><head><title>Mierdoso</title></head>
        <body>
        {0}
        </body>
        </html>
        """
        self.response.out.write(cutrangadaHTML.format(chorizo))

    def post(self):
        """get receive text and prettyprint it"""
        #- take the text from the request
        txt = self.request.get('chorizo')
        #- send it to the formater
        bonitico = self.formater(txt)
        #- and show a website with the pretty code 
        formCutre=self.formCutre.format(bonitico)
        self.renderCutre(formCutre)
        
    def get(self):
        """shows just atext box for input"""
        self.renderCutre(self.formCutre.format("Aqui pegar tu codigo python fulero"))
        

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
