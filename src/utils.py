import json
import hashlib
import re
import lxml.html

def return_raw_content_data(content):
    xpath_data = lxml.html.fromstring(content).xpath('/html/body/script[1]/text()')[0]
    raw_json = re.findall(r'({.*});', xpath_data)[0]
    return {'csrf_token' : json.loads(raw_json)["config"]["csrf_token"],
            'rhx_gis'    : json.loads(raw_json)["rhx_gis"]}


def calculate_md5_data(rhx_gis, variables):
    print variables
    print rhx_gis
    hash_data = hashlib.md5()
    hash_data.update('{}:{}'.format(
        rhx_gis,
        variables).encode('utf-8'))

    return hash_data.hexdigest()


