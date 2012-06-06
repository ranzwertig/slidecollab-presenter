#!/usr/bin/env python
#
# This is an sample AppEngine application that shows how to 1) log in a user
# using the Twitter OAuth API and 2) extract their timeline.
#
# INSTRUCTIONS: 
#
# 1. Set up a new AppEngine application using this file, let's say on port 
# 8080. Rename this file to main.py, or alternatively modify your app.yaml 
# file.)
# 2. Fill in the application ("consumer") key and secret lines below.
# 3. Visit http://localhost:8080 and click the "login" link to be redirected
# to Twitter.com.
# 4. Once verified, you'll be redirected back to your app on localhost and
# you'll see some of your Twitter user info printed in the browser.
# 5. Copy and paste the token and secret info into this file, replacing the 
# default values for user_token and user_secret. You'll need the user's token 
# & secret info to interact with the Twitter API on their behalf from now on.
# 6. Finally, visit http://localhost:8080/timeline to see your twitter 
# timeline.
#
import logging

_logger = logging.getLogger(__name__)

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

import config

from handlers import (connect_handler,
                      main_handler,
                      presenter_handler,
                      slides_handler,
                      pages_handler)

def main():
    application = webapp.WSGIApplication([
                                            ('/', main_handler.MainHandler),
                                            ('/connect/(.*)', connect_handler.ConnectHandler),
                                            ('/presenter', presenter_handler.PresenterHandler),
                                            ('/slides', slides_handler.SlidesHandler),
                                            ('/file', slides_handler.FileLoaderHandler),
                                            ('/help', pages_handler.HelpHandler),
                                            ('/about', pages_handler.AboutHandler)
                                         ], debug=True)                                
                                       
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()