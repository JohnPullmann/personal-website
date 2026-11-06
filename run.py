from werkzeug.middleware.proxy_fix import ProxyFix

from website import create_app

app = create_app()
# Behind Caddy: trust one proxy hop so url_for(_external=True) builds https links.
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
