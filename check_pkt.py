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



full_analysis = False

try:

    if sys.argv[1] == "all":
        run = [351, 368, 370, 372, 375, 355, 376, 377, 378, 387, 380, 383, 384, 385]

        full_analysis = True
        ht1 = ROOT.TH1D("ht1", "No hits (TIGER) all RUNs", 100, 0, 100)
        ht1.GetXaxis().SetTitle("TIGER")
        ht1.GetYaxis().SetTitle("N")

        ht2 = ROOT.TH1D("ht2", "No hits (FEB) all RUNs", 50, 0, 50)
        ht2.GetXaxis().SetTitle("FEB")
        ht2.GetYaxis().SetTitle("N")

        ht3 = ROOT.TH1D("ht3", "No hits (GEMROC) all RUNs", 15, 0, 15)
        ht3.GetXaxis().SetTitle("GEMROC")
        ht3.GetYaxis().SetTitle("N")

    else:
        run = [int(sys.argv[1])]

except:
    run = [383]



print("\n\nPerforming DATA QUALITY analysis on the following RUNs {}".format(run))

for RUN in run:



    path = "{}/CHECK_PACKETS/{}".format(home_folder, RUN)
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
    ## 1. DATI SPURI

    condition = "(delta_coarse==25 || delta_coarse==26)"
    h1 = ROOT.TH1D("h1", condition, l1count_max, 0, l1count_max)
    h1.GetXaxis().SetTitle("count")
    h1.GetYaxis().SetTitle("N")
    c1 = ROOT.TCanvas("c11", "c11", 100, 100, 1600, 1000)
    chain.Draw("count>>h1", condition, "colz")

    TOT1 = int(h1.GetEntries())
    print("TOTAL ENTRIES = {} ({} spurious removed, {:.2f}%)".format( TOT1, TOT-TOT1, (TOT-TOT1)/float(TOT)*100 ) )
    f.write("TOTAL ENTRIES = {} ({} spurious removed, {:.2f}%)\n".format( TOT1, TOT-TOT1, (TOT-TOT1)/float(TOT)*100 ) )

    c1.Update()
    c1.SaveAs("{}/count.pdf".format(path))
    c1.SaveAs("{}/count.png".format(path))
    c1.SaveAs("{}/count.root".format(path))
    h1.Delete()
    c1.Close()
    #gSystem.ProcessEvents()




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
    c1.SaveAs("{}/good.png".format(path))
    c1.SaveAs("{}/good.root".format(path))
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
    chain.Draw("gemroc:count>>h1", condition, "count")
    
    c1.Update()
    c1.SaveAs("{}/COUNTvsGEMROC.pdf".format(path))
    c1.SaveAs("{}/COUNTvsGEMROC.png".format(path))
    c1.SaveAs("{}/COUNTvsGEMROC.root".format(path))
    h1.Delete()
    c1.Close()




    #################################################################################
    ## 4. PACCHETTI SFASATI (errors on TIGER 0-3 and 4-7)

    condition = "(delta_coarse==25 || delta_coarse==26) && (l1ts_min_tcoarse<1300 || l1ts_min_tcoarse>1566) && tiger<4"
    h1 = ROOT.TH2D("h1", condition, l1count_max, 0, l1count_max, 15, 0, 15)
    h1.GetXaxis().SetTitle("count")
    h1.GetYaxis().SetTitle("gemroc")
    c1 = ROOT.TCanvas("c11", "c11", 100, 100, 1800, 1200)
    chain.Draw("gemroc:count>>h1", condition, "colz")
    print("l1ts_min_tcoarse errors from TIGER 0-3 = {} ({:.2f}%)".format( int(h1.GetEntries()), h1.GetEntries()/(TOT1-TOT2)*100 ) )
    f.write("l1ts_min_tcoarse errors from TIGER 0-3 = {} ({:.2f}%)\n".format( int(h1.GetEntries()), h1.GetEntries()/(TOT1-TOT2)*100 ) )
    
    c1.Update()
    c1.SaveAs("{}/COUNTvsGEMROC_TIGER03.pdf".format(path))
    c1.SaveAs("{}/COUNTvsGEMROC_TIGER03.png".format(path))
    c1.SaveAs("{}/COUNTvsGEMROC_TIGER03.root".format(path))
    h1.Delete()
    c1.Close()


    condition = "(delta_coarse==25 || delta_coarse==26) && (l1ts_min_tcoarse<1300 || l1ts_min_tcoarse>1566) && tiger>3"
    h1 = ROOT.TH2D("h1", condition, l1count_max, 0, l1count_max, 15, 0, 15)
    h1.GetXaxis().SetTitle("count")
    h1.GetYaxis().SetTitle("gemroc")
    c1 = ROOT.TCanvas("c11", "c11", 100, 100, 1800, 1200)
    chain.Draw("gemroc:count>>h1", condition, "colz")
    print("l1ts_min_tcoarse errors from TIGER 4-7 = {} ({:.2f}%)".format( int(h1.GetEntries()), h1.GetEntries()/(TOT1-TOT2)*100 ) )
    f.write("l1ts_min_tcoarse errors from TIGER 4-7 = {} ({:.2f}%)\n".format( int(h1.GetEntries()), h1.GetEntries()/(TOT1-TOT2)*100 ) )

    c1.Update()
    c1.SaveAs("{}/COUNTvsGEMROC_TIGER47.pdf".format(path))
    c1.SaveAs("{}/COUNTvsGEMROC_TIGER47.png".format(path))
    c1.SaveAs("{}/COUNTvsGEMROC_TIGER47.root".format(path))
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
            print ("\nAnalyzing GEMROC {}...".format(roc))
            f.write("\nGEMROC {}:\n".format(roc))


            condition = "(delta_coarse==25 || delta_coarse==26) && (l1ts_min_tcoarse<1300 || l1ts_min_tcoarse>1566) && gemroc=={}".format(roc)
            h1 = ROOT.TH2D("h1", condition, l1count_max, 0, l1count_max, subrun_max, 0, subrun_max)
            h1.GetXaxis().SetTitle("count")
            h1.GetYaxis().SetTitle("subRunNo")
            c1 = ROOT.TCanvas("c11", "c11", 100, 100, 1800, 1200)
            chain.Draw("subRunNo:count>>h1", condition, "colz")

            c1.Update()
            c1.SaveAs("{}/GEMROC_{}.pdf".format(path, roc))
            c1.SaveAs("{}/GEMROC_{}.png".format(path, roc))
            c1.SaveAs("{}/GEMROC_{}.root".format(path, roc))
            h1.Delete()
            c1.Close()

            condition = "(delta_coarse==25 || delta_coarse==26) && (l1ts_min_tcoarse<1300 || l1ts_min_tcoarse>1566) && count>30 && gemroc=={}".format(roc)
            h1 = ROOT.TH1D("h1", condition, subrun_max, 0, subrun_max)
            h1.GetXaxis().SetTitle("subRunNo")
            h1.GetYaxis().SetTitle("N")
            c1 = ROOT.TCanvas("c11", "c11", 100, 100, 1800, 1200)
            chain.Draw("subRunNo>>h1", condition, "*")
            for subrun_bin in range(0, subrun_max):
                N = int(h1.GetBinContent(subrun_bin))
                if N > 0:
                    print( "BAD subRUN = {} ({})".format(subrun_bin - 1, N) )
                    f.write( "BAD subRUN = {}\n".format(subrun_bin - 1) )

            c1.Update()
            c1.SaveAs("{}/badSubRUN_GEMROC_{}.pdf".format(path, roc))
            c1.SaveAs("{}/badSubRUN_GEMROC_{}.png".format(path, roc))
            c1.SaveAs("{}/badSubRUN_GEMROC_{}.root".format(path, roc))
            h1.Delete()
            c1.Close()



    #################################################################################
    #################################################################################


    print("\nDone\n\n")
    f.write("\nDone\n\n")

    f.close()


