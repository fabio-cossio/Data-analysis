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


is_tdc_calib = True
is_check_data = False
is_coarse_counters = False


ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gErrorIgnoreLevel = ROOT.kWarning


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


pickle.dump( map_dict, open( "TDC_folder/mapping.pickle", "wb" ) )


#################################################################################
#################################################################################




##################################################################

# TDC calibration

##################################################################


if is_tdc_calib:

        
	#run_list = [338, 339, 340, 341, 342, 343, 351]
	run_list = [351, 353, 355, 356, 357, 360, 365, 368, 370, 372, 375, 376, 377, 378, 380]


	#img = ROOT.TImage.Create()

	out_file = ROOT.TFile("TDC_folder/Tfine.root", "RECREATE")
	if out_file.IsOpen():
		print("ROOT file opened successfully")
	else:
		print("Error while opening ROOT file")


	print("\nImporting pickle with Tfine data...\n")

	pickle_list = list()
	for run in run_list:
		with open('TDC_folder/Tfine_{}.pickle'.format(run), 'rb') as handle:
			print("Reading data from run {}...".format(run) )
			Tfine_dict = pickle.load(handle)
			pickle_list.append(Tfine_dict)

	print("\nImport finished.\n")


	###############################################################################################################################
	###############################################################################################################################

	h = dict()
	fitFunc = dict()
	fitFunc2 = dict()



	fit_error_list = list()

	c_dT = ROOT.TCanvas("c_dT", "Interpolation factor", 270, 270, 800, 600)
	h_dT = ROOT.TH1D("h_dT", "Interpolation factor", 600, 0, 300)

	#c_dT2 = ROOT.TCanvas("c_dT2", "Interpolation factor scatter plot", 370, 300, 800, 600)
	#h_dT2 = ROOT.TH2D("h_dT2", "Interpolation factor scatter plot", 30000, 0, 30000, 600, 0, 300)


	for feb_number in Tfine_dict.keys():
	#for feb_number in range(16, 56):
	#for feb_number in range(31, 32):
	#for feb_number in range(28, 29):
	#for feb_number in range(14, 20):


		#if (feb_number > 43 and feb_number < 48) or (feb_number > 49 and feb_number < 52) or feb_number > 55:
		if feb_number > 43:
			continue


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
			print("\n")
			print("*********************************************************************")
			print("**                           LAYER ERROR                           **")
			print("*********************************************************************")
			print("\n")
			#sys.exit()


		print("\n")
		print("*********************************************************************")
		print("**                 FEB_label = {} --> Layer = {}                   **".format(feb_number, layer_number))
		print("**                 FEB_label = {} --> HW_FEB = {}                  **".format(feb_number, HW_feb))
		print("*********************************************************************")
		print("\n")



		for chip_number in Tfine_dict[feb_number].keys():
		#for chip_number in range(1, 2):

			print("\nchip {}".format(chip_number))
		
			h_dT2 = ROOT.TH2D("h_dT2_{}_{}".format(feb_number, chip_number), "Interpolation factor scatter plot (FEB{} chip{})".format(feb_number, chip_number), 70*4, 0, 70, 175, -50, 300)
			h_dT2.SetMarkerStyle(3)

			#with open("TDC_calib/calib/L{}FEB{}_c{}_TDC_calib.tdc".format(layer_number, feb_number, chip_number), "w") as tdc_file:
			with open("TDC_folder/calib/L{}FEB{}_c{}_TDCscan.tdc".format(layer_number, HW_feb, chip_number), "w") as tdc_file:

				for channel_number in Tfine_dict[feb_number][chip_number].keys():
				#for channel_number in range(0, 5):


					tdc_file.write( '{}\t'.format(channel_number) )

					if layer_number == 2 and channel_number > 60:
						#h_dT2.SetMarkerColor(4)
                                                continue

					if layer_number == 3 and channel_number > 61:
                                                continue
						#h_dT2.SetMarkerColor(4)


					#print ("Preparing canvas for channel {} (FEB {} chip {})".format(channel_number, feb_number, chip_number))
					c = ROOT.TCanvas("c_{}_{}_{}".format(feb_number, chip_number, channel_number), "Tfine (FEB={}, CHIP={}, CHANNEL={})".format(feb_number, chip_number, channel_number), 170, 170, 1600, 800)
					c.Divide(2,2)

					bad_tdc = False

					for tac_number in Tfine_dict[feb_number][chip_number][channel_number].keys():
						#print ("TAC {}".format(tac_number))
						#h[tac_number] = ROOT.TH1I("h_{}_{}_{}_{}".format(feb_number, chip_number, channel_number, tac_number), "Tfine (FEB={}, CHIP={}, CHANNEL={}, TAC={})".format(feb_number, chip_number, channel_number, tac_number), 1024/8, 0, 1024)
						h[tac_number] = ROOT.TH1I("h_{}_{}_{}_{}".format(feb_number, chip_number, channel_number, tac_number), "Tfine (FEB={} ({}), CHIP={}, CHANNEL={}, TAC={})".format(feb_number, HW_feb, chip_number, channel_number, tac_number), int(1024/8), 0, 1024)

						h[tac_number].SetFillColor(38)
                                                
						"""
						for x in Tfine_dict[feb_number][chip_number][channel_number][tac_number]:
							if channel_number != 62:
								h[tac_number].Fill(x)

						for x in Tfine_dict2[feb_number][chip_number][channel_number][tac_number]:
							if channel_number != 62:
								h[tac_number].Fill(x)
 						"""
						
						"""
						for x in Tfine_dict[feb_number][chip_number][channel_number][tac_number]:
							h[tac_number].Fill(x)
						
 						for x in Tfine_dict2[feb_number][chip_number][channel_number][tac_number]:
							h[tac_number].Fill(x)
						"""
                                                
						for d in pickle_list:
							for x in d[feb_number][chip_number][channel_number][tac_number]:
								h[tac_number].Fill(x)

						c.cd(tac_number+1)
						#print ("Drawing histograms")
						h[tac_number].Draw()

						fitFunc[tac_number] = ROOT.TF1("fitFunc_{}".format(tac_number), fermi_dirac, 100, 800, 3)		## MAX
						fitFunc2[tac_number] = ROOT.TF1("fitFunc2_{}".format(tac_number), fermi_dirac2, 5, 500, 3)		## MIN
						#print ("Fitting TAC {}".format(tac_number))

						#print("MAX BIN = {}".format( h[tac_number].GetMaximumBin()) )
						#print("MAX x = {}".format( h[tac_number].GetXaxis().GetBinCenter(h[tac_number].GetMaximumBin())) )
						#print("MAX = {}\n".format( h[tac_number].GetMaximum()) )
							
						#fitFunc[tac_number].SetParameter(0, h[tac_number].GetXaxis().GetBinCenter(h[tac_number].GetMaximumBin()) + 50)
						


						integ = h[tac_number].Integral()

						min_bin = 0
						max_bin = 0

						for tf in range(2, 100):
							#h[tac_number].GetXaxis().SetRange(tf, tf)
							count = h[tac_number].GetBinContent(tf)
							#print count
							if count > 5:
								min_bin = tf - 1
								break

						x_min = h[tac_number].GetBinCenter(min_bin) - 20
						#print( "MIN BIN = {} ({}), count = {}".format( min_bin, x_min, count ) )

						for tf in range(2, 100):
							bin_num = 102 - tf
							count = h[tac_number].GetBinContent(bin_num)
							#print count
							if count > 5:
								max_bin = bin_num + 1
								break

						x_max = h[tac_number].GetBinCenter(max_bin) + 20
						#print( "MAX BIN = {} ({}), count = {}".format( max_bin, x_max, count ) )




						h[tac_number].GetXaxis().SetRange(5, 1000)

						fitFunc[tac_number].SetParameter(0, x_max-50)
						fitFunc[tac_number].SetParLimits(0, x_max-150, x_max+50)
						fitFunc[tac_number].SetParameter(1, 5)
						fitFunc[tac_number].SetParLimits(1, 1, 10)
						fitFunc[tac_number].SetParameter(2, h[tac_number].GetMaximum())
						fitFunc[tac_number].SetParLimits(2, h[tac_number].GetMaximum() * 0.9, h[tac_number].GetMaximum() * 1.2)

						#h[tac_number].Fit("fitFunc_{}".format(tac_number), "Q0", "", h[tac_number].GetXaxis().GetBinCenter(h[tac_number].GetMaximumBin()), 1023)
						h[tac_number].Fit("fitFunc_{}".format(tac_number), "RQ0", "", x_max-150, x_max+50)


						#fitFunc2[tac_number].SetParameter(0, h[tac_number].GetXaxis().GetBinCenter(h[tac_number].GetMaximumBin()) - 50)
						fitFunc2[tac_number].SetParameter(0, x_min+50)
						fitFunc2[tac_number].SetParLimits(0, x_min-50, x_min+150)
						fitFunc2[tac_number].SetParameter(1, fitFunc[tac_number].GetParameter(1))
						fitFunc2[tac_number].SetParLimits(1, 1, 10)
						fitFunc2[tac_number].SetParameter(2, fitFunc[tac_number].GetParameter(2))
						#fitFunc2[tac_number].SetParLimits(2, fitFunc[tac_number].GetParameter(2) * 0.9, fitFunc[tac_number].GetParameter(2) * 1.1)
						fitFunc2[tac_number].SetParLimits(2, h[tac_number].GetMaximum() * 0.9, h[tac_number].GetMaximum() * 1.2)
						
						fitFunc2[tac_number].SetLineColor(4)

						#h[tac_number].Fit("fitFunc2_{}".format(tac_number), "Q0", "", 0, h[tac_number].GetXaxis().GetBinCenter(h[tac_number].GetMaximumBin()))
						h[tac_number].Fit("fitFunc2_{}".format(tac_number), "RQ0", "", max(x_min-50, 50), x_min+150)


						Tfine_MAX = fitFunc[tac_number].GetParameter(0)
						Tfine_MIN = fitFunc2[tac_number].GetParameter(0)
						dT = Tfine_MAX - Tfine_MIN


						#if Tfine_MIN < 50 or Tfine_MIN > 300 or Tfine_MAX < 200 or Tfine_MAX > 650 or dT < 100 or dT > 180:
						if Tfine_MIN < 50 or Tfine_MIN > 300 or Tfine_MAX < 200 or Tfine_MAX > 450 or dT < 100 or dT > 180:
							h[tac_number].Fit("fitFunc_{}".format(tac_number), "MRQ0", "", x_max-150, x_max+50)
							h[tac_number].Fit("fitFunc2_{}".format(tac_number), "MRQ0", "", max(x_min-50, 50), x_min+150)

							Tfine_MAX = fitFunc[tac_number].GetParameter(0)
							Tfine_MIN = fitFunc2[tac_number].GetParameter(0)
							dT = Tfine_MAX - Tfine_MIN


						h[tac_number].GetXaxis().SetRange(0, 1023)

						#print ("\nFEB_label={}, chip={}, channel={}, tac={}, Tfine MIN = {}".format( feb_number, chip_number, channel_number, tac_number, Tfine_MIN ) )
						#print ("FEB_label={}, chip={}, channel={}, tac={}, Tfine MAX = {}\n".format( feb_number, chip_number, channel_number, tac_number, Tfine_MAX ) )

						#tdc_file.write( '{0:.2f} {1:.2f} '.format(fitFunc2[tac_number].GetParameter(0), fitFunc[tac_number].GetParameter(0)) )
						tdc_file.write( '{0:.1f}\t{1:.1f}\t0\t0\t'.format(Tfine_MIN, Tfine_MAX ) )
						

						h_dT.Fill(dT)
						h_dT2.Fill((channel_number*4 + tac_number)/4., dT)
						
						if Tfine_MIN < 50 or Tfine_MIN > 300 or Tfine_MAX < 200 or Tfine_MAX > 450 or dT < 120 or dT > 180 or integ < 300:
							if layer_number == 1:
                                                                if not( feb_number==8 and chip_number==1 and (channel_number==0 or channel_number==42 or channel_number==38 or channel_number==16 or channel_number==45 or channel_number==57 or channel_number==8 or channel_number==21 or channel_number==47 or channel_number==10 ) ) and not( feb_number==0 and chip_number==2 and (channel_number==3 or channel_number==11 or channel_number==22 or channel_number==4 or channel_number==45 or channel_number==47 or channel_number==54 or channel_number==41 or channel_number==43 ) ):                               ## disconnected channels
                                                                        fit_error_list.append([ll, HW_feb, chip_number, channel_number, tac_number, Tfine_MIN, Tfine_MAX, dT, integ])
                                                                        print( "L{0}FEB{1}_c{2}\tch {3}\ttac {4}\tMIN={5:.1f}\tMAX={6:.1f}\tdelta={7:.1f}    N={8}".format( ll, HW_feb, chip_number, channel_number, tac_number, Tfine_MIN, Tfine_MAX, dT, integ ) )
                                                                        bad_tdc = True
							elif layer_number == 2 and (channel_number < 61):
                                                                if not( (feb_number==43 or feb_number==36) and chip_number==1 and channel_number==57):                               ## disconnected channels
                                                                        fit_error_list.append([ll, HW_feb, chip_number, channel_number, tac_number, Tfine_MIN, Tfine_MAX, dT, integ])
                                                                        print( "L{0}FEB{1}_c{2}\tch {3}\ttac {4}\tMIN={5:.1f}\tMAX={6:.1f}\tdelta={7:.1f}    N={8}".format( ll, HW_feb, chip_number, channel_number, tac_number, Tfine_MIN, Tfine_MAX, dT, integ ) )
                                                                        bad_tdc = True
							elif layer_number == 3 and (channel_number < 62):
								fit_error_list.append([ll, HW_feb, chip_number, channel_number, tac_number, Tfine_MIN, Tfine_MAX, dT, integ])
								print( "L{0}FEB{1}_c{2}\tch {3}\ttac {4}\tMIN={5:.1f}\tMAX={6:.1f}\tdelta={7:.1f}    N={8}".format( ll, HW_feb, chip_number, channel_number, tac_number, Tfine_MIN, Tfine_MAX, dT, integ ) )
								bad_tdc = True

						fitFunc[tac_number].Draw("same")
						fitFunc2[tac_number].Draw("same")

						#print ("slope (max) = {}".format( fitFunc[tac_number].GetParameter(1) ) )
						#print ("slope (min) = {}".format( fitFunc2[tac_number].GetParameter(1) ) )

						#print ("norm (max) = {}".format( fitFunc[tac_number].GetParameter(2) ) ) 
						#print ("norm (min) = {}\n".format( fitFunc2[tac_number].GetParameter(2) ) )


					c.Update()
					#img.FromPad(c)
					#img.WriteImage("TDC_calib/images/L{}/Tfine_L{}_{}_{}_{}.png".format( ll, ll, HW_feb, chip_number, channel_number ) )
					c.SaveAs( "TDC_folder/images/L{}/Tfine_L{}_{}_{}_{}.pdf".format( ll, ll, HW_feb, chip_number, channel_number ) )
					c.Write()

					if bad_tdc:
						c.SaveAs("TDC_folder/images/bad/Tfine_L{}_{}_{}_{}.pdf".format( ll, HW_feb, chip_number, channel_number ) )

					#print ("Deleting canvas")
					#c.Destructor()

					#print ("Deleting histograms\n\n\n")
					for hd in h.values():
						hd.Delete()

					tdc_file.write("\n")				# new line for each channel



			h_dT2.Draw("*")
			h_dT2.Write()
	


	#ROOT.gROOT.SetBatch(ROOT.kFALSE)

	c_dT.cd(1)
	h_dT.Draw()
	#img.FromPad(c_dT)
	c_dT.SaveAs("TDC_folder/IF.pdf")
	h_dT.Write()


	#c_dT2.cd(1)
	#h_dT2.Draw()
	#img.FromPad(c_dT2)
	#img.WriteImage("TDC_folder/IF2.png")
	#h_dT2.Write()


	out_file.Close()


	print("\n\nFEB summary\n")

	with open("TDC_folder/summary.txt".format(layer_number, HW_feb, chip_number), "w") as summary_file:
                for err in fit_error_list:
                        print( "L{0}FEB{1}_c{2}\tch {3}\ttac {4}\tMIN={5:.1f}\tMAX={6:.1f}\tdelta={7:.1f}    N={8}".format( err[0], err[1], err[2], err[3], err[4], err[5], err[6], err[7], err[8] ) )
                        summary_file.write("L{0}FEB{1}_c{2}\tch {3}\ttac {4}\tMIN={5:.1f}\tMAX={6:.1f}\tdelta={7:.1f}    N={8}\n".format( err[0], err[1], err[2], err[3], err[4], err[5], err[6], err[7], err[8] ) )



if is_coarse_counters or is_check_data:

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
	  
	"""
	chain.Add("ana_281/Sub_RUN_ana*");
	chain.Add("ana_289/Sub_RUN_ana*");

	chain.Add("298/Sub_RUN_ana*");
	chain.Add("299/Sub_RUN_ana*");
	chain.Add("300/Sub_RUN_ana*");
	chain.Add("302/Sub_RUN_ana*");

	chain.Add("303/Sub_RUN_ana*");
	chain.Add("305/Sub_RUN_ana*");
	chain.Add("306/Sub_RUN_ana*");

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


	mystruct = ROOT.TreeStruct()


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
	efine_uncal = array( 'f', [0] )
	chain.SetBranchAddress( "efine_uncal", efine_uncal )
	tcoarse = array( 'f', [0] )
	chain.SetBranchAddress( "tcoarse", tcoarse )
	ecoarse = array( 'f', [0] )
	chain.SetBranchAddress( "ecoarse", ecoarse )
	charge_SH = array( 'f', [0] )
	chain.SetBranchAddress( "charge_SH", charge_SH )










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





##################################################################

# Check data quality

##################################################################

FEB_errors = list()

if is_check_data:

	for i in range( chain.GetEntries() ):
		chain.GetEntry( i )
		
		#if i%100000 == 0:
		#	print ("READ {} hits".format(i) )
		
		if tfine_uncal[0] == 0 or tfine_uncal[0] > 900:
			print (layer[0], FEB_label[0], chip[0], channel[0], tac[0], tfine_uncal[0], efine_uncal[0], charge_SH[0], tcoarse[0], ecoarse[0])
			FEB_errors.append(FEB_label[0])

	
	

















#rootFile = ROOT.TFile(rname, 'recreate')
#tree = ROOT.TTree('tree', '')
#mystruct = ROOT.TreeStruct()
