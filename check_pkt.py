import numpy as np
import time
import sys
from array import array
import pickle
import ROOT

#from ROOT import gROOT, AddressOf, TChain

import sys
import os



#############################################################




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


#################################################################################
#################################################################################

home_folder = "/home/Fabio/analysis/Data-analysis"

try:
        RUN = int(sys.argv[1])
except:
        RUN = 383


path = "{}/CHECK_PACKETS/{}".format(home_folder, RUN)
if not(os.path.isdir(path)):
        os.mkdir(path)


#################################################################################
#################################################################################


data_path = "/dati/Data_CGEM_IHEP_Integration_2019/raw_root/{}".format(RUN)

chain = ROOT.TChain("tree")
chain.Add("{}/Sub_RUN_dec_*.root".format(data_path))


#################################################################################
#################################################################################


print("RUN = {}".format(RUN))



subrun_max = 100000
h1 = ROOT.TH1D("h1", "h1", subrun_max, 0, subrun_max)
chain.Draw("subRunNo>>h1", "", "colz")
bin = h1.FindLastBinAbove(0, 1)
subrun_max = int(h1.GetXaxis().GetBinCenter(bin)) + 2
print("subRunNo MAX = {}".format(subrun_max))
h1.Delete()


l1count_max = 100000
h1 = ROOT.TH1D("h1", "h1", l1count_max, 0, l1count_max)
chain.Draw("count>>h1", "", "colz")
bin = h1.FindLastBinAbove(0, 1)
l1count_max = int(h1.GetXaxis().GetBinCenter(bin)) + 10
print("L1 count MAX = {}".format(l1count_max))
h1.Delete()


TOT = int(chain.GetEntries())
print("TOTAL ENTRIES = {}".format(TOT))



#################################################################################
## 1. DATI SPURI

condition = "(delta_coarse==25 || delta_coarse==26)"
h1 = ROOT.TH1D("h1", "h1", 100000, 0, 100000)
h1.GetXaxis().SetTitle("count")
h1.GetYaxis().SetTitle("N")
c1 = ROOT.TCanvas("c11", "c11", 100, 100, 1600, 1000)
chain.Draw("count>>h1", condition, "colz")

TOT1 = int(h1.GetEntries())
print("TOTAL ENTRIES = {} ({} spourious removed, {:.2f}%)".format( TOT1, TOT-TOT1, (TOT-TOT1)/float(TOT)*100 ) )

c1.Update()
c1.SaveAs("{}/count.pdf".format(path))
h1.Delete()
c1.Close()
#gSystem.ProcessEvents()




#################################################################################
## 2. PACCHETTI SFASATI

condition = "(delta_coarse==25 || delta_coarse==26) && (l1ts_min_tcoarse>1299 && l1ts_min_tcoarse<1567)"
h1 = ROOT.TH1D("h1", condition, 100000, 0, 100000)
h1.GetXaxis().SetTitle("count")
h1.GetYaxis().SetTitle("N")
c1 = ROOT.TCanvas("c11", "c11", 100, 100, 1600, 1000)
chain.Draw("count>>h1", condition, "colz")

TOT2 = int(h1.GetEntries())
print(" GOOD ENTRIES = {} ({:.2f}%)".format( TOT2, TOT2/float(TOT1)*100 ) )

c1.Update()
c1.SaveAs("{}/good.pdf".format(path))
h1.Delete()
c1.Close()




#################################################################################
## 3. PACCHETTI SFASATI (errors)

condition = "(delta_coarse==25 || delta_coarse==26) && (l1ts_min_tcoarse<1299 || l1ts_min_tcoarse>1567)"
h1 = ROOT.TH2D("h1", condition, l1count_max, 0, l1count_max, 15, 0, 15)
h1.GetXaxis().SetTitle("count")
h1.GetYaxis().SetTitle("gemroc")
c1 = ROOT.TCanvas("c11", "c11", 100, 100, 1800, 1200)
chain.Draw("gemroc:count>>h1", condition, "*")

c1.Update()
c1.SaveAs("{}/COUNTvsGEMROC.pdf".format(path))
h1.Delete()
c1.Close()







#################################################################################
## 4. GEMROC

for roc in range(0, 14):
        if roc == 11:
                continue
        else:
                print ("Analyzing GEMROC {}...".format(roc))


                condition = "(delta_coarse==25 || delta_coarse==26) && (l1ts_min_tcoarse<1299 || l1ts_min_tcoarse>1567) && gemroc=={}".format(roc)
                h1 = ROOT.TH2D("h1", condition, l1count_max, 0, l1count_max, subrun_max, 0, subrun_max)
                h1.GetXaxis().SetTitle("count")
                h1.GetYaxis().SetTitle("subRunNo")
                c1 = ROOT.TCanvas("c11", "c11", 100, 100, 1800, 1200)
                chain.Draw("subRunNo:count>>h1", condition, "*")

                c1.Update()
                c1.SaveAs("{}/GEMROC_{}.pdf".format(path, roc))
                h1.Delete()
                c1.Close()







#################################################################################
#################################################################################







