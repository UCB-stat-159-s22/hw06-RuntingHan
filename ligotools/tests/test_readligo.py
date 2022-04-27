import numpy as np
from scipy import signal
from scipy.interpolate import interp1d
from scipy.signal import butter, filtfilt, iirdesign, zpk2tf, freqz
import h5py
import json
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from ligotools import readligo as rl

eventname = 'GW150914' 
fnjson = "data/BBH_events_v3.json"
events = json.load(open(fnjson,"r"))
event = events[eventname]
fn_H1 = event['fn_H1']
fn_L1 = event['fn_L1']
strain_H1, time_H1, chan_dict_H1 = rl.loaddata("data/" + fn_H1, 'H1')
strain_L1, time_L1, chan_dict_L1 = rl.loaddata("data/" + fn_L1, 'L1')

def test_loaddata1():
    assert isinstance(strain_H1, np.ndarray)
    assert isinstance(time_H1, np.ndarray)
    assert isinstance(chan_dict_H1, dict)

def test_loaddata2():
    assert isinstance(strain_L1, np.ndarray)
    assert isinstance(time_L1, np.ndarray)
    assert isinstance(chan_dict_L1, dict)    

def test_dq_channel_to_seglist1():
    segment_list = rl.dq_channel_to_seglist(chan_dict['CBC_CAT3'])
    assert type(segment_list) == list
    
def test_read_hdf5():
    assert len(rl.read_hdf5("data/H-H1_LOSC_4_V2-1126259446-32.hdf5", True)) == 7