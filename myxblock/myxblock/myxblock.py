# TO-DO: Write a description of what this XBlock is.

import pkg_resources,os
from web_fragments.fragment import Fragment
from xblock.core import XBlock
from django.core.files.base import ContentFile
from xblock.fields import Integer, Scope, String
from django.template import Context, Template
from xblockutils.resources import ResourceLoader
import urllib.parse
import logging
import json
import os
from django.conf import settings
from django.core.files.storage import default_storage
from webob import Response
log = logging.getLogger(__name__)




class MyXBlock(XBlock):
    """
    TO-DO: document what your XBlock does.
    """    
    
    jupyterlite_url = String(
        display_name="JupyterLite Service URL",
        help="The URL of the JupyterLite service",
        scope=Scope.settings,
        default="http://localhost:9500/lab/"
    )
    editable_fields = ('jupyterlite_url','default_notebook')
    default_notebook = String(
        display_name="Default Notebook",
        scope=Scope.settings,
        help="The default notebook for the JupyterLite service",
        default="test.ipynb"
    )
    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")
    
    def get_external_url(self, file_name):
        base_url = self.jupyterlite_url
        encoded_file_name = urllib.parse.quote(file_name)
        external_url = f"{base_url}?fromURL={encoded_file_name}"
        return external_url

    def render_template(self, template_path, context):
        template_str = self.resource_string(template_path)
        template = Template(template_str)
        rendered_template = template.render(Context({'context': context}))
        return rendered_template
    
    
    def get_tmp_file_url(self):
        tmp_file_path = 'static/defaut_notebook.ipynb'
        path =  '{}{}'.format(settings.MEDIA_URL, tmp_file_path)
        print("path =  ",path)
        return path
    
    # def json_to_nb_format(nb_str):
    #     """Converts Notebook JSON to python object"""
    #     nb = nbformat.reads(nb_str, as_version=4)
    #     return nb
    
    def student_view(self, context=None):
        file_name = self.default_notebook
        base_url = self.jupyterlite_url
        jupyterlite_iframe = '<iframe src="{}?fromURL={}" width="100%" height="600px" style="border: none;"></iframe>'.format(base_url, file_name)
        print("new urll             ==============",jupyterlite_iframe )
        # Create the HTML fragment
        html = self.resource_string("static/html/myxblock.html").format(jupyterlite_iframe=jupyterlite_iframe, self=self)
        frag = Fragment(html)
        frag.initialize_js('MyXBlock')
        return frag
    
    

    @staticmethod
    def json_response(data):
        return Response(
            json.dumps(data), content_type="application/json", charset="utf8"
        )
    
    def studio_view(self, context=None):
        studio_context = {
            "jupyterlite_url": self.fields["jupyterlite_url"],
        } 
        studio_context.update(context or {})
        template = self.render_template("static/html/upload.html", studio_context)
        frag = Fragment(template)
        frag.add_javascript(self.resource_string("static/js/src/jupyter_file.js"))
        frag.add_javascript(self.resource_string("static/js/src/myxblock.js"))
        frag.initialize_js('MyXBlock')
        return frag
    




    @XBlock.handler
    def studio_submit(self, request, _suffix):
        """
        Handle form submission in Studio.
        """
        # Get values from the form data
        url = request.params.get("jupyterlite_url",None)
        notebook = request.params.get("default_notebook").file
        print("notebook == ",type(notebook))
        name = request.params.get("default_notebook").file._name
        print("name == ",name)
        namee = f'static/{name}'
        path = default_storage.save(f'static/{name}', ContentFile(notebook.read()))
        print("path " ,path )
        tmp_file = os.path.join(settings.MEDIA_ROOT, path)
        self.default_notebook = tmp_file
        print("tmp_file           " ,tmp_file)
        self.jupyterlite_url = url
        # self.default_notebook = notebook
        response = {"result": "success", "errors": []}
        return self.json_response(response)



    @staticmethod
    def workbench_scenarios():
        return [
            ("MyXBlock",
             """<myxblock/>
             """),
            ("Multiple MyXBlock",
             """<vertical_demo>
                <myxblock/>
                <myxblock/>
                <myxblock/>
                </vertical_demo>
             """),
        ]
