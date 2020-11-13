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
    print("ERROR: OS {} not compatible".format(OS))
    sys.exit()


code_path = os.environ["QAQC_code"]
out_path = os.environ["QAQC_out"]
data_path = os.environ["data"]
show_path = os.environ["QAQC_show"]

#print("QAQC code path: {}".format(code_path))
#print("QAQC output path: {}".format(out_path))
#print("QAQC show path: {}".format(show_path))
#print("Data path: {}".format(data_path))

Data_path = "{}/raw_root".format(data_path)

local_path = "/home/Fabio/analysis/Data-analysis/OUT_folder"
if not(os.path.isdir(local_path)):
    os.mkdir(local_path)

code_dir = "{}/Fabio".format(code_path)


#home_folder = os.getcwd()
#path = "{}/data_quality".format(home_folder)
#if not(os.path.isdir(path)):
#    os.mkdir(path)


try:
    if len(sys.argv)==3 and sys.argv[1] == "full":
        run = [int(sys.argv[2])]
        os.system( "python3 {}/check_data.py {}".format(code_dir, run[0]) )
        os.system( "python3 {}/check_pkt.py {}".format(code_dir, run[0]) )
    elif len(sys.argv)==2 and sys.argv[1] == "full":
        os.system( "python3 {}/check_data.py all".format(code_dir) )
        os.system( "python3 {}/check_pkt.py all".format(code_dir) )
        run = [351, 368, 370, 372, 375, 355, 376, 377, 378, 387, 380, 383, 384, 385, 395, 396, 397, 400]
    elif sys.argv[1] == "all":
        run = [351, 368, 370, 372, 375, 355, 376, 377, 378, 387, 380, 383, 384, 385, 395, 396, 397, 400]
    else:
        run = [int(sys.argv[1])]
except:
    run = [368]


for RUN in run:

    print("\n\n\nAnalyzing RUN {}\n\n".format(RUN))
    
    path = "{}/{}".format(local_path, RUN)
    if not(os.path.isdir(path)):
        os.mkdir(path)

    run_path = "{}/{}".format(out_path, RUN)
    if not(os.path.isdir(run_path)):
        os.mkdir(run_path)

    link_path = "{}/decode_check".format(run_path)
    if not(os.path.isdir(link_path)):
        os.system( "ln -s {} {}".format(path, link_path)  )


    """
    root_dir = "{}/root".format(path)
    if not( os.path.isdir( root_dir ) ):
        os.mkdir(root_dir)
    pdf_dir = "{}/pdf".format(path)
    if not( os.path.isdir( pdf_dir ) ):
        os.mkdir(pdf_dir)
    png_dir = "{}/png".format(path)
    if not( os.path.isdir( png_dir ) ):
        os.mkdir(png_dir)
    """

    log_dir = "{}/log".format(path)
    if not( os.path.isdir( log_dir ) ):
        os.mkdir(log_dir)

    show_dir = "{}/{}".format(show_path, RUN)
    if not(os.path.isdir(show_dir)):
        os.mkdir(show_dir)


    f2 = open("{}/RUN_{}_summary.txt".format(log_dir, RUN), "w")
    
    f3 = open("{}/decode_log.txt".format(show_dir), "w")


    #############################################################################################
    #############################################################################################


    with open("{}/RUN_{}_data_log.txt".format(log_dir, RUN), "r") as f:

        for line in f.readlines():
            if "subRunNo MAX" in line:
                n_tot = int(line.split(" = ")[-1]) + 1

            if "GOOD SUBRUNs" in line:
                l_start = line.split("=")[-1].split("[")[-1].split("]")[0].split(", ")
                #print l_start
                #print type(l_start)
                l_start = [int(x) for x in l_start]
                #print ("SUBRUNs with high ENTRIES = {}\n".format(l_start))
                #f2.write("SUBRUNs with high ENTRIES = {}\n\n".format(l_start))
        
            if "BAD SUBRUNs (low hits) from Decode" in line:

                l_toCut3 = line.split("[")[-1].split("]")[0].split(", ")
                try:
                    l_toCut3 = [int(x) for x in l_toCut3]
                    print ("SUBRUNs to be CUT due to low hits = {}\n".format(l_toCut3))
                    f2.write("SUBRUNs to be CUT due to low hits = {}\n\n".format(l_toCut3))
                except:
                    print("No SUBRUNs to be cut due to holes: {}\n".format(l_toCut3))
                    f2.write("No SUBRUNs to be cut due to holes: {}\n\n".format(l_toCut3))
                    l_toCut3 = list()

                n_hits = len(l_toCut3)

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

                n_holes = len(l_toCut)

    l_good = [x for x in l_start if x not in l_toCut]
    #print ("SUBRUNs GOOD (# hits and holes) = {}\n".format(l_good))


    #############################################################################################
    #############################################################################################


    with open("{}/RUN_{}_pkt_log.txt".format(log_dir, RUN), "r") as f:

        for line in f.readlines():
            
            if "TOTAL ENTRIES" in line:
                f3.write("{}".format(line))
            if "GOOD ENTRIES" in line:
                f3.write("{}".format(line))
            if "BAD ENTRIES" in line:
                f3.write("{}\n".format(line))
            if "l1ts_min_tcoarse errors from TIGER" in line:
                f3.write("{}".format(line))

            if "BAD SUBRUNs from Decode" in line:
                l_toCut2 = line.split("[")[-1].split("]")[0].split(", ")
                print(l_toCut2)
                #print type(l_toCut2)
                try:
                    l_toCut2 = [int(x) for x in l_toCut2]
                    print ("SUBRUNs to be CUT due to packets shift = {}\n".format(l_toCut2))
                    f2.write("SUBRUNs to be CUT due to packets shift = {}\n\n".format(l_toCut2))
                except:
                    print("No SUBRUNs to be cut due to pakets shift: {}\n".format(l_toCut2))
                    f2.write("No SUBRUNs to be cut due to pakets shift: {}\n\n".format(l_toCut2))
                    l_toCut2 = list()

                n_pkt = len(l_toCut2)

    l_good2 = [x for x in l_good if x not in l_toCut2]
    l_good2.sort()
    print ("SUBRUNs GOOD (decode) = {}\n".format(l_good2))
    f2.write("SUBRUNs GOOD (decode) = {}\n\n".format(l_good2))

    n_good = len(l_good2)

    f3.write("\n\nNumber of subRUNs: {}\n".format(n_tot))
    f3.write("\nGood subRUNs: {} ({:.2f}%)\n".format(n_good, n_good/n_tot*100))
    f3.write("Bad subRUNs due to low hits: {} ({:.2f}%)\n".format(n_hits, n_hits/n_tot*100))
    f3.write("Bad subRUNs due to holes: {} ({:.2f}%)\n".format(n_holes, n_holes/n_tot*100))
    f3.write("Bad subRUNs due to packets shift: {} ({:.2f}%)\n".format(n_pkt, n_pkt/n_tot*100))


    #############################################################################################
    #############################################################################################

    data_path = "{}/{}".format(Data_path, RUN)

    sub_run_good = list()
    for file in glob.glob("{}/Sub_RUN_event*".format(data_path)):
        sub_run_good.append( int( file.split("/")[-1].split("_")[-1].split(".")[0] ) )
    sub_run_good.sort()
    print ("SUBRUNs GOOD (event)  = {} ({:.2f}%)\n".format(sub_run_good, len(sub_run_good)/n_tot*100))
    f2.write("SUBRUNs GOOD (event)  = {} ({:.2f}%)\n\n".format(sub_run_good, len(sub_run_good)/n_tot*100) )


    # 1
    sub_run_lowEvents = list()
    for file in glob.glob("{}/badSubRUN/lowevent/Sub_RUN_event*".format(data_path)):
        sub_run_lowEvents.append( int( file.split("/")[-1].split("_")[-1].split(".")[0] ) )
    sub_run_lowEvents.sort()
    print ("SUBRUNs LOW EVENTS (event)  = {} ({:.2f}%)\n".format(sub_run_lowEvents, len(sub_run_lowEvents)/n_tot*100) )
    f2.write("SUBRUNs LOW EVENTS (event)  = {} ({:.2f}%)\n\n".format(sub_run_lowEvents, len(sub_run_lowEvents)/n_tot*100))

    # 2
    sub_run_holes = list()
    for file in glob.glob("{}/badSubRUN/nofireFEB/Sub_RUN_event*".format(data_path)):
        sub_run_holes.append( int( file.split("/")[-1].split("_")[-1].split(".")[0] ) )
    sub_run_holes.sort()
    print ("SUBRUNs HOLES (event)  = {} ({:.2f}%)\n".format(sub_run_holes, len(sub_run_holes)/n_tot*100) )
    f2.write("SUBRUNs HOLES (event)  = {} ({:.2f}%)\n\n".format(sub_run_holes, len(sub_run_holes)/n_tot*100) )

    # 3
    sub_run_l1ts = list()
    for file in glob.glob("{}/badSubRUN/tool1ts/Sub_RUN_event*".format(data_path)):
        sub_run_l1ts.append( int( file.split("/")[-1].split("_")[-1].split(".")[0] ) )
    sub_run_l1ts.sort()
    print ("SUBRUNs L1TS (event)  = {} ({:.2f}%)\n".format(sub_run_l1ts, len(sub_run_l1ts)/n_tot*100 ))
    f2.write("SUBRUNs L1TS (event)  = {} ({:.2f}%)\n\n".format(sub_run_l1ts, len(sub_run_l1ts)/n_tot*100) )



    #############################################################################################
    #############################################################################################


    l_dif = [i for i in l_good2 + sub_run_good if i not in l_good2 or i not in sub_run_good]
    print( "\n\nDifference between GOOD subRUNs for Decode and Event: {} ({:.2f}%)".format(l_dif, len(l_dif)/n_tot*100) )
    f2.write( "\n\nDifference between GOOD subRUNs for Decode and Event: {} ({:.2f}%)".format(l_dif, len(l_dif)/n_tot*100) )
    f3.write( "\nDifference between GOOD subRUNs for Decode and Event: {} ({:.2f}%)".format(l_dif, len(l_dif)/n_tot*100) )

    l_dif1 = [i for i in l_good2 if i not in sub_run_good]
    print( "\n\nGOOD subRUNs present in Decode but not in Event: {}".format(l_dif1) )
    f2.write( "\n\nGOOD subRUNs present in Decode but not in Event: {}\n".format(l_dif1) )

    for sr in l_dif1:
        if sr in sub_run_l1ts:
            print( "{} --> L1TS".format(sr) )
            f2.write( "{} --> L1TS\n".format(sr) )
        if sr in sub_run_lowEvents:
            print( "{} --> LOW_EVENTS".format(sr) )
            f2.write( "{} --> LOW_EVENTS\n".format(sr) )
        if sr in sub_run_holes:
            print( "{} --> HOLES".format(sr) )
            f2.write( "{} --> HOLES\n".format(sr) )
        if sr not in sub_run_l1ts and sr not in sub_run_lowEvents and sr not in sub_run_holes:
            print( "Error: cut for subRUN {} not found".format(sr) )
            f2.write( "Error: cut for subRUN {} not found\n".format(sr) )

    l_dif2 = [i for i in sub_run_good if i not in l_good2]
    print( "\n\nGOOD subRUNs present in Event but not in Decode: {}".format(l_dif2) )
    f2.write( "\n\nGOOD subRUNs present in Event but not in Decode: {}\n".format(l_dif2) )

    for sr in l_dif2:
        if sr in l_toCut2:
            print( "{} --> packets_shift".format(sr) )
            f2.write( "{} --> packets_shift\n".format(sr) )
        if sr in l_toCut3:
            print( "{} --> LOW_HITS".format(sr) )
            f2.write( "{} --> LOW_HITS\n".format(sr) )
        if sr in l_toCut:
            print( "{} --> HOLES".format(sr) )
            f2.write( "{} --> HOLES\n".format(sr) )
        if sr not in l_toCut and sr not in l_toCut2 and sr not in l_toCut3:
            print( "Error: cut for subRUN {} not found".format(sr) )
            f2.write( "Error: cut for subRUN {} not found\n".format(sr) )


    f2.close()

    f3.close()

    os.system( "cp {}/RUN_{}_summary.txt {}/decode_summary.txt".format(log_dir, RUN, show_dir) )

    print("\n\n")
