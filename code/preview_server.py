# Local preview of the portfolio with the new case studies. Run:  python preview_server.py
# then open http://localhost:8765/philosophy-cans  or  http://localhost:8765/tori-richard-kahala
import http.server, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8765

class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=HERE, **k)
    def do_GET(self):
        p = self.path.split('?')[0]
        if '/assets/' in p: p = p[p.index('/assets/'):]   # relative ./assets/ from a nested route like /work/
        if p.startswith('/assets/') or p == '/index.html':
            self.path = p
            return super().do_GET()
        # every site route gets the shell; the site's own JS routes on location.pathname
        self.path = '/index.html'
        return super().do_GET()
    def log_message(self, *a): pass

print('preview on http://localhost:%d/' % PORT)
http.server.ThreadingHTTPServer(('127.0.0.1', PORT), H).serve_forever()
