import os
from oauth import oauth

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import config
from session import cookie

class MainHandler(webapp.RequestHandler, cookie.SimpleCookieSessionMixin):
    """
    ('/')
    """
    def get(self):
        session = self.get_session()
        current_user = session.get('current_user')
        if current_user:
             username = current_user['name']
        else:
             username = None
        template_values = {'username': username}
        path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'index.html')
        self.response.out.write(template.render(path, template_values))