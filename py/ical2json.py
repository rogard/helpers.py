#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Original code (Bosch) as recorded at:
# https://github.com/rogard/helpers.py, commit 9d1a659

#  Copyright (c) 2011, Philipp Bosch
#
#  Permission is hereby granted, free of charge, to any person obtaining a
#  copy of this software and associated documentation files (the Software),
#  to deal in the Software without restriction, including
#  without limitation the rights to use, copy, modify, merge, publish,
#  distribute, sublicense, and/or sell copies of the Software, and to
#  permit persons to whom the Software is furnished to do so, subject to
#  the following conditions:
#
#  The above copyright notice and this permission notice shall be included
#  in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED AS IS, WITHOUT WARRANTY OF ANY KIND, EXPRESS
#  OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
#  CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
#  TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#  SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os

from flask import Flask, abort, jsonify, request
from icalendar import Calendar
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return u'Please use like <code>http://<script>document.write(location.host);</script><noscript>ical2json.pb.io</noscript>/http://www.myserver.com/path/to/file.ics</code><br>Source code and instructions at <a href="http://github.com/philippbosch/ical2json">http://github.com/philippbosch/ical2json</a>.'

@app.route('/<path:url>')
def convert_from_url(url):
    if url == 'favicon.ico':
        abort(404)
    if not url.startswith('http'):
        url = 'http://%s' % url

    try:
        r = requests.get(url)
        r.raise_for_status()
        
        # previous attempt:
        # try:
        #     r = requests.get(url)
        # except:
        #     abort(500)
        # if not r.ok:
        #     abort(r.status_code)
        
        ics = r.content
        cal = Calendar.from_ical(ics)
    except requests.HTTPError as e:
        # Source URL returned an error
        abort(e.response.status_code if 400 <= e.response.status_code < 600 else 500)
    except requests.RequestException:
        abort(502)  # Bad Gateway - couldn't reach source
    except Exception:
        abort(500)  # Internal error parsing ICS

    # build data
    data = {}
    data[cal.name] = dict(cal.items())

    for component in cal.subcomponents:
        if not component.name in data[cal.name]:
            data[cal.name][component.name] = []

        comp_obj = {}
        for item in component.items():
            if hasattr(item[1], 'dt'):
                val = item[1].dt.isoformat()
            else:
                val = item[1].to_ical().decode('utf-8').replace('\\,', ',')
                comp_obj[item[0]] = val

        data[cal.name][component.name].append(comp_obj)

    resp = jsonify(data)
    if 'callback' in request.args:
        resp.data = "%s(%s);" % (request.args['callback'], resp.data)
    return resp

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
