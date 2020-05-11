import numpy as np
import time
import sys
from array import array
import pickle
import ROOT

#from ROOT import gROOT, AddressOf, TChain

import sys
import os
import glob



#############################################################




OS = sys.platform
if OS == 'win32':
    sep = '\\'
elif OS == 'linux2' or OS == "linux":
    sep = '/'
else:
    print("ERROR: OS {} non compatible".format(OS))
    sys.exit()

home_folder = "/home/Fabio/analysis/Data-analysis"
Data_path = "/dati/Data_CGEM_IHEP_Integration_2019/raw_root/"
path = "{}/data_quality".format(home_folder)
if not(os.path.isdir(path)):
    os.mkdir(path)


ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gErrorIgnoreLevel = ROOT.kWarning


#################################################################################
#################################################################################

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

    path = "{}/data_quality/{}".format(home_folder, RUN)
    if not(os.path.isdir(path)):
        os.mkdir(path)
    root_dir = "{}/root".format(path)
    if not( os.path.isdir( root_dir ) ):
        os.mkdir(root_dir)
    pdf_dir = "{}/pdf".format(path)
    if not( os.path.isdir( pdf_dir ) ):
        os.mkdir(pdf_dir)
    png_dir = "{}/png".format(path)
    if not( os.path.isdir( png_dir ) ):
        os.mkdir(png_dir)

    f = open("{}/RUN_{}_data_log.txt".format(path, RUN), "w")

    #################################################################################
    #################################################################################


    data_path = "{}{}".format(Data_path, RUN)



    BAD_SUBRUNs_low = list()
    BAD_SUBRUNs_holes = list()
    for name in glob.glob("{}/badSubRUN/lowevent/Sub_RUN_event*".format(data_path)):
        BAD_SUBRUNs_low.append( int( name.split("/")[-1].split("_")[-1].split(".")[0] ) )
    for name in glob.glob("{}/badSubRUN/nofireFEB/Sub_RUN_event*".format(data_path)):
        BAD_SUBRUNs_holes.append( int( name.split("/")[-1].split("_")[-1].split(".")[0] ) )

    #print BAD_SUBRUNs_low
    #print BAD_SUBRUNs_holes


    BAD_SUBRUNs_low_dec = list()
    BAD_SUBRUNs_holes_dec = list()



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



    h2 = ROOT.TH1D("h2", "Number of hits per subRun", int(MAX/400), 0, MAX+10)
    h2.GetXaxis().SetTitle("# hits")
    h2.GetYaxis().SetTitle("N")

    for binN in range(0, subrun_max):
        N = h1.GetBinContent(binN)
        h2.Fill(N)

    c2 = ROOT.TCanvas("c2", "c2", 100, 100, 1600, 1000)
    h2.Draw()
    h2.Fit("gaus", "", "", h2.GetMean()-h2.GetMean()/5, MAX+10)
    g = h2.GetListOfFunctions().FindObject("gaus")
    mu = g.GetParameter(1)
    sigma = g.GetParameter(2)
    cut = mu - 4*sigma
    print mu, sigma, cut
    line_cut = ROOT.TLine(cut,0, cut,h2.GetMaximum())
    line_cut.Draw()

    c2.Update()
    c2.SaveAs("{}/Hits.pdf".format(pdf_dir))
    c2.SaveAs("{}/Hits.png".format(png_dir))
    c2.SaveAs("{}/Hits.root".format(root_dir))
    h2.Delete()
    c2.Close()



    l_zero = list()
    l_low = list()
    l_good = list()

    for binN in range(0, subrun_max):
        N = h1.GetBinContent(binN)
        if N == 0:
            l_zero.append(binN-1)
            l_low.append(binN-1)
        elif N > cut:
            l_good.append(binN-1)
        else:
            l_low.append(binN-1)
            

    h1.Delete()
    c1.Close()

    print("\n\nEMPTY SUBRUNs = {}\n\n".format(l_zero))
    print("GOOD SUBRUNs ({}) = {}\n".format(len(l_good), l_good))
    print("LOW ENTRIES SUBRUNs = {}\n\n".format(l_low))
    f.write("EMPTY SUBRUNs = {}\n\n".format(l_zero))
    f.write("GOOD SUBRUNs ({}) = {}\n\n".format(len(l_good), l_good))
    f.write("LOW ENTRIES SUBRUNs = {}\n".format(l_low))

    BAD_SUBRUNs_low_dec = l_low



    #################################################################################
    ## 2. Hits per subrun per TIGER

    f.write("\n\nTIGER with no hits\n")
    f.write("\nsubRUN\tTIGER\n")
    print("\n\nTIGER with no hits\n")
    print("subRUN\tTIGER\n")

    condition = "(delta_coarse==25 || delta_coarse==26)"
    h1 = ROOT.TH2D("h1", condition, subrun_max, 0, subrun_max, 90, 0, 90)
    h1.GetXaxis().SetTitle("subRunNo")
    h1.GetYaxis().SetTitle("TIGER")
    c1 = ROOT.TCanvas("c11", "c11", 100, 100, 1600, 1000)
    chain.Draw("gemroc*8+tiger:subRunNo>>h1", condition, "colz")

    line_tiger = list()
    for i in range(0, 23):
        line_tiger.append(ROOT.TLine(0, i*4, subrun_max, i*4))
        line_tiger[i].Draw()
        line_tiger[i].SetLineStyle(7)
        line_tiger[i].SetLineWidth(1)

    
    h2 = ROOT.TH1D("h2", "No hits (TIGER)", 100, 0, 100)
    h2.GetXaxis().SetTitle("TIGER")
    h2.GetYaxis().SetTitle("N")


    for subRUN in range(0, subrun_max):
        if subRUN in l_good:
            for TIGER in range(0, 88):
                binN = h1.GetBin(subRUN+1, TIGER+1)
                N = h1.GetBinContent(binN)
                if N == 0:
                    if (RUN < 375 or TIGER != 69) and (RUN < 376 or TIGER != 68):
                        h2.Fill(TIGER)
                        print("{}\t{}".format(subRUN, TIGER))
                        f.write("{}\t{}\n".format(subRUN, TIGER))
                        if not(subRUN in BAD_SUBRUNs_holes_dec):
                            BAD_SUBRUNs_holes_dec.append(subRUN)

                        if full_analysis and RUN != 368:
                            ht1.Fill(TIGER)


    c1.Update()
    c1.SaveAs("{}/Hits_vs_TIGER.pdf".format(pdf_dir))
    c1.SaveAs("{}/Hits_vs_TIGER.png".format(png_dir))
    c1.SaveAs("{}/Hits_vs_TIGER.root".format(root_dir))
    h1.Delete()
    c1.Close()

    c2 = ROOT.TCanvas("c2", "c2", 100, 100, 1600, 1000)
    h2.Draw()

    c2.Update()
    c2.SaveAs("{}/noHits_TIGER.pdf".format(pdf_dir))
    c2.SaveAs("{}/noHits_TIGER.png".format(png_dir))
    c2.SaveAs("{}/noHits_TIGER.root".format(root_dir))
    h2.Delete()
    c2.Close()




    #################################################################################
    ## 3. Hits per subrun per TIGER (split)

    start = 0
    stop = 100

    for i in range(0,subrun_max/100 + 1):

        start = i*100
        stop = (i+1)*100
        print("Saving plots for subRun n. {}".format(start))

        condition = "(delta_coarse==25 || delta_coarse==26)"
        h1 = ROOT.TH2D("h1", condition, 100, start, stop, 100, 0, 100)
        h1.GetXaxis().SetTitle("subRunNo")
        h1.GetYaxis().SetTitle("TIGER")
        c1 = ROOT.TCanvas("c11", "c11", 100, 100, 1600, 1000)
        chain.Draw("gemroc*8+tiger:subRunNo>>h1", condition, "colz")
        h1.SetStats(0)

        line_tiger = list()
        for i in range(0, 23):
            line_tiger.append(ROOT.TLine(start, i*4, stop, i*4))
            line_tiger[i].Draw()
            line_tiger[i].SetLineStyle(7)
            line_tiger[i].SetLineWidth(1)

        #gPad->Update()
        #h1.FindObject("stats")

        c1.Update()
        c1.SaveAs("{}/Hits_vs_TIGER_{}.pdf".format(pdf_dir, start))
        c1.SaveAs("{}/Hits_vs_TIGER_{}.png".format(png_dir, start))
        c1.SaveAs("{}/Hits_vs_TIGER_{}.root".format(root_dir, start))
        h1.Delete()
        c1.Close()




    #################################################################################
    ## 4. Hits per subrun per FEB

    f.write("\n\nFEBs with no hits\n")
    f.write("\nsubRUN\tFEB\n")
    print("\n\nFEB with no hits\n")
    print("subRUN\tFEB\n")

    condition = "(delta_coarse==25 || delta_coarse==26)"
    h1 = ROOT.TH2D("h1", condition, subrun_max, 0, subrun_max, 46, 0, 46)
    h1.GetXaxis().SetTitle("subRunNo")
    h1.GetYaxis().SetTitle("FEB")
    c1 = ROOT.TCanvas("c11", "c11", 100, 100, 1600, 1000)
    chain.Draw("gemroc*4+tiger/2:subRunNo>>h1", condition, "colz")

    h2 = ROOT.TH1D("h2", "No hits (FEB)", 50, 0, 50)
    h2.GetXaxis().SetTitle("FEB")
    h2.GetYaxis().SetTitle("N")

    for subRUN in range(0, subrun_max):
        if subRUN in l_good:
            for FEB in range(0, 44):
                binN = h1.GetBin(subRUN+1, FEB+1)
                N = h1.GetBinContent(binN)
                if N == 0:
                    if (RUN < 376 or FEB != 34):
                        h2.Fill(FEB)
                        print("{}\t{}".format(subRUN, FEB))
                        f.write("{}\t{}\n".format(subRUN, FEB))
                        if full_analysis and RUN != 368:
                            ht2.Fill(FEB)

    c1.Update()
    c1.SaveAs("{}/Hits_vs_FEB.pdf".format(pdf_dir))
    c1.SaveAs("{}/Hits_vs_FEB.png".format(png_dir))
    c1.SaveAs("{}/Hits_vs_FEB.root".format(root_dir))
    h1.Delete()
    c1.Close()

    c2 = ROOT.TCanvas("c2", "c2", 100, 100, 1600, 1000)
    h2.Draw()

    c2.Update()
    c2.SaveAs("{}/noHits_FEB.pdf".format(pdf_dir))
    c2.SaveAs("{}/noHits_FEB.png".format(png_dir))
    c2.SaveAs("{}/noHits_FEB.root".format(root_dir))
    h2.Delete()
    c2.Close()



    #################################################################################
    ## 5. Hits per subrun per GEMROC

    f.write("\n\nGEMROCs with no hits\n")
    f.write("\nGEMROC\tFEB\n")
    print("\n\nGEMROCs with no hits\n")
    print("GEMROC\tFEB\n")

    condition = "(delta_coarse==25 || delta_coarse==26)"
    h1 = ROOT.TH2D("h1", condition, subrun_max, 0, subrun_max, 15, 0, 15)
    h1.GetXaxis().SetTitle("subRunNo")
    h1.GetYaxis().SetTitle("GEMROC")
    c1 = ROOT.TCanvas("c11", "c11", 100, 100, 1600, 1000)
    chain.Draw("gemroc:subRunNo>>h1", condition, "colz")

    h2 = ROOT.TH1D("h2", "No hits (GEMROC)", 15, 0, 15)
    h2.GetXaxis().SetTitle("GEMROC")
    h2.GetYaxis().SetTitle("N")
    
    for subRUN in range(0, subrun_max):
        if subRUN in l_good:
            for ROC in range(0, 11):
                binN = h1.GetBin(subRUN+1, ROC+1)
                N = h1.GetBinContent(binN)
                if N == 0:
                    h2.Fill(ROC)
                    print("{}\t{}".format(subRUN, ROC))
                    f.write("{}\t{}\n".format(subRUN, ROC))
                    if full_analysis and RUN != 368:
                        ht3.Fill(ROC)

    c1.Update()
    c1.SaveAs("{}/Hits_vs_GEMROC.pdf".format(pdf_dir))
    c1.SaveAs("{}/Hits_vs_GEMROC.png".format(png_dir))
    c1.SaveAs("{}/Hits_vs_GEMROC.root".format(root_dir))
    h1.Delete()
    c1.Close()

    c2 = ROOT.TCanvas("c2", "c2", 100, 100, 1600, 1000)
    h2.Draw()

    c2.Update()
    c2.SaveAs("{}/noHits_GEMROC.pdf".format(pdf_dir))
    c2.SaveAs("{}/noHits_GEMROC.png".format(png_dir))
    c2.SaveAs("{}/noHits_GEMROC.root".format(root_dir))
    h2.Delete()
    c2.Close()


    BAD_SUBRUNs_low_dec.sort()
    BAD_SUBRUNs_low.sort()
    BAD_SUBRUNs_holes_dec.sort()
    BAD_SUBRUNs_holes.sort()


    print( "\n\nBAD SUBRUNs (low hits) from Decode: {}".format(BAD_SUBRUNs_low_dec) )
    print( "BAD SUBRUNs (low events) from Event: {}".format(BAD_SUBRUNs_low) )
    f.write( "\n\nBAD SUBRUNs (low hits) from Decode: {}\n\n".format(BAD_SUBRUNs_low_dec) )
    f.write( "BAD SUBRUNs (low events) from Event: {}".format(BAD_SUBRUNs_low) )

    print( "\n\nBAD SUBRUNs (holes) from Decode: {}".format(BAD_SUBRUNs_holes_dec) )
    print( "BAD SUBRUNs (holes) from Event: {}".format(BAD_SUBRUNs_holes) )
    f.write( "\n\nBAD SUBRUNs (holes) from Decode: {}\n\n".format(BAD_SUBRUNs_holes_dec) )
    f.write( "BAD SUBRUNs (holes) from Event: {}".format(BAD_SUBRUNs_holes) )



    print("\nDone\n\n")
    #f.write("\nDone\n\n")



    f.close()





########################################################################
##  ALL RUN TOGETHER

if full_analysis:

    path = "{}/data_quality".format(home_folder)

    ct1 = ROOT.TCanvas("ct1", "ct1", 100, 100, 1600, 1000)
    ht1.Draw()
    ct1.Update()
    ct1.SaveAs("{}/noHits_TIGER_allRUNs.pdf".format(path))
    ct1.SaveAs("{}/noHits_TIGER_allRUNs.png".format(path))
    ct1.SaveAs("{}/noHits_TIGER_allRUNs.root".format(path))
    ht1.Delete()
    ct1.Close()

    ct2 = ROOT.TCanvas("ct2", "ct2", 100, 100, 1600, 1000)
    ht2.Draw()
    ct2.Update()
    ct2.SaveAs("{}/noHits_FEB_allRUNs.pdf".format(path))
    ct2.SaveAs("{}/noHits_FEB_allRUNs.png".format(path))
    ct2.SaveAs("{}/noHits_FEB_allRUNs.root".format(path))
    ht2.Delete()
    ct2.Close()

    ct3 = ROOT.TCanvas("ct3", "ct3", 100, 100, 1600, 1000)
    ht3.Draw()
    ct3.Update()
    ct3.SaveAs("{}/noHits_GEMROC_allRUNs.pdf".format(path))
    ct3.SaveAs("{}/noHits_GEMROC_allRUNs.png".format(path))
    ct3.SaveAs("{}/noHits_GEMROC_allRUNs.root".format(path))
    ht3.Delete()
    ct3.Close()





