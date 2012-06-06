import os
from oauth import oauth

import logging
_logger = logging.getLogger(__name__)

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from django.utils import simplejson as json

import config
from session import cookie



class SlidesHandler(webapp.RequestHandler, cookie.SimpleCookieSessionMixin):
    """
    ('/slides/(*.)')
    """
    def get(self, mode=''):    
        session = self.get_session()    
        callback_url = "%s/connect/verify" % self.request.host_url
        client = oauth.DropboxClient(config.APPLICATION_KEY, config.APPLICATION_SECRET, callback_url)
        if session.get('dropbox_credentials'):
            dropbox_credentials = session.get('dropbox_credentials')
            result = client.make_request('https://api.dropbox.com/1/metadata/sandbox', token=dropbox_credentials.get('token'), secret=dropbox_credentials.get('secret'), additional_params={})
            result_object = json.loads(result.content)
            current_user = session.get('current_user')
            if current_user:
                 username = current_user['name']
            else:
                 username = None
            template_values = {
                                  'contents': result_object.get('contents'),
                                  'username': username}
            path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'slides.html')
            self.response.out.write(template.render(path, template_values))
        else:
            self.redirect('/connect/login')
            
class FileLoaderHandler(webapp.RequestHandler, cookie.SimpleCookieSessionMixin):
    """
    ('/file/(*.)')
    """
    def get(self):
        session = self.get_session()   
        path = self.request.get('path') 
        if session.get('dropbox_credentials'):
            callback_url = "%s/connect/verify" % self.request.host_url
            client = oauth.DropboxClient(config.APPLICATION_KEY, config.APPLICATION_SECRET, callback_url)
            if path:
                dropbox_credentials = session.get('dropbox_credentials')
                result = client.make_request('https://api-content.dropbox.com/1/files/sandbox' + path, token=dropbox_credentials.get('token'), secret=dropbox_credentials.get('secret'), additional_params={})
                if result.status_code == 200:
                    metadata = json.loads(result.headers['x-dropbox-metadata'])
                    self.response.headers["Content-Type"] = metadata.get('mime_type')
                    print result.content
                else:
                   self.error(result.status_code)
        else:
            self.redirect('/connect')
            
            
            
            
            