import os
from oauth import oauth

import logging
_logger = logging.getLogger(__name__)

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import config
from session import cookie

class PresenterHandler(webapp.RequestHandler, cookie.SimpleCookieSessionMixin):
    """
    ('/presenter')
    """
    def get(self):
        session = self.get_session()   
        path = self.request.get('path') 
        if session.get('dropbox_credentials'):
            current_user = session.get('current_user')
            if current_user:
                 username = current_user['name']
            else:
                 username = None
            template_values = {
                                  'pdf': '/file?path='+path,
                                  'username': username
                               }
            path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'presenter.html')
            self.response.out.write(template.render(path, template_values))
        else:
            self.redirect('/connect')