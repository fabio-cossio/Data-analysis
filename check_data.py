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


path = "{}/CHECK_DATA/{}".format(home_folder, RUN)
if not(os.path.isdir(path)):
        os.mkdir(path)

f = open("{}/RUN_{}_log.txt".format(path, RUN), "w")

#################################################################################
#################################################################################


data_path = "/dati/Data_CGEM_IHEP_Integration_2019/raw_root/{}".format(RUN)

chain = ROOT.TChain("tree")
chain.Add("{}/Sub_RUN_dec_*.root".format(data_path))


#################################################################################
#################################################################################


print("\nRUN = {}".format(RUN))
f.write("\nRUN = {}\n".format(RUN))


subrun_max = 100000
h1 = ROOT.TH1D("h1", "h1", subrun_max, 0, subrun_max)
chain.Draw("subRunNo>>h1", "", "colz")
bin = h1.FindLastBinAbove(0, 1)
subrun_max = int(h1.GetXaxis().GetBinCenter(bin)) + 2
print("subRunNo MAX = {}".format(subrun_max-2))
f.write("subRunNo MAX = {}\n".format(subrun_max-2))
h1.Delete()


l1count_max = 100000
h1 = ROOT.TH1D("h1", "h1", l1count_max, 0, l1count_max)
chain.Draw("count>>h1", "", "colz")
bin = h1.FindLastBinAbove(0, 1)
l1count_max = int(h1.GetXaxis().GetBinCenter(bin)) + 10
print("L1 count MAX = {}".format(l1count_max-10))
f.write("L1 count MAX = {}\n".format(l1count_max-10))
h1.Delete()


TOT = int(chain.GetEntries())
print("TOTAL ENTRIES = {}".format(TOT))
f.write("TOTAL ENTRIES = {}\n".format(TOT))




#################################################################################
## 1. Hits per subrun

condition = "(delta_coarse==25 || delta_coarse==26)"
h1 = ROOT.TH1D("h1", condition, subrun_max, 0, subrun_max)
h1.GetXaxis().SetTitle("subRunNo")
h1.GetYaxis().SetTitle("N")
c1 = ROOT.TCanvas("c11", "c11", 100, 100, 1600, 1000)
chain.Draw("subRunNo>>h1", condition, "colz")
MAX = int(h1.GetMaximum())
print("Max. hits per subrun = {}".format(MAX))

h2 = ROOT.TH1D("h2", "Number of hits per subRun", int(MAX/300), 0, MAX+10)
h1.GetXaxis().SetTitle("# hits")
h1.GetYaxis().SetTitle("N")

l_zero = list()
l_good = list()

for binN in range(0, subrun_max):
    N = h1.GetBinContent(binN)
    h2.Fill(N)
    if N == 0:
        l_zero.append(binN-1)
    elif N > 18000:
        l_good.append(binN-1)

c2 = ROOT.TCanvas("c2", "c2", 100, 100, 1600, 1000)
h2.Draw()

c2.Update()
c2.SaveAs("{}/Hits.pdf".format(path))
h2.Delete()
c2.Close()
#gSystem.ProcessEvents()
h1.Delete()
c1.Close()

print(l_zero)
print(l_good)


#################################################################################
## 2. Hits per subrun per FEB

condition = "(delta_coarse==25 || delta_coarse==26)"
h1 = ROOT.TH2D("h1", condition, subrun_max, 0, subrun_max, 90, 0, 90)
h1.GetXaxis().SetTitle("subRunNo")
h1.GetYaxis().SetTitle("TIGER")
c1 = ROOT.TCanvas("c11", "c11", 100, 100, 1600, 1000)
chain.Draw("gemroc*8+tiger:subRunNo>>h1", condition, "colz")

for TIGER in range(0, 88):
    for subRUN in range(0, subrun_max):
        if subRUN in l_good:
            binN = h1.GetBin(subRUN+1, TIGER+1)
            N = h1.GetBinContent(binN)
            if N == 0:
                if TIGER<200:
                    print(binN, subRUN, TIGER)
                f.write("{} {} {}\n".format(binN, subRUN, TIGER))

#MAX = int(h1.GetMaximum())
#print("Max. hits per subrun = {}".format(MAX))

c1.Update()
c1.SaveAs("{}/Hits_vs_FEB.pdf".format(path))
h1.Delete()
c1.Close()
#gSystem.ProcessEvents()




#################################################################################
## 3. Hits per subrun per FEB (split)

start = 0
stop = 100

for i in range(0,subrun_max/100 + 1):

    start = i*100
    stop = (i+1)*100
    print("Analyzing subRun n. {}".format(start))

    condition = "(delta_coarse==25 || delta_coarse==26)"
    h1 = ROOT.TH2D("h1", condition, 100, start, stop, 100, 0, 100)
    h1.GetXaxis().SetTitle("subRunNo")
    h1.GetYaxis().SetTitle("TIGER")
    c1 = ROOT.TCanvas("c11", "c11", 100, 100, 1600, 1000)
    chain.Draw("gemroc*8+tiger:subRunNo>>h1", condition, "colz")
    h1.SetStats(0)
    #gPad->Update()
    #h1.FindObject("stats")

    c1.Update()
    c1.SaveAs("{}/Hits_vs_FEB_{}.pdf".format(path,start))
    h1.Delete()
    c1.Close()
    #gSystem.ProcessEvents()





"""

#################################################################################
## 2. PACCHETTI SFASATI

print("\nANALYSIS ON L1TS_MIN_TCOARSE ERRORS")
f.write("\nANALYSIS ON L1TS_MIN_TCOARSE ERRORS\n")

condition = "(delta_coarse==25 || delta_coarse==26) && (l1ts_min_tcoarse>1299 && l1ts_min_tcoarse<1567)"
h1 = ROOT.TH1D("h1", condition, l1count_max, 0, l1count_max)
h1.GetXaxis().SetTitle("count")
h1.GetYaxis().SetTitle("N")
c1 = ROOT.TCanvas("c11", "c11", 100, 100, 1600, 1000)
chain.Draw("count>>h1", condition, "colz")

TOT2 = int(h1.GetEntries())
print("GOOD ENTRIES = {} ({:.2f}%)".format( TOT2, TOT2/float(TOT1)*100 ) )
f.write("GOOD ENTRIES = {} ({:.2f}%)\n".format( TOT2, TOT2/float(TOT1)*100 ) )

c1.Update()
c1.SaveAs("{}/good.pdf".format(path))
h1.Delete()
c1.Close()

print(" BAD ENTRIES = {} ({:.2f}%)".format( TOT1-TOT2, (TOT1-TOT2)/float(TOT1)*100 ) )
f.write(" BAD ENTRIES = {} ({:.2f}%)\n".format( TOT1-TOT2, (TOT1-TOT2)/float(TOT1)*100 ) )




#################################################################################
## 3. PACCHETTI SFASATI (errors)

condition = "(delta_coarse==25 || delta_coarse==26) && (l1ts_min_tcoarse<1300 || l1ts_min_tcoarse>1566)"
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
## 4. PACCHETTI SFASATI (errors on TIGER 0-3 and 4-7)

condition = "(delta_coarse==25 || delta_coarse==26) && (l1ts_min_tcoarse<1300 || l1ts_min_tcoarse>1566) && tiger<4"
h1 = ROOT.TH2D("h1", condition, l1count_max, 0, l1count_max, 15, 0, 15)
h1.GetXaxis().SetTitle("count")
h1.GetYaxis().SetTitle("gemroc")
c1 = ROOT.TCanvas("c11", "c11", 100, 100, 1800, 1200)
chain.Draw("gemroc:count>>h1", condition, "*")
print("l1ts_min_tcoarse errors from TIGER 0-3 = {} ({:.2f}%)".format( int(h1.GetEntries()), h1.GetEntries()/(TOT1-TOT2)*100 ) )
f.write("l1ts_min_tcoarse errors from TIGER 0-3 = {} ({:.2f}%)\n".format( int(h1.GetEntries()), h1.GetEntries()/(TOT1-TOT2)*100 ) )

c1.Update()
c1.SaveAs("{}/COUNTvsGEMROC_TIGER03.pdf".format(path))
h1.Delete()
c1.Close()


condition = "(delta_coarse==25 || delta_coarse==26) && (l1ts_min_tcoarse<1300 || l1ts_min_tcoarse>1566) && tiger>3"
h1 = ROOT.TH2D("h1", condition, l1count_max, 0, l1count_max, 15, 0, 15)
h1.GetXaxis().SetTitle("count")
h1.GetYaxis().SetTitle("gemroc")
c1 = ROOT.TCanvas("c11", "c11", 100, 100, 1800, 1200)
chain.Draw("gemroc:count>>h1", condition, "*")
print("l1ts_min_tcoarse errors from TIGER 4-7 = {} ({:.2f}%)".format( int(h1.GetEntries()), h1.GetEntries()/(TOT1-TOT2)*100 ) )
f.write("l1ts_min_tcoarse errors from TIGER 4-7 = {} ({:.2f}%)\n".format( int(h1.GetEntries()), h1.GetEntries()/(TOT1-TOT2)*100 ) )

c1.Update()
c1.SaveAs("{}/COUNTvsGEMROC_TIGER47.pdf".format(path))
h1.Delete()
c1.Close()


print("\n")
f.write("\n")




#################################################################################
## 5. GEMROC

for roc in range(0, 14):
        if roc == 11:
                continue
        else:
                print ("Analyzing GEMROC {}...".format(roc))
                f.write("Analyzing GEMROC {}...\n".format(roc))


                condition = "(delta_coarse==25 || delta_coarse==26) && (l1ts_min_tcoarse<1300 || l1ts_min_tcoarse>1566) && gemroc=={}".format(roc)
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


"""

print("\nDone\n\n")
f.write("\nDone\n\n")



f.close()


