# coding=utf-8
from urllib import urlencode

from alfred_utils import load_json, Items
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


api_key = '01068bdd0c3168a70313a397249439f5'


def search(query):
    url = 'https://api.douban.com/v2/movie/search?count=15&apikey=%s&%s' % (api_key, urlencode(dict(q=query)))
    data = load_json(url)
    items = Items('icon.png')
    for sub in data['subjects']:
        types = u','.join(sub['genres'])
        subtitle = u'类型: ' + types
        casts = u','.join([i['name'] for i in sub['casts']])
        if casts:
            subtitle += u'    主演: ' + casts
        title = u'(%.1f分)  %s' % (sub['rating']['average'], sub['title'])
        items.add(sub['id'], sub['alt'], subtitle, title)

    return items.to_xml()


def query_in_theaters(query):
    if query:
        return search(query)
    url = 'https://api.douban.com/v2/movie/in_theaters?apikey=%s&count=15' % api_key
    data = load_json(url)
    items = Items('icon.png')
    for sub in data['subjects']:
        types = u','.join(sub['genres'])
        casts = u','.join([i['name'] for i in sub['casts']])
        subtitle = u'类型: ' + types + u'    主演: ' + casts
        title = u'(%.1f分)  %s' % (sub['rating']['average'], sub['title'])
        items.add(sub['id'], sub['alt'], subtitle, title)

    return items.to_xml()


def query_coming_soon(query):
    if query:
        return search(query)
    url = 'https://api.douban.com/v2/movie/coming_soon?apikey=%s&count=15' % api_key
    data = load_json(url)
    data = data['subjects']
    data.sort(key=lambda x: -x['collect_count'])
    items = Items('icon.png')
    for sub in data:
        types = u','.join(sub['genres'])
        casts = u','.join([i['name'] for i in sub['casts']])
        subtitle = u'类型: ' + types + u'    主演: ' + casts + u'    收藏: ' + str(sub['collect_count'])
        title = u'(%.1f分)  %s' % (sub['rating']['average'], sub['title'])
        items.add(sub['id'], sub['alt'], subtitle, title)

    return items.to_xml()


if __name__ == '__main__':
    print(query_coming_soon(None))
