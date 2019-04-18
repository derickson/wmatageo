#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from datetime import datetime
from dateutil.relativedelta import relativedelta

import pytz

from elasticsearch import helpers

# import elasticapm

## useful esutils

def cleanName( name ):
	return name.replace(" ","")

def hasField(field, row):
	return field in row and row[field] != ""

def prettyPrint(doc):
	print(json.dumps(doc, indent=4, sort_keys=True))

def boolFromZeroOneStr( val ):
	if val == '0':
		return False
	elif val == '1':
		return True
	else: 
		return False

def debuggingPrint( item, debugging ):
	if(debugging):
		print(item)


def FileCheck(fn):
    try:
      open(fn, "r")
      return 1
    except IOError:
      print("FileCheck: File does not appear to exist.")
      return 0

def CacheTheListOfDicts(fn, listOfDicts):
	keys = listOfDicts[0].keys()
	print(keys)
	with open(fn, 'w') as fout:
		json.dump(listOfDicts, fout)

def RetrieveCachedListOfDicts(fn):
	with open(fn, 'r') as infile:
		return json.load(infile)

###############################################
### TIME STUFF                             ####
###############################################

def add_months(sourcedatetime,months):
	# print(sourcedatetime)
	r = sourcedatetime + relativedelta(months=months)
	# print(r)
	return r


def isoFormat_from_str_tz(datestr, tzstr):
	local = pytz.timezone (tzstr) ## "America/New_York"
	naive = datetime.strptime (datestr, "%Y-%m-%dT%H:%M:%S")
	local_dt = local.localize(naive, is_dst=None)
	utc_dt = local_dt.astimezone(pytz.utc)
	return utc_dt.isoformat()

###############################################
### TEMPLATE MANAGEMENT                    ####
###############################################


def assertTemplate(esTo, template, templateName):
	print("Applying Mapping Template")
	esTo.indices.put_template(name=templateName, body=template, create=False)




###############################################
### BATCH LOAD CONTROL WITH ALIAS FLIPPING ####
###############################################

BATCH_CONTROL = "sfdc-batch-control"

def updateCurrentState(esTo, state):
	theId = "state-" + state['startTime']
	esTo.index(index=BATCH_CONTROL,doc_type="doc",id=theId,body=state,refresh="wait_for")
	return True

# @elasticapm.capture_span()
def initLoad(esTo, state):
	state["startTime"] = datetime.now().isoformat()
	state["state"] = "starting"
	state['suffix'] = state["startTime"].replace(".","-").replace(":","-").lower()
	state['indexLoads'] = []
	updateCurrentState(esTo, state)

# @elasticapm.capture_span()	
def finishLoad(esTo, state):
	state['state'] = "finished"
	state['finishTime'] = datetime.now().isoformat()

	total = 0
	for load in state['indexLoads']:
		total = total + load['count']
	state['totalCount'] = total

	updateCurrentState(esTo, state)




# @elasticapm.capture_span()
def pushDataSet( typeName, dictInQuestion, esTo, state, indexBase, writeBatchSize, doDelete=True, actCounter=0):
	# push the data
	toType = typeName
	toIndex = indexBase+toType+"-"+state['suffix']


	bulkActions = []
	
	for _id in dictInQuestion:
		actCounter = actCounter + 1

		action = {
			"_index": toIndex,
			# "_type": "doc",
			"_id": _id,
			"_source": dictInQuestion[_id]
		}
		bulkActions.append( action )
		
		if(len(bulkActions) >= writeBatchSize ):
			helpers.bulk( esTo,  bulkActions )
			bulkActions = []

		## print some status
		if(actCounter % writeBatchSize == 0):
				print("Writing to " + toIndex + ": " + str(actCounter))

	if(len(bulkActions) > 0):
	    helpers.bulk( esTo,  bulkActions )
	    bulkActions = []
	

	# flush the new index
	esTo.indices.forcemerge(index=toIndex)
	esTo.indices.flush(index=toIndex)
	
	# set up or modify the aliases
	if( esTo.indices.exists_alias(name=toType) ):
		## update alias
		existingAlias = esTo.indices.get_alias(name=toType)
		nameToRemove = list(existingAlias.keys())[0]
		# prettyPrint(existingAlias)


		updateActions = {
		  "actions": [
		  	{ "remove": {"index": nameToRemove, "alias": toType}},
		    { "add": {"index": toIndex,"alias": toType}}
		  ]
		}

		# prettyPrint(updateActions)
		esTo.indices.update_aliases(body=updateActions)

		# clean up old copy of the data
		if(doDelete):
			deleteIndexTarget = nameToRemove
			esTo.indices.delete(index=deleteIndexTarget, ignore=[400, 404])

	else:
		## create alias for the first time
		esTo.indices.put_alias(index=toIndex, name=toType)

	state['indexLoads'].append({"index":toIndex,"name":toType,"count":actCounter})
	updateCurrentState(esTo, state)

	print("Batch load finished: " + toIndex)

	return actCounter



