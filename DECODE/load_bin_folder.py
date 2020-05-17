import sys
import GEM_OFFLINE_classes
#path=raw_input("Insert path:")
#path="RUN_320"
#path="RUN_338"
#path="RUN_333"
#path="RUN_380"

######################################################################
######################################################################

data_path = "/dati/Data_CGEM_IHEP_Integration_2019/raw_dat/"

try:
    run = "RUN_{}".format(sys.argv[1])
except:
    run = "RUN_375"


path = data_path + run

GEM5=GEM_OFFLINE_classes.reader(0)

GEM5.write_txt_TM_folder(path)
GEM5.write_txt_TL_folder(path)


command=(raw_input("Press enter to exit"))
print "FINE"
