#!/usr/bin/env python

import eventful
import json

api = eventful.API('75nvdNNS994cgSfT', cache='.cache')
#api.login('dadadawen123', 'Xiaohangjia123!')
events = api.call('/events/search', q='music', l='San Diego')

for event in events['events']['event']:
    print ("%s at %s" % (event['title'], event['venue_name']))

print(events)

with open('data.txt', 'w') as outfile:
    json.dump(events, outfile)