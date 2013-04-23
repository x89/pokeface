#!/usr/bin/env python2
from twisted.web import server, resource
from twisted.internet import reactor
from httplib import HTTPSConnection
from urllib import urlencode

class Simple(resource.Resource):
    isLeaf = True
    app_id = 542723585779395

    def render_GET(self, request):
        print 'GET', request.args
        mode = request.args['hub.mode'][0]
        if request.args['hub.verify_token'][0] != 'general_test':
            raise Exception()
        print self._add_user()
        self._list_subs()
        return request.args['hub.challenge'][0]

    def render_POST(self, request):
        print 'POST', request.args

    def _add_user(self):
        params = urlencode({
            'object': 'user',
            'fields': 'personal_info,general_info,feed',
            'callback_url': 'http://face.trailbeans.eu/poke.py',
            'verify_token': 'sub_user_info'
        })
        conn = HTTPSConnection('graph.facebook.com')
        return conn.request('POST', '/{0}/subscriptions'.format(self.app_id), params)

    def _list_subs(self):
        conn = HTTPSConnection('graph.facebook.com')
        ret = conn.request('POST', '/{0}/subscriptions'.format(self.app_id))
        if ret:
            print ret.read()
        return ret

site = server.Site(Simple())
reactor.listenTCP(8080, site)
reactor.run()
