
def topology(config):

    stringout = "read rtf card name \""+config["topologypath"]["value"] + "\"   !Read topology"
    return stringout


def parameter(config):
    stringout = "read param card name \""+config["parameterpath"]["value"] + "\"   !Read parameter file"
    return stringout


def psfload(config):
    stringout = "read psf card name \""+config["psfname"]["value"] + "\"   !Read PSF file"
    return stringout

def readcoor(config):
    stringout = "read coor card name \""+config["crdname"]["value"] + "\"   !Read Coordinates from CRD file"
    return stringout

def writecoor(config):
    stringout = "write coor card name \""+config["crdwritename"]["value"] + "\"   !Read Coordinates from CRD file"
    return stringout

def quantum(config):
    if config["quantumtype"]["value"] == "None":
        stringout="! No quantum region specified"

    return stringout



def crystal(config):
    if config["crystaltype"]["value"] == "None":
        stringout="! No crystal specified"

    return stringout


def rxncoor(config):
    rxncoorstring=config["rxncoorstring"]["value"]["text"]
    strwrite="! Write out reaction coordinate {\n"
    for lines in rxncoorstring:
        strwrite=strwrite+lines+"\n"

    strwrite=strwrite+"!  } Finish writing reaction coordinate \n"

    return strwrite


def randomseed(config):
    import random

    randnum=random.randint(100000,999999)
    strwrite="rand iseed "+str(randnum)+ "    ! Random number generator seed"
    return strwrite

def dynamics(config):
    import stringmanipulation.formatting as smf

    stringdyna=""


    try:

        if config["parameter_iunrea"]["value"]!=-1:
            stringdyna=stringdyna+"open read unit "+str(config["parameter_iunrea"]["value"])+ " formatted name \""+config["formattedreadname_restart"]["value"] +"\"   !Open formatted file to read restart \n"
    except:
        pass

    try:

        if config["parameter_iunwri"]["value"]!=-1:
            stringdyna=stringdyna+"open write unit "+str(config["parameter_iunwri"]["value"])+ " formatted name \""+config["formattedwritename_restart"]["value"] +"\"   !Open formatted file to write restart \n"
    except:
        pass


    try:

        if config["parameter_iuncrd"]["value"]!=-1:
            stringdyna=stringdyna+"open write unit "+str(config["parameter_iuncrd"]["value"])+ " formatted name \""+config["binarywritename_positions"]["value"] +"\"   !Open unformatted file to write coordinates\n"
    except:
        pass

    try:

        if config["parameter_iunvel"]["value"]!=-1:
            stringdyna=stringdyna+"open write unit "+str(config["parameter_iunvel"]["value"])+ " formatted name \""+config["binarywritename_velocity"]["value"] +"\"   !Open unformatted file to write velocities\n"
    except:
        pass

    stringdyna=stringdyna+"dyna -    !Call dynamics \n"
    stringdyna=stringdyna+"    "+smf.genvaluecommentstring(config["header_startpoint"])+ "\n"
    stringdyna=stringdyna+"    "+smf.genvaluecommentstring(config["header_dynamicstype"])+ "\n"
    nkeys=0
    for keys in config:
        if "parameter_" in keys:
            nkeys+=1

    nkeysi=0
    for keys in config:
        if "parameter_" in keys:
            nkeysi+=1
            nextlinedelim="-"
            if nkeysi == nkeys:
                nextlinedelim=""
            stringdyna=stringdyna+"    "+keys[10:]+" "+str(config[keys]["value"])+" "+nextlinedelim+"   "+config[keys]["comment"]+"\n"

    return stringdyna

def ratchetdynamics(config):  #umbsamp_ratchetdynamics
    import copy,os
    import stringmanipulation.formatting

    ratchetingsteps=config["equilrxncoorsteps"]["value"]

    stringadd="! Write out serial micro-equilibrations { \n"
    isfirststep=1
    counter=0

    doorg=config["organizefiles"]["value"]
    if doorg:
        stringadd=stringadd+"syst \"mkdir restarts\" \n\n"
        addstr="restarts/"
    else:
        addstr=""


    for cstep in ratchetingsteps:
        passconfig=copy.deepcopy(config)

        passconfig["simulationcenter"]["value"]=cstep
        stringadd=stringadd+umbrellacenter(passconfig)
        stringadd=stringadd+"\n"

        if isfirststep==1:
            passconfig["header_startpoint"]["value"]="start"
            passconfig["parameter_iunwri"]["value"]=32
            passconfig["parameter_iunrea"]["value"]=-1
            passconfig['formattedwritename_restart']["value"]=addstr+os.path.splitext(config['formattedwritename_restart']["value"])[0]+stringmanipulation.formatting.autogennumstringfromlength(counter,len(ratchetingsteps))+".res"
        else:
            passconfig["header_startpoint"]["value"]="restart"
            passconfig["parameter_iunwri"]["value"]=32
            passconfig["parameter_iunrea"]["value"]=31
            passconfig['formattedreadname_restart']["value"]=addstr+os.path.splitext(config['formattedreadname_restart']["value"])[0]+stringmanipulation.formatting.autogennumstringfromlength(counter-1,len(ratchetingsteps))+".res"
            passconfig['formattedwritename_restart']["value"]=addstr+os.path.splitext(config['formattedwritename_restart']["value"])[0]+stringmanipulation.formatting.autogennumstringfromlength(counter,len(ratchetingsteps))+".res"
        counter+=1
        stringadd=stringadd+dynamics(passconfig)
        stringadd=stringadd+"\n"

        isfirststep=0
    stringadd=stringadd+" ! } Finished writing serial micro-equilibrations"
    return stringadd

def umbrellacenter(config):


    stringtopass=""
    for cidx in range(len(config["rxncoorstring"]["value"]["names"])):
        stringadd="rxncor: umbr name "+config["rxncoorstring"]["value"]["names"][cidx]
        stringadd=stringadd+ " kumb "+str(config["forceconstant"]["value"][cidx])
        stringadd=stringadd+ " del0 "+str(config["simulationcenter"]["value"][cidx])
        stringtopass=stringtopass+stringadd+"\n"

    return stringtopass


def umbrellatrace(config):
    stringtopass=""
    startunit=341
    for cidx in range(len(config["rxncoorstring"]["value"]["names"])):
        stringadd="rxncor: trace "+config["rxncoorstring"]["value"]["names"][cidx]
        stringadd=stringadd+ " unit "+str(startunit)+" freq 1"
        startunit+=1
        stringtopass=stringtopass+stringadd+"\n"

    stringadd="rxncor: stat - \n"
    for cidx in range(len(config["rxncoorstring"]["value"]["names"])):
        stringadd=stringadd+"name " +config["rxncoorstring"]["value"]["names"][cidx]
        stringadd=stringadd+ " lowdelta -1000 hidelta -999 deld 1 "

        if (cidx+1) != len((config["rxncoorstring"]["value"]["names"])):
            stringadd=stringadd+" - \n"
        else:
            stringadd=stringadd+" start 100000000"



    stringtopass=stringtopass+stringadd+"\n"

    return stringtopass
