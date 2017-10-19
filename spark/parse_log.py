# -*- coding: utf8 -*-
from collections import defaultdict

def split_item(line=""):

    line = line.replace("- - --", "")
    lines = line.split(" ", line)
    item = defaultdict(lambda: "")
    item['month'] = lines[0]
    item['day'] = lines[1]
    item['date'] = lines[6]
    item['ip'] = lines[5]
    item['server'] = lines[8]
    item['interface'] = lines[-2].split('?')[0]
    item['method'] = lines[-3]
    if '/v1.0/callback/ios_click' in item['interface']:
        item['download_user'] = lines[-2].split('?')[1].split('&')[0].split('=')[1].split('ios_')[0]

    return item
