# -*- coding: utf-8 -*-
from activity import create_app
from werkzeug.contrib.fixers import ProxyFix
from gevent import monkey

monkey.patch_all()
app = create_app()
app.wsgi_app = ProxyFix(app.wsgi_app)


if __name__ == '__main__':
    app.run(threaded=True)
