import os
from oauth import oauth

import logging
_logger = logging.getLogger(__name__)

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import config
from session import cookie

class ConnectHandler(webapp.RequestHandler, cookie.SimpleCookieSessionMixin):
    """
    ('/conect/(*.)')
    """
    def get(self, mode=''):    
        session = self.get_session()    
        application_key = config.APPLICATION_KEY 
        application_secret = config.APPLICATION_SECRET  
        
        if session.get('dropbox_credentials'):
            self.redirect('/slides')
        
        callback_url = "%s/connect/verify" % self.request.host_url
        client = oauth.DropboxClient(application_key, application_secret, callback_url)
        
        if mode == "login":
            return self.redirect(client.get_authorization_url())
        elif mode == "verify":
            auth_token = self.request.get("oauth_token")
            auth_verifier = self.request.get("oauth_verifier")
            user_info = client.get_user_info(auth_token, auth_verifier=auth_verifier)
            secret = user_info['secret']
            token = user_info['token']
            
            session['current_user'] = user_info
            dropbox_credentials = {'secret': secret,
                                   'token': token}
            session['dropbox_credentials'] = dropbox_credentials
            self.set_session(session)
            self.redirect('/slides')
        elif mode == 'logout':
            session['current_user'] = None
            session['dropbox_credentials'] = None
            self.set_session(session)
            self.redirect('/')
        else:   
            template_values = {}
            path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'connect.html')
            self.response.out.write(template.render(path, template_values))