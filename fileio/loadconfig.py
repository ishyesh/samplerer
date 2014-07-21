


def read_configfile(fname): #This reads an ini file
    import ConfigParser
    import fileio.outputprinter
    import fileio.fileiomanipulation


    fileio.outputprinter.postinfo("Trying to read config file: "+ fname,5,5)

    parser=ConfigParser.SafeConfigParser()
    fileproxy=fileio.fileiomanipulation.StripTabsAndBlanks(fname)
    parser.readfp(fileproxy)

    fileio.outputprinter.postinfo("Finishing reading config file: "+ fname,5,5)
    return parser

def convert_configfiletodictionary(parser): #This converts the ini file into a telescoping dictionary
    import fileio.outputprinter

    fileio.outputprinter.postinfo("Trying to convert config file input data to a dictionary",5,5)
    config=dict()
    for section in parser.sections():
        config[section]=dict()
        for option in parser.options(section):
            config[section][option]=parser.get(section,option)

    fileio.outputprinter.postinfo("Finished converting config file input data to a dictionary",5,5)

    return config

def convert_configdictionarytodata(config):
    import fileio.outputprinter

    fileio.outputprinter.postinfo("Trying to convert strings to value and comments in the config file",5,5)
    newdict=dict()
    for headers in config.keys():
        newdict[headers]=dict()
        for keys in config[headers].keys():
            newdict[headers][keys]=dict()
            cstr=config[headers][keys]
            idxcut=cstr.find("!")

            if idxcut==-1:
                newdict[headers][keys]["value"]=config[headers][keys].strip()
                newdict[headers][keys]["comment"]=""
            else:
                newdict[headers][keys]["value"]=config[headers][keys][0:idxcut].strip()
                newdict[headers][keys]["comment"]=config[headers][keys][idxcut:len(cstr)]

    fileio.outputprinter.postinfo("Finished converting strings to value and comments in the config file",5,5)
    return newdict


def evaluate_datavariables(data):
    import fileio.outputprinter


    fileio.outputprinter.postinfo("Trying to evaluate any operations in the config file",5,5)
    for headers in data.keys():
        for keys in data[headers].keys():
            if data[headers][keys]["value"][0]=="@":
                if data[headers][keys]["value"] in "@genrandomnumber" :
                    import variablemanipulation.numberoperations
                    data[headers][keys]["value"]=variablemanipulation.numberoperations.genrandomnumber()

    fileio.outputprinter.postinfo("Finished evaluating operations in the config file",5,5)

    return data

def wrapper_loadconfigfile(fname):

    parser=read_configfile(fname)
    config=convert_configfiletodictionary(parser)
    data=convert_configdictionarytodata(config)
    finaldata=evaluate_datavariables(data)

    return finaldata


