#!/usr/bin/env python2
from twisted.web import server, resource
from twisted.internet import ssl, reactor
from httplib import HTTPSConnection
from urllib import urlencode
import json, pprint

ssl = False # your .crt should be signed (Facebook verifies them)
port = 8080

class RealFace(resource.Resource):
    """Faceboook callback script in Twisted Python.
    
    It listens to GET messages to authorise callback methods added from
    Facebook as well as acting as an event handler for POSTs.

    """

    isLeaf = True
    app_id = ''
    secret_id = ''
    access_token= ''

    def render_GET(self, request):
        """Authorizes a new subscription.
        See: https://developers.facebook.com/apps/$app_id/realtime.


        """
        print 'GET', request.args
        mode = request.args['hub.mode'][0]
        if request.args['hub.verify_token'][0] != 'aoeu':
            raise Exception('''Invalid verify_token.''')
        self._list_subs()
        return request.args['hub.challenge'][0]

    def render_POST(self, request):
        """Take return from Facebook callback and handle it by passing it
        on to other methods.

        Note that this method is currently utterly fucked so it's not working
        once the useless cunt Facebook devs actually fix the  real time
        issues then this will start working again and I'll be able to
        add functions to deal with the POST returns.

        The return response will be in JSON, so json.loads(request.args) or
        something of that sort, followed by a dispatch to functions dependant
        on what the post was.
        
        For now we're just going to print the request and wait for Facebook
        to get a fucking move on.
        
        See:
        https://developers.facebook.com/bugs/526383230745695
        https://developers.facebook.com/bugs/570043949694824
        http://facebook.stackoverflow.com/questions/16210345/no-post-responses-from-real-time-callbacks
        
        """
        print(request)
        return

    def _add_user(self):
        """Set up a users permissions. (potentially)."""

        params = urlencode({
            'object': 'user',
            'fields': 'personal_info,general_info,feed',
            'callback_url': 'https://blah:8080/',
            'verify_token': 'test'
        })
        conn = HTTPSConnection('graph.facebook.com')
        return conn.request('POST', '/{0}/subscriptions'.format(self.app_id), params)

    def _list_subs(self):
        conn = HTTPSConnection('graph.facebook.com')
        ret = conn.request('POST', '/{0}/subscriptions'.format(self.app_id))
        if ret:
            return ret.read()
        return ret

site = server.Site(RealFace())
if ssl:
    reactor.listenSSL(port, site, ssl.DefaultOpenSSLContextFactory('key/server.key', 'key/server.crt'))
else:
    reactor.listenTCP(port, site)

reactor.run()
