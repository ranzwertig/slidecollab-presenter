import os
from oauth import oauth

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import config
from session import cookie
        
class AboutHandler(webapp.RequestHandler, cookie.SimpleCookieSessionMixin):
    """
    ('/about')
    """
    def get(self):
        session = self.get_session() 
        current_user = session.get('current_user')
        if current_user:
             username = current_user['name']
        else:
             username = None
        template_values = {'username': username}
        path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'about.html')
        self.response.out.write(template.render(path, template_values))
        
class HelpHandler(webapp.RequestHandler, cookie.SimpleCookieSessionMixin):
    """
    ('/help')
    """
    def get(self):
        session = self.get_session() 
        current_user = session.get('current_user')
        if current_user:
             username = current_user['name']
        else:
             username = None
        template_values = {'username': username}
        path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'help.html')
        self.response.out.write(template.render(path, template_values))