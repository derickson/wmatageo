#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import requests

import json
import certifi

from elasticsearch import helpers
from elasticsearch import Elasticsearch
from elasticsearch import ElasticsearchException

from esutils import prettyPrint

from esutils import assertTemplate
from esutils import initLoad
from esutils import finishLoad
from esutils import pushDataSet

from esutils import isoFormat_from_str_tz

API_KEY = os.environ.get('API_KEY','e13626d03d8e4c03ac07f95541b3091b')  ## that's the public demo api key


certLocation = os.environ.get("ES_CA_CERT", certifi.where())
esConnString = os.environ.get('ES_CONN_STRING', 'http://localhost:9200')
esTo = Elasticsearch([esConnString],request_timeout=100,ca_certs=certLocation)
writeBatchSize = 100
indexBase = 'bus-'


## bus positions might be deprecated https://developer.wmata.com/docs/services/54763629281d83086473f231/operations/5476362a281d830c946a3d68

url = "https://api.wmata.com/Bus.svc/json/jBusPositions"
headers={"api_key":API_KEY}

busPositions = (requests.get(url=url, headers=headers).json())['BusPositions']
busses = {}

for bus in busPositions:
	if 'VehicleID' in bus :
		bus['location'] = [ bus['Lon'], bus['Lat'] ]
		bus['DateTime'] = isoFormat_from_str_tz(bus['DateTime'], "America/New_York")
		bus['TripStartTime'] = isoFormat_from_str_tz(bus['TripStartTime'], "America/New_York")
		bus['TripEndTime'] = isoFormat_from_str_tz(bus['TripEndTime'], "America/New_York")

		# bus['_id'] = bus['VehicleID']
		busses[bus['VehicleID']] = bus

		# prettyPrint(bus)

template = {
	"index_patterns": ["bus-*"],
	"settings": {
		"number_of_shards": 1
	},
	"mappings": {
		"properties": {
			"location": {"type": "geo_point"}
		}
	}
}

assertTemplate(esTo, template, "sfdc_template")

_state = {}
initLoad(esTo, _state)

pushDataSet( 'positions', busses, esTo, _state, indexBase, writeBatchSize)

finishLoad(esTo, _state)
