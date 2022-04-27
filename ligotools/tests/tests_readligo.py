from ligotools import readligo as rl
import json
eventname = 'GW150914' 

def test_loaddata1():
	# fnjson = "./../BBH_events_v3.json"
	fnjson = "BBH_events_v3.json"
	events = json.load(open(fnjson,"r"))

	event = events[eventname]
	fn_H1 = event['fn_H1']

	strain, time, chan_dict = rl.loaddata(fn_H1)
	assert type(time) == numpy.ndarray