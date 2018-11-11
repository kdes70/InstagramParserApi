import json
import re
import lxml.html

def get_csrf_token(content):
    xpath_data = lxml.html.fromstring(content).xpath('/html/body/script[1]/text()')[0]
    raw_json = re.findall(r'({.*});', xpath_data)[0]
    return json.loads(raw_json)["config"]["csrf_token"]
