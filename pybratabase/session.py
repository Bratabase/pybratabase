import requests

from pybratabase.schemas import Document, RELS


class Session:
    def __init__(self, host, credentials=None):
        self.credentials = credentials or {}
        headers = {}
        if self.credentials:
            if 'code' in self.credentials:
                # User authorized request
                headers['Authorization'] = 'bearer %s' % self.credentials['code']
            elif 'app_key' in self.credentials:
                headers['Authorization'] = 'APP %s:%s' % (
                    self.credentials['app_key'], self.credentials['app_secret'])
        self.headers = headers or None
        self.host = host
        self.root = self.get(host)

    def get(self, url):
        resp = requests.get(url, headers=self.headers)
        payload = resp.json()
        rel = payload.get('rel')
        cls = RELS.get(rel, Document)
        return cls(payload, session=self, response=resp)
