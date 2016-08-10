import os
from pybratabase import Session

API_HOST = os.environ['API_HOST']
APP_ID = os.environ['APP_ID']
APP_SECRET = os.environ['APP_SECRET']
TOKEN = os.environ['APP_TOKEN']


def test_fetch_index():
    sess = Session(host=API_HOST)
    assert sess.site.self == API_HOST, sess.site.self


def test_brands():
    sess = Session(host=API_HOST)
    brands = sess.site.links.brands.collection
    assert len(brands) == 20


def test_brand_detail():
    sess = Session(host=API_HOST)
    brands = sess.site.links.brands
    first_brand_tup = brands.collection[0]
    first_brand = first_brand_tup.entity
    assert first_brand.self == first_brand_tup.href
    assert first_brand.self == brands.payload['collection'][0]['href']


def test_meta():
    sess = Session(host=API_HOST)
    brands = sess.site.links.brands
    assert brands.meta.current.self == brands.self


def text_pagination():
    sess = Session(host=API_HOST)
    page_1 = sess.site.links.brands
    page_2 = page_1.meta.next
    assert page_1.meta.payload['next'] == page_2.self
    prev = page_2.meta.prev
    assert page_1.self == prev.self


def test_rate_limit():
    sess = Session(host=API_HOST)
    rate_limit = sess.site.links.rate_limit
    current_limit = rate_limit.body['base'].copy()
    # Make one more request
    page_1 = sess.site.links.brands
    rate_limit.refresh()
    assert current_limit['limit'] + 1 == rate_limit.body['base']['limit']


def test_client_id():
    anon_sess = Session(host=API_HOST)
    rate_limit = anon_sess.site.links.rate_limit.body['base']
    anon_total = rate_limit['limit'] + rate_limit['remaining']
    auth_sess = Session(host=API_HOST, credentials={
        'app_key': APP_ID,
        'app_secret': APP_SECRET
    })
    auth_rate_limit = auth_sess.site.links.rate_limit.body['base']
    auth_total = auth_rate_limit['limit'] + auth_rate_limit['remaining']
    assert auth_total > anon_total, (auth_total, anon_total)


def test_user_authenticated():
    sess = Session(host=API_HOST, credentials={
        'code': TOKEN,
    })
    me = sess.site.links.me
    bras = me.links.bras
    assert bras.rel == 'collection'
    assert bras.self.endswith('/me/bras/')
