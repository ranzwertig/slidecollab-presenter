import time
import base64
import hashlib
import datetime
import pickle

class NoValidCookieRepresentationException(Exception):
    pass
class InvalidSignatireException(Exception):
    pass

class SimpleCookieSessionMixin(object):
    
    def __init__(self, expires=3600, domain=None, path='/', coockie_name='data', salt='custom_salt'):
        self.cookie_name = coockie_name
        self.expires = expires
        self.domain = domain
        self.path = path
        self.salt = salt
        
    def set_session(self, data):
        json_data = pickle.dumps(data)
        self.response.headers.add_header('Set-Cookie', self._get_coockie_strig(json_data))
        
    def get_session(self):
        cookie = self.request.headers.get('Cookie')
        if cookie:
            cookie_data = cookie.replace(self.cookie_name+'=', '')
            parts = cookie_data.split('|')
            if len(parts) > 1:
                json_string = base64.b64decode(parts[0])
                signed = parts[1]
                if str(hashlib.md5(str(json_string)+str(self.salt)).hexdigest()) == signed:
                    return pickle.loads(json_string)
                else:
                    raise InvalidSignatireException('Signature of cookie not valid!')
            else:
                raise NoValidCookieRepresentationException('Cookie not signed!')
        else:
            return {}
            
    def _get_coockie_strig(self, json_data):
        cookie = {}
        cookie['domain'] = self.domain
        cookie['path'] = self.path
        
        encoded_data = base64.b64encode(json_data)
        signed_data = str(hashlib.md5(str(json_data)+str(self.salt)).hexdigest())
        
        cookie_string = self.cookie_name + '=' + encoded_data + '|' + signed_data
        if self.expires:
            expires_date = datetime.datetime.utcnow() + datetime.timedelta(0, self.expires)
            expires_str = expires_date.strftime('%a, %d-%b-%Y %H:%M:%S GMT')
            cookie_string += '; ' + str('expires') + '=' + str(expires_str)
        
        for key in cookie:
            if cookie[key] != None: 
                cookie_string += '; ' + str(key) + '=' + str(cookie[key])
                
        return cookie_string
        