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



home_folder = "/home/Fabio/analysis/Data-analysis"


try:
    if sys.argv[1] == "full":
        os.system("python check_data.py all")
        os.system("python check_pkt.py all")
        run = [351, 368, 370, 372, 375, 355, 376, 377, 378, 387, 380, 383, 384, 385]
    elif sys.argv[1] == "all":
        run = [351, 368, 370, 372, 375, 355, 376, 377, 378, 387, 380, 383, 384, 385]
    else:
        run = [int(sys.argv[1])]
except:
    run = [368]


for RUN in run:

    print("\n\n\nAnalyzing RUN {}\n\n".format(RUN))
   
    f2 = open("{}/CHECK_DATA/{}/RUN_{}_summary.txt".format(home_folder, RUN, RUN), "w")
    f = open("{}/CHECK_DATA/{}/RUN_{}_log.txt".format(home_folder, RUN, RUN), "r")

    for line in f.readlines():
        if "GOOD SUBRUNs" in line:
            l_start = line.split("=")[-1].split("[")[-1].split("]")[0].split(", ")
            #print l_start
            #print type(l_start)
            l_start = [int(x) for x in l_start]
            print ("SUBRUNs with high ENTRIES = {}\n".format(l_start))
            f2.write("SUBRUNs with high ENTRIES = {}\n\n".format(l_start))
        
        if "BAD SUBRUNs (holes) from Decode" in line:
            l_toCut = line.split("[")[-1].split("]")[0].split(", ")
            #print l_toCut
            #print type(l_toCut)
            try:
                l_toCut = [int(x) for x in l_toCut]
                print ("SUBRUNs to be CUT due to holes = {}\n".format(l_toCut))
                f2.write("SUBRUNs to be CUT due to holes = {}\n\n".format(l_toCut))
            except:
                print("No SUBRUNs to be cut due to holes: {}\n".format(l_toCut))
                f2.write("No SUBRUNs to be cut due to holes: {}\n\n".format(l_toCut))
                l_toCut = list()
    f.close()

    l_good = [x for x in l_start if x not in l_toCut]
    print ("SUBRUNs GOOD (# hits and holes) = {}\n".format(l_good))


    f = open("{}/CHECK_PACKETS/{}/RUN_{}_log.txt".format(home_folder, RUN, RUN), "r")

    for line in f.readlines():
        if "BAD SUBRUNs from Decode" in line:
            l_toCut2 = line.split("[")[-1].split("]")[0].split(", ")
            #print l_toCut2
            #print type(l_toCut2)
            try:
                l_toCut2 = [int(x) for x in l_toCut2]
                print ("SUBRUNs to be CUT due to packets shift = {}\n".format(l_toCut2))
                f2.write("SUBRUNs to be CUT due to packets shift = {}\n\n".format(l_toCut2))
            except:
                print("No SUBRUNs to be cut due to pakets shift: {}\n".format(l_toCut2))
                f2.write("No SUBRUNs to be cut due to pakets shift: {}\n\n".format(l_toCut2))
                l_toCut2 = list()
    f.close()

    l_good2 = [x for x in l_good if x not in l_toCut2]
    l_good2.sort()
    print ("SUBRUNs GOOD (decode) = {}\n".format(l_good2))
    f2.write("SUBRUNs GOOD (decode) = {}\n\n".format(l_good2))


    sub_run_good = list()
    for file in glob.glob("/dati/Data_CGEM_IHEP_Integration_2019/raw_root/{}/Sub_RUN_event*".format(RUN)):
        sub_run_good.append( int( file.split("/")[-1].split("_")[-1].split(".")[0] ) )
    sub_run_good.sort()
    print ("SUBRUNs GOOD (event)  = {}\n".format(sub_run_good))
    f2.write("SUBRUNs GOOD (event)  = {}\n\n".format(sub_run_good))




    sub_run_holes = list()
    for file in glob.glob("/dati/Data_CGEM_IHEP_Integration_2019/raw_root/{}/badSubRUN/nofireFEB/Sub_RUN_event*".format(RUN)):
        sub_run_holes.append( int( file.split("/")[-1].split("_")[-1].split(".")[0] ) )
    sub_run_holes.sort()
    print ("SUBRUNs HOLES (event)  = {}\n".format(sub_run_holes))
    f2.write("SUBRUNs HOLES (event)  = {}\n\n".format(sub_run_holes))



    sub_run_lowEvents = list()
    for file in glob.glob("/dati/Data_CGEM_IHEP_Integration_2019/raw_root/{}/badSubRUN/lowevent/Sub_RUN_event*".format(RUN)):
        sub_run_lowEvents.append( int( file.split("/")[-1].split("_")[-1].split(".")[0] ) )
    sub_run_lowEvents.sort()
    print ("SUBRUNs LOW EVENTS (event)  = {}\n".format(sub_run_lowEvents))
    f2.write("SUBRUNs LOW EVENTS (event)  = {}\n\n".format(sub_run_lowEvents))



    sub_run_l1ts = list()
    for file in glob.glob("/dati/Data_CGEM_IHEP_Integration_2019/raw_root/{}/badSubRUN/tool1ts/Sub_RUN_event*".format(RUN)):
        sub_run_l1ts.append( int( file.split("/")[-1].split("_")[-1].split(".")[0] ) )
    sub_run_l1ts.sort()
    print ("SUBRUNs L1TS (event)  = {}\n".format(sub_run_l1ts))
    f2.write("SUBRUNs L1TS (event)  = {}\n\n".format(sub_run_l1ts))




    l_dif = [i for i in l_good2 + sub_run_good if i not in l_good2 or i not in sub_run_good]
    print( "Difference between GOOD RUNS for Decode and Event: {}\n\n".format(l_dif) )
    f2.write( "Difference between GOOD RUNS for Decode and Event: {}\n\n".format(l_dif) )

    l_dif1 = [i for i in l_good2 if i not in sub_run_good]
    print( "GOOD RUNS present in Decode but not in Event: {}\n\n".format(l_dif1) )
    f2.write( "GOOD RUNS present in Decode but not in Event: {}\n\n".format(l_dif1) )

    l_dif2 = [i for i in sub_run_good if i not in l_good2]
    print( "GOOD RUNS present in Event but not in Decode: {}\n\n".format(l_dif2) )
    f2.write( "GOOD RUNS present in Event but not in Decode: {}\n\n".format(l_dif2) )


    f2.close()
