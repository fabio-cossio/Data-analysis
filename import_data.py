import numpy as np
import time
import sys
from array import array
import pickle
import ROOT

#from ROOT import gROOT, AddressOf, TChain

import sys
import os




#############################################################################################################

def fermi_dirac(x, par):

	return par[2] / ( ROOT.TMath.Exp( (x[0] - par[0]) / (par[1]) ) + 1 );

#############################################################################################################





#############################################################################################################

def fermi_dirac2(x, par):
 	
	return par[2] / ( ROOT.TMath.Exp( -(x[0] - par[0]) / (par[1]) ) + 1 );

#############################################################################################################





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




#################################################################################
#################################################################################

f = ROOT.TFile("mapping_IHEP_L2_2planari_penta.root")
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











#################################################################################


is_tdc_calib = True
is_coarse_counters = False








img = ROOT.TImage.Create()

chain = ROOT.TChain("tree")


"""
chain.Add("234/Sub_RUN_ana*");
chain.Add("235/Sub_RUN_ana*");
chain.Add("236/Sub_RUN_ana*");
chain.Add("237/Sub_RUN_ana*");
chain.Add("238/Sub_RUN_ana*");
chain.Add("239/Sub_RUN_ana*");
chain.Add("240/Sub_RUN_ana*");
chain.Add("241/Sub_RUN_ana*");
chain.Add("242/Sub_RUN_ana*");
  

chain.Add("251/Sub_RUN_ana*");
chain.Add("252/Sub_RUN_ana*");
chain.Add("254/Sub_RUN_ana*");
  
chain.Add("ana_281/Sub_RUN_ana*");
chain.Add("ana_289/Sub_RUN_ana*");


chain.Add("298/Sub_RUN_ana*");
chain.Add("299/Sub_RUN_ana*");
chain.Add("300/Sub_RUN_ana*");
chain.Add("302/Sub_RUN_ana*");


chain.Add("303/Sub_RUN_ana*");
chain.Add("305/Sub_RUN_ana*");
chain.Add("306/Sub_RUN_ana*");


"""
chain.Add("318/Sub_RUN_ana*");
chain.Add("325/Sub_RUN_ana*");
chain.Add("326/Sub_RUN_ana*");




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



	###############################################################################################################################
	###############################################################################################################################

	h = dict()
	fitFunc = dict()
	fitFunc2 = dict()




	#for feb_number in Tfine_dict.keys():
	for feb_number in range(48, 58):

		if feb_number < 16:
			layer_number = 1
		elif feb_number < 44:
			layer_number = 2
		else:
			layer_number = 3

		try:
			ll = map_dict[feb_number][0]
			HW_feb = map_dict[feb_number][1]	
		except :
			ll = 0
			HW_feb = 99

		if ll != layer_number:
			print("\n\n")
			print("*********************************************************************")
			print("**                	 LAYER ERROR				                  **")
			print("*********************************************************************")
			print("\n")
			#sys.exit()


		print("\n\n")
		print("*********************************************************************")
		print("**                 FEB_label = {} --> Layer = {}                   **".format(feb_number, layer_number))
		print("**                 FEB_label = {} --> HW_FEB = {}                  **".format(feb_number, HW_feb))
		print("*********************************************************************")
		print("\n")


		for chip_number in Tfine_dict[feb_number].keys():
		#for chip_number in range(1, 2):

			print("\nchip {}".format(chip_number))
			

			with open("TDC_calib/calib/L{}FEB{}_c{}_TDCscan.tdc".format(layer_number, HW_feb, chip_number), "w") as tdc_file:

				for channel_number in Tfine_dict[feb_number][chip_number].keys():
				#for channel_number in range(0, 5):

					print ("Preparing canvas for channel {} (FEB {} chip {})".format(channel_number, feb_number, chip_number))
					c = ROOT.TCanvas("c_{}_{}_{}".format(feb_number, chip_number, channel_number), "Tfine (FEB={}, CHIP={}, CHANNEL={})".format(feb_number, chip_number, channel_number), 70, 70, 1800, 1000)
					c.Divide(2,2)

					for tac_number in Tfine_dict[feb_number][chip_number][channel_number].keys():
						print ("TAC {}".format(tac_number))
						h[tac_number] = ROOT.TH1I("h_{}_{}_{}_{}".format(feb_number, chip_number, channel_number, tac_number), "Tfine (FEB={} ({}), CHIP={}, CHANNEL={}, TAC={})".format(feb_number, HW_feb, chip_number, channel_number, tac_number), 1024/8, 0, 1024)
						h[tac_number].SetFillColor(38)

						for x in Tfine_dict[feb_number][chip_number][channel_number][tac_number]:
							h[tac_number].Fill(x)
							
						c.cd(tac_number+1)
						print ("Drawing histograms")
						h[tac_number].Draw()

						fitFunc[tac_number] = ROOT.TF1("fitFunc_{}".format(tac_number), fermi_dirac, 0, 1023, 3)
						fitFunc2[tac_number] = ROOT.TF1("fitFunc2_{}".format(tac_number), fermi_dirac2, 0, 1023, 3)
						print ("Fitting TAC {}".format(tac_number))

						#print("MAX BIN = {}".format( h[tac_number].GetMaximumBin()) )
						#print("MAX x = {}".format( h[tac_number].GetXaxis().GetBinCenter(h[tac_number].GetMaximumBin())) )
						#print("MAX = {}\n".format( h[tac_number].GetMaximum()) )
							
						#fitFunc[tac_number].SetParameter(0, h[tac_number].GetXaxis().GetBinCenter(h[tac_number].GetMaximumBin()) + 50)
						fitFunc[tac_number].SetParameter(0, 350)
						fitFunc[tac_number].SetParLimits(0, 0, 1023)
						fitFunc[tac_number].SetParameter(1, 3)
						fitFunc[tac_number].SetParLimits(1, 1, 12)
						fitFunc[tac_number].SetParameter(2, h[tac_number].GetMaximum())
						fitFunc[tac_number].SetParLimits(2, h[tac_number].GetMaximum() * 0.75, h[tac_number].GetMaximum() * 1.0)

						h[tac_number].Fit("fitFunc_{}".format(tac_number), "Q0", "", h[tac_number].GetXaxis().GetBinCenter(h[tac_number].GetMaximumBin()), 1023)


						#fitFunc2[tac_number].SetParameter(0, h[tac_number].GetXaxis().GetBinCenter(h[tac_number].GetMaximumBin()) - 50)
						fitFunc2[tac_number].SetParameter(0, 150)
						fitFunc2[tac_number].SetParLimits(0, 0, 1023)
						fitFunc2[tac_number].SetParameter(1, fitFunc[tac_number].GetParameter(1))
						fitFunc2[tac_number].SetParLimits(1, 1, 12)
						fitFunc2[tac_number].SetParameter(2, fitFunc[tac_number].GetParameter(2))
						#fitFunc2[tac_number].SetParLimits(2, fitFunc[tac_number].GetParameter(2) * 0.9, fitFunc[tac_number].GetParameter(2) * 1.1)
						fitFunc2[tac_number].SetParLimits(2, h[tac_number].GetMaximum() * 0.75, h[tac_number].GetMaximum() * 1.0)
						
						fitFunc2[tac_number].SetLineColor(4)

						h[tac_number].Fit("fitFunc2_{}".format(tac_number), "Q0", "", 0, h[tac_number].GetXaxis().GetBinCenter(h[tac_number].GetMaximumBin()))

						print ("\nFEB_label={}, chip={}, channel={}, tac={}, Tfine MIN = {}".format( feb_number, chip_number, channel_number, tac_number, fitFunc2[tac_number].GetParameter(0)) )
						print ("FEB_label={}, chip={}, channel={}, tac={}, Tfine MAX = {}\n".format( feb_number, chip_number, channel_number, tac_number, fitFunc[tac_number].GetParameter(0)) )

						tdc_file.write( '{0:.1f}\t{1:.1f}\t0\t0\t'.format(fitFunc2[tac_number].GetParameter(0), fitFunc[tac_number].GetParameter(0)) )

						fitFunc[tac_number].Draw("same")
						fitFunc2[tac_number].Draw("same")

						print ("slope (max) = {}".format( fitFunc[tac_number].GetParameter(1) ) )
						print ("slope (min) = {}\n".format( fitFunc2[tac_number].GetParameter(1) ) )

						print ("norm (max) = {}".format( fitFunc[tac_number].GetParameter(2) ) ) 
						print ("norm (min) = {}\n".format( fitFunc2[tac_number].GetParameter(2) ) )


					c.Update()
					print ("Saving images")
					img.FromPad(c)
					img.WriteImage("TDC_calib/images/Tfine_{}_{}_{}.png".format( HW_feb, chip_number, channel_number ) )

					print ("Deleting canvas")
					c.Destructor()

					print ("Deleting histograms\n\n\n")
					for hd in h.values():
						hd.Delete()

					tdc_file.write("\n")				# new line for each channel




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
