# coding=utf-8
import json
import ssl
import urllib2


def gen_element(lists):
    assert len(lists) % 3 == 0
    name = lists[0]  # 节点名
    params = lists[1]  # 节点属性list
    content = lists[2]  # 节点内容 可能是String 或者是包含其他Element.
    string = "\n<" + name  # 以下为解析XML List的过程

    for k, v in params.items():  # 枚举属性
        string += ' %s="%s"' % (k, v)

    if isinstance(content, str) or isinstance(content, unicode):  # 通过递归 解析子节点
        text = content
    else:
        text = gen_element(content)
    string += ">" + text + "</%s>" % name

    if len(lists) <= 3:  # 通过递归， 解析同级节点
        return string
    else:
        return string + gen_element(lists[3:])


def gen_alfred_xml(row_list):  # 生成alfred所需要的XML String.
    item = []
    for row in row_list:
        tsi = ['title', {}, row['title'], 'subtitle', {}, row['subtitle'], 'icon', {}, row['icon']]
        item.extend(['item', {'uid': row['uid'], 'arg': row['arg']}, tsi])
    items = ['items', {}, item]
    return gen_element(items)


def load_json(url, encoding='utf-8'):
    context = ssl._create_unverified_context()
    resp = urllib2.urlopen(url, context=context).read()
    return json.loads(resp, encoding=encoding)


class Items(object):
    def __init__(self, icon=None):
        self.lst = []
        self.icon = icon

    def add(self, uid, arg, subtitle, title, valid='yes', icon=None):
        if not icon:
            icon = self.icon
        self.lst.append(dict(uid=uid, arg=arg, icon=icon, subtitle=subtitle, title=title, valid=valid))

    def to_xml(self):
        return gen_alfred_xml(self.lst)

    def len(self):
        return len(self.lst)


if __name__ == '__main__':
    rowList = [{'uid': '123321', 'arg': 'argsx', 'autocomplete': 'autocompletex', 'icon': 'icon',
                'subtitle': 'subtitle', 'title': 'title'}]
    element = gen_alfred_xml(rowList)

    print(element)
