class Document:
    def __init__(self, payload, session, response):
        self.payload = payload
        self.session = session
        self.response = response

    def __getattr__(self, item):
        if item == 'links':
            return Links(self.payload['links'], self.session, self.response)
        elif item == 'meta':
            return Meta(self.payload['meta'], self.session, self.response)
        elif item in self.payload:
            return self.payload[item]
        return super().__getattribute__(item)

    def refresh(self):
        doc = self.session.get(self.response.request.url)
        self.response = doc.response
        self.payload = doc.payload


class Links(Document):
    def __getattr__(self, item):
        if item in self.payload:
            next_url = self.payload[item]
            return self.session.get(next_url)
        return super().__getattribute__(item)


class Meta(Document):
    URLS = {'next', 'current', 'prev'}

    def __getattr__(self, item):
        if item in self.URLS:
            next_url = self.payload[item]
            return self.session.get(next_url)
        else:
            return self.payload[item]


class CollectionTuple(Document):
    @property
    def entity(self):
        return self.session.get(self.payload['href'])


class Collection(Document):
    def __getattr__(self, item):
        if item == 'collection':
            return [CollectionTuple(tup, self.session, self.response)
                    for tup in self.payload['collection']]
        return super().__getattr__(item)


class Entity(Document):
    pass


RELS = {
    'collection': Collection,
    'entity': Entity
}
