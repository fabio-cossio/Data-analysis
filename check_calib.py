import numpy as np
import time
import sys
from array import array
import pickle
import ROOT


import sys
import os



OS = sys.platform
if OS == 'win32':
    sep = '\\'
elif OS == 'linux2' or OS == "linux":
    sep = '/'
else:
    print("ERROR: OS {} non compatible".format(OS))
    sys.exit()

ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gErrorIgnoreLevel = ROOT.kWarning

path = "/home/ihep_data/TIGER_Event_Reconstruction/mapping_and_calibration_file/"
filename = "QDCcalib_CGEMBOSS_2.0.root"

f = ROOT.TFile(path + filename)
tr = f.Get("tree")

#tr.Print()

"""
ROOT.gROOT.ProcessLine('struct TreeStruct {\
	int layer_id;\
	int channel_id;\
	int gemroc_id;\
	int FEB_label;\
	int chip_id;\
	int HW_FEB_id;\
	int SW_FEB_id;\
	float constant;\
	float slope;\
	float qmax;\
	};')

my_struct = ROOT.TreeStruct()

layer_id = array( 'i', [0] )
tr.SetBranchAddress( "layer_id", layer_id )
FEB_label = array( 'i', [0] )
tr.SetBranchAddress( "FEB_label", FEB_label )
chip_id = array( 'i', [0] )
tr.SetBranchAddress( "chip_id", chip_id )
channel_id 	 = array( 'i', [0] )
tr.SetBranchAddress( "channel_id", channel_id )
gemroc_id 	 = array( 'i', [0] )
tr.SetBranchAddress( "gemroc_id", gemroc_id )
HW_FEB_id = array( 'i', [0] )
tr.SetBranchAddress( "HW_FEB_id", HW_FEB_id )
SW_FEB_id = array( 'i', [0] )
tr.SetBranchAddress( "SW_FEB_id", SW_FEB_id )
constant = array( 'f', [0] )
tr.SetBranchAddress( "constant", constant )
slope = array( 'f', [0] )
tr.SetBranchAddress( "slope", slope )
qmax = array( 'f', [0] )
tr.SetBranchAddress( "qmax", qmax )


for i in range( tr.GetEntries() ):
    tr.GetEntry( i )
    FEB = FEB_label[0]
    SW_FEB = SW_FEB_id[0]
    HW_FEB = HW_FEB_id[0]
    chip = chip_id[0]
    channel = channel_id[0]
    a = slope[0]
    b = constant[0]
    qsat_old = qmax[0]
    try:
        qsat = -(b/a + 15/a)
    except:
        print(a,b)
        qsat = 0
    #print(FEB, SW_FEB, HW_FEB, chip, channel, a, b, qsat_old, qsat)
"""

hist_dict = dict()

k = 0

save_dir = "/home/Fabio/analysis/Data-analysis/QDC_check"

for feb in range(0, 44):
    for ch in [1, 2]:

        ee = "-(constant+15)/slope>>h1[{}]".format(k)
        sel = "FEB_label=={} && chip_id=={}".format(feb, ch)
        c1 = ROOT.TCanvas("c1", "c1", 100, 100, 1600, 1000)
        hist_dict[k] = ROOT.TH1D("h1_{}".format(k), sel, 100, 30, 70)
        tr.Draw(ee, sel, "")
        
        c1.Update()
        c1.SaveAs("{}/FEB{}_chip{}.png".format(save_dir, feb, ch))
        #c1.SaveAs("{}/good.png".format(png_dir))
        #c1.SaveAs("{}/good.root".format(root_dir))
        c1.Close()

        k = k+1



