from werkzeug.exceptions import NotFound
from werkzeug.middleware.shared_data import SharedDataMiddleware
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from server import create_app

client = SharedDataMiddleware(NotFound(), {
  '/js/': '../client/dist/js/',
  '/css/': '../client/dist/css/',
  '/img/': '../client/dist/img/',
  '/': '../client/dist/index.html'
})

app = DispatcherMiddleware(client, {'/server': create_app()})

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('127.0.0.1', 5000, app, use_debugger = True, use_reloader = True)