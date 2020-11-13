import numpy as np
import time
import sys
from array import array
import pickle
import ROOT

#from ROOT import gROOT, AddressOf, TChain

import sys
import os



"""
#############################################################################################################

def fermi_dirac(x, par):

	return par[2] / ( ROOT.TMath.Exp( (x[0] - par[0]) / (par[1]) ) + 1 );

#############################################################################################################





#############################################################################################################

def fermi_dirac2(x, par):
 	
	return par[2] / ( ROOT.TMath.Exp( -(x[0] - par[0]) / (par[1]) ) + 1 );

#############################################################################################################
"""




#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################




OS = sys.platform
if OS == 'win32':
    sep = '\\'
elif OS == 'linux2' or OS == "linux":
    sep = '/'
else:
    print("ERROR: OS {} non compatible".format(OS))
    sys.exit()




"""
#################################################################################
#################################################################################

map_path = "/home/ihep_data/TIGER_Event_Reconstruction/mapping_and_calibration_file/"
map_file = map_path + "mapping_CGEMBOSS_2.0.root"
f = ROOT.TFile(map_file)
tr = f.Get("tree")

map_dict = dict()

#tr.Print()

ROOT.gROOT.ProcessLine('struct TreeStruct {\
	int layer_id;\
	int channel_id;\
	int FEB_label;\
	int chip_id;\
	int HW_FEB_id;\
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
HW_FEB_id = array( 'i', [0] )
tr.SetBranchAddress( "HW_FEB_id", HW_FEB_id )


for i in range( tr.GetEntries() ):
	tr.GetEntry( i )
	#print(FEB_label[0])
	#print("FEB_label = {}\tL = {}\tHW_FEB = {}\t ".format(FEB_label[0], layer_id[0], HW_FEB_id[0]))
	map_dict[FEB_label[0]] = [layer_id[0], HW_FEB_id[0]]


#################################################################################
#################################################################################

"""










#################################################################################


is_tdc_calib = True
is_coarse_counters = False


img = ROOT.TImage.Create()
chain = ROOT.TChain("tree")



try:
        RUN = int(sys.argv[1])
except:
        RUN = 355

print("Importing Tfine values for TDC calibration from RUN {}".format(RUN))

data_path = "/home/ihep_data/data/raw_root/{}".format(RUN)

chain.Add("{}/Sub_RUN_ana*".format(data_path));

ROOT.gROOT.ProcessLine('struct TreeStruct {\
	int efine_uncal;\
	int tfine_uncal;\
	int tcoarse;\
	int ecoarse;\
	int layer;\
	int channel;\
	int FEB_label;\
	int chip;\
	int tac;\
	int strip_x;\
	int strip_v;\
	float charge_SH_uncal;\
	float charge_SH;\
	};')

#mystruct = var_t()

mystruct = ROOT.TreeStruct()


"""
for key in ROOT.TreeStruct.__dict__.keys():
	print key
	if '__' not in key:
		chain.SetBranchAddress(key, ROOT.AddressOf(mystruct, key))

		#formstring = '/F'
		#if isinstance(mystruct.__getattribute__(key), int):
		#formstring = '/I'
		#chain.Branch(key, ROOT.AddressOf(mystruct, key), key + formstring)
"""



layer = array( 'i', [0] )
chain.SetBranchAddress( "layer", layer )
FEB_label = array( 'i', [0] )
chain.SetBranchAddress( "FEB_label", FEB_label )
chip = array( 'i', [0] )
chain.SetBranchAddress( "chip", chip )
channel = array( 'i', [0] )
chain.SetBranchAddress( "channel", channel )
tac = array( 'i', [0] )
chain.SetBranchAddress( "tac", tac )
tfine_uncal = array( 'f', [0] )
chain.SetBranchAddress( "tfine_uncal", tfine_uncal )
tcoarse = array( 'f', [0] )
chain.SetBranchAddress( "tcoarse", tcoarse )
ecoarse = array( 'f', [0] )
chain.SetBranchAddress( "ecoarse", ecoarse )
charge_SH = array( 'f', [0] )
chain.SetBranchAddress( "charge_SH", charge_SH )


#chain.Print()


##################################################################

# TDC calibration

##################################################################


if is_tdc_calib:

	Tfine_dict = dict()
	for feb_number in range(0, 60):
		#print feb_number
		chip_dict = dict()
		for chip_number in range(1, 3):
			#print chip_number
			channel_dict = dict()
			for channel_number in range(0, 64):
				#print channel_number
				tac_dict = dict()
				for tac_number in range(0, 4):
					#print tac_number
					tac_dict[tac_number] = list()
				channel_dict[channel_number] = tac_dict
			chip_dict[chip_number] = channel_dict
		Tfine_dict[feb_number] = chip_dict


	for i in range( chain.GetEntries() ):
		chain.GetEntry( i )
		
		if i%100000 == 0:
			print ("READ {} hits".format(i) )
		#if channel[0] != 62:
		#print layer[0], FEB_label[0], chip[0], channel[0], tac[0], tfine_uncal[0], charge_SH[0], tcoarse[0], ecoarse[0]

		Tfine_dict[FEB_label[0]][chip[0]][channel[0]][tac[0]].append(int(tfine_uncal[0]))
        

	with open("TDC_folder/Tfine_{}.pickle".format(RUN), 'wb') as handle:
                pickle.dump(Tfine_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)




##################################################################

# Check flat distribution for Tcoarse and Ecoarse

##################################################################


if is_coarse_counters:

	hTcoarse = ROOT.TH1D("h_Tcoarse", "Tcoarse", 65536, 0, 65536)
	cTcoarse = ROOT.TCanvas("c_Tcoarse", "Tcoarse", 250, 250, 1000, 600)
	chain.Draw("tcoarse>>h_Tcoarse", "", "")

	hEcoarse = ROOT.TH1D("h_Ecoarse", "Ecoarse", 1024, 0, 1024)
	cEcoarse = ROOT.TCanvas("c_Ecoarse", "Ecoarse", 300, 300, 1000, 600)
	chain.Draw("ecoarse>>h_Ecoarse", "", "")





















#rootFile = ROOT.TFile(rname, 'recreate')
#tree = ROOT.TTree('tree', '')
#mystruct = ROOT.TreeStruct()
