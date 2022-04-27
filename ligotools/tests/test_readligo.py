import numpy as np
from scipy import signal
from scipy.interpolate import interp1d
from scipy.signal import butter, filtfilt, iirdesign, zpk2tf, freqz
import h5py
import json
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from ligotools import readligo as rl
from ligotools.utils import *

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
    
    
# tests for utils
fs = event['fs'] 
NFFT = 4*fs
fband = event['fband'] 
bb, ab = butter(4, [fband[0]*2./fs, fband[1]*2./fs], btype='band')
normalization = np.sqrt((fband[1]-fband[0])/(fs/2))
Pxx_H1, freqsH = mlab.psd(strain_H1, Fs = fs, NFFT = NFFT)
Pxx_L1, freqsL = mlab.psd(strain_L1, Fs = fs, NFFT = NFFT)
psd_H1 = interp1d(freqsH, Pxx_H1)
psd_L1 = interp1d(freqsL, Pxx_L1)
dt_H1 = time_H1[1] - time_H1[0]
dt_L1 = time_L1[1] - time_L1[0]

def test_whiten1():
	whiten_h1 = whiten(strain_H1, psd_H1, dt_H1)
	assert type(whiten_h1) == type(np.array([1,2]))
    assert len(whiten_h1) == 131072
    
def test_whiten2():
	whiten_l1 = whiten(strain_L1, psd_L1, dt_L1)
	assert type(whiten_l1) == type(np.array([1,2]))

def test_write_wavfile():
	whiten_h1 = whiten(strain_H1, psd_H1, dt_H1)
	write_wavfile("audio/" + eventname +"_H1_shifted.wav", 4096, whiten_h1)
	assert path.isfile('audio/GW150914_H1_shifted.wav') == True

def test_plot_code():
	whiten_l1 = whiten(strain_L1, psd_L1, dt_L1)
	plot_PSD(0, 1126259462.4324, 13.2, 'g', 'L1', 1126259462.44, 0, 0, 'GW150914', 'png', 0, 0, 999.74, 0, 0, 4096)
	assert exists("figures/GW150914_L1_matchfreq.png")
 