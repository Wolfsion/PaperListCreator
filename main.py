import os
import xml.sax

from MHandler import MHandler
from Repo import Repo


def init_papers():
    filename = 'dblp.xml'
    if os.path.exists(filename) is False:
        print('[%s] not exists!' % filename)
        exit(1)

    # 创建一个 XMLReader
    parser = xml.sax.make_parser()
    # turn off namespaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    inner = Repo()
    handler = MHandler(inner)
    parser.setContentHandler(handler)
    parser.parse(filename)
    print('Parser Complete!')
    inner.format()
    inner.over()


if __name__ == '__main__':
    init_papers()
