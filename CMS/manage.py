# -*- coding: utf-8 -*-
from werkzeug.contrib.fixers import ProxyFix
from gevent import monkey

from cms import create_app


#monkey.patch_all()
app = create_app()
app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
    app.run(threaded=True)
