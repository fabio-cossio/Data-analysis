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

home_folder = os.getcwd()
#home_folder = "/home/Fabio/analysis/Data-analysis"
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
        run = [351, 368, 370, 372, 375, 355, 376, 377, 378, 387, 380, 383, 384, 385, 395, 396, 397, 400]

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

    f = open("{}/RUN_{}_pkt_log.txt".format(path, RUN), "w")

    #################################################################################
    #################################################################################


    data_path = "{}{}".format(Data_path, RUN)


    BAD_SUBRUNs = list()
    for name in glob.glob("{}/badSubRUN/tool1ts/Sub_RUN_event*".format(data_path)):
        BAD_SUBRUNs.append( int( name.split("/")[-1].split("_")[-1].split(".")[0] ) )

    #print BAD_SUBRUNs


    BAD_SUBRUNs_dec = list()


    chain = ROOT.TChain("tree")
    chain.Add("{}/Sub_RUN_dec_*.root".format(data_path))


    #################################################################################
    #################################################################################


    print("\nRUN = {}".format(RUN))
    f.write("\nRUN = {}\n".format(RUN))


    subrun_max = 100000
    h1 = ROOT.TH1D("h1", "h1", subrun_max, 0, subrun_max)
    chain.Draw("subRunNo>>h1", "", "")
    bin = h1.FindLastBinAbove(0, 1)
    subrun_max = int(h1.GetXaxis().GetBinCenter(bin)) + 2
    print("subRunNo MAX = {}".format(subrun_max-2))
    f.write("subRunNo MAX = {}\n".format(subrun_max-2))
    h1.Delete()


    l1count_max = 100000
    h1 = ROOT.TH1D("h1", "h1", l1count_max, 0, l1count_max)
    chain.Draw("count>>h1", "", "")
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
    chain.Draw("count>>h1", condition, "")

    TOT1 = int(h1.GetEntries())
    print("TOTAL ENTRIES = {} ({} spurious removed, {:.2f}%)".format( TOT1, TOT-TOT1, (TOT-TOT1)/float(TOT)*100 ) )
    f.write("TOTAL ENTRIES = {} ({} spurious removed, {:.2f}%)\n".format( TOT1, TOT-TOT1, (TOT-TOT1)/float(TOT)*100 ) )

    c1.Update()
    c1.SaveAs("{}/count.pdf".format(pdf_dir))
    c1.SaveAs("{}/count.png".format(png_dir))
    c1.SaveAs("{}/count.root".format(root_dir))
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
    chain.Draw("count>>h1", condition, "")

    TOT2 = int(h1.GetEntries())
    print("GOOD ENTRIES = {} ({:.2f}%)".format( TOT2, TOT2/float(TOT1)*100 ) )
    f.write("GOOD ENTRIES = {} ({:.2f}%)\n".format( TOT2, TOT2/float(TOT1)*100 ) )

    c1.Update()
    c1.SaveAs("{}/good.pdf".format(pdf_dir))
    c1.SaveAs("{}/good.png".format(png_dir))
    c1.SaveAs("{}/good.root".format(root_dir))
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
    chain.Draw("gemroc:count>>h1", condition, "colz")

    bin_max = h1.ProjectionX().GetMaximumBin()
    print( "\nBIN MAX = {}".format(bin_max) )
    l1count_cut = h1.GetXaxis().GetBinCenter( bin_max ) + 15
    print( "Cut on L1 COUNT set to {}\n".format(l1count_cut) )
    f.write( "\nCut on L1 COUNT set to {}\n\n".format(l1count_cut) )
    
    line_cut = ROOT.TLine(l1count_cut, 0, l1count_cut, 15)
    line_cut.Draw()
    line_cut.SetLineStyle(7)
    line_cut.SetLineWidth(1)

    c1.Update()
    c1.SaveAs("{}/COUNTvsGEMROC.pdf".format(pdf_dir))
    c1.SaveAs("{}/COUNTvsGEMROC.png".format(png_dir))
    c1.SaveAs("{}/COUNTvsGEMROC.root".format(root_dir))
    h1.Delete()
    c1.Close()


    condition = "(delta_coarse==25 || delta_coarse==26) && (l1ts_min_tcoarse<1300 || l1ts_min_tcoarse>1566)"
    h1 = ROOT.TH2D("h1", condition, l1count_max, 0, l1count_max, subrun_max, 0, subrun_max)
    h1.GetXaxis().SetTitle("count")
    h1.GetYaxis().SetTitle("subRunNo")
    c1 = ROOT.TCanvas("c11", "c11", 100, 100, 1800, 1200)
    chain.Draw("subRunNo:count>>h1", condition, "colz")

    line_cut = ROOT.TLine(l1count_cut, 0, l1count_cut, subrun_max)
    line_cut.Draw()
    line_cut.SetLineStyle(7)
    line_cut.SetLineWidth(1)

    c1.Update()
    c1.SaveAs("{}/SUBRUNvsCOUNT.pdf".format(pdf_dir))
    c1.SaveAs("{}/SUBRUNvsCOUNT.png".format(png_dir))
    c1.SaveAs("{}/SUBRUNvsCOUNT.root".format(root_dir))
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
    
    line_cut.Draw()
    line_cut.SetLineStyle(7)
    line_cut.SetLineWidth(1)

    c1.Update()
    c1.SaveAs("{}/COUNTvsGEMROC_TIGER03.pdf".format(pdf_dir))
    c1.SaveAs("{}/COUNTvsGEMROC_TIGER03.png".format(png_dir))
    c1.SaveAs("{}/COUNTvsGEMROC_TIGER03.root".format(root_dir))
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

    line_cut.Draw()
    line_cut.SetLineStyle(7)
    line_cut.SetLineWidth(1)

    c1.Update()
    c1.SaveAs("{}/COUNTvsGEMROC_TIGER47.pdf".format(pdf_dir))
    c1.SaveAs("{}/COUNTvsGEMROC_TIGER47.png".format(png_dir))
    c1.SaveAs("{}/COUNTvsGEMROC_TIGER47.root".format(root_dir))
    h1.Delete()
    c1.Close()


    print("\n")
    f.write("\n")




    #################################################################################
    ## 5. GEMROC

    for roc in range(0, 11):
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

            line_cut = ROOT.TLine(l1count_cut, 0, l1count_cut, subrun_max)
            line_cut.Draw()
            line_cut.SetLineStyle(7)
            line_cut.SetLineWidth(1)

            c1.Update()
            c1.SaveAs("{}/GEMROC_{}.pdf".format(pdf_dir, roc))
            c1.SaveAs("{}/GEMROC_{}.png".format(png_dir, roc))
            c1.SaveAs("{}/GEMROC_{}.root".format(root_dir, roc))
            h1.Delete()
            c1.Close()

            condition = "(delta_coarse==25 || delta_coarse==26) && count>{} && gemroc=={}".format(l1count_cut, roc)
            h2 = ROOT.TH1D("h2", condition, subrun_max, 0, subrun_max)
            h2.GetXaxis().SetTitle("subRunNo")
            h2.GetYaxis().SetTitle("N")
            c2 = ROOT.TCanvas("c22", "c22", 100, 100, 1800, 1200)
            chain.Draw("subRunNo>>h2", condition, "")

            condition = "(delta_coarse==25 || delta_coarse==26) && (l1ts_min_tcoarse<1300 || l1ts_min_tcoarse>1566) && count>{} && gemroc=={}".format(l1count_cut, roc)
            h1 = ROOT.TH1D("h1", condition, subrun_max, 0, subrun_max)
            h1.GetXaxis().SetTitle("subRunNo")
            h1.GetYaxis().SetTitle("N")
            c1 = ROOT.TCanvas("c11", "c11", 100, 100, 1800, 1200)
            chain.Draw("subRunNo>>h1", condition, "")
            for subrun_bin in range(0, subrun_max):
                N = int(h1.GetBinContent(subrun_bin))
                D = int(h2.GetBinContent(subrun_bin))
                if D > 0:
                    bad_perc = N / float(D) * 100
                    if bad_perc > 2:
                        print( "BAD subRUN = {} ({}, {:.2f}%)".format(subrun_bin - 1, N, bad_perc) )
                        f.write( "BAD subRUN = {} ({}, {:.2f}%)\n".format(subrun_bin - 1, N, bad_perc) )
                    
                        if not(subrun_bin - 1 in BAD_SUBRUNs_dec):
                            BAD_SUBRUNs_dec.append(subrun_bin - 1)


            c1.Update()
            c1.SaveAs("{}/badSubRUN_GEMROC_{}.pdf".format(pdf_dir, roc))
            c1.SaveAs("{}/badSubRUN_GEMROC_{}.png".format(png_dir, roc))
            c1.SaveAs("{}/badSubRUN_GEMROC_{}.root".format(root_dir, roc))
            h1.Delete()
            c1.Close()

            h2.Delete()
            c2.Close()

    #################################################################################
    #################################################################################


    BAD_SUBRUNs_dec.sort()
    BAD_SUBRUNs.sort()

    print( "\n\nBAD SUBRUNs from Decode: {}".format(BAD_SUBRUNs_dec) )
    print( "BAD SUBRUNs from Event: {}".format(BAD_SUBRUNs) )
    f.write( "\n\nBAD SUBRUNs from Decode: {}\n\n".format(BAD_SUBRUNs_dec) )
    f.write( "BAD SUBRUNs from Event: {}".format(BAD_SUBRUNs) )


    print("\nDone\n\n")
    f.write("\nDone\n\n")

    f.close()


