


import universal
import fileio.outputprinter
import fileio.loadconfig
import variablemanipulation.configmanipulation
import fileio.outputprinter
import fileio.loadconfig
import variablemanipulation.configmanipulation


universal.allocatevariables()

configfilename = "/usr/people/isp/workspace/samplerer/defaults.config"
simulationtype = "umbsamp"
simulationrootdirectory = "/data/isp03/cm/test"


#---Get configuration data
defaults = fileio.loadconfig.wrapper_loadconfigfile( configfilename)  # Load configuration file
localconfig = fileio.loadconfig.wrapper_loadconfigfile(simulationrootdirectory + "/" + defaults['main']['simulationconfigfilename']["value"])
config = variablemanipulation.configmanipulation.evaluateinorder( defaults, localconfig)
config = variablemanipulation.configmanipulation.evaluate_configinherit(config)

import random
random.seed()

if simulationtype in "umbsamp":
    import simulationvariablecreator.common
    import simulationvariablecreator.umbsamp

    config["generatedvars"]["rxncoor"] = simulationvariablecreator.common.readrxncoor(simulationrootdirectory + "/" + config['umbsamp']['rxncoordefinitionfilepath']["value"])


    simulationvariablecreator.umbsamp.checkforpreqs(config)
    productionfiles=simulationvariablecreator.umbsamp.generatesteps(config)
    filewriteconfig=simulationvariablecreator.umbsamp.processproduceforoutput(productionfiles,config)

    import fileio.writecharmm
    filetasks=fileio.writecharmm.interpretcharmmtemplate(config["umbsamp"]["templatefilepath"]["value"])




import fileio.writecharmm
fileio.writecharmm.execute(filewriteconfig,filetasks)





universal.allocatevariables()

configfilename = "/usr/people/isp/workspace/samplerer/defaults.config"
simulationtype = "umbsamp"
simulationrootdirectory = "/data/isp03/cm/test"


#---Get configuration data
defaults = fileio.loadconfig.wrapper_loadconfigfile( configfilename)  # Load configuration file
localconfig = fileio.loadconfig.wrapper_loadconfigfile(simulationrootdirectory + "/" + defaults['main']['simulationconfigfilename']["value"])
config = variablemanipulation.configmanipulation.evaluateinorder( defaults, localconfig)
config = variablemanipulation.configmanipulation.evaluate_configinherit(config)

import random
random.seed()

if simulationtype in "umbsamp":
    import simulationvariablecreator.common
    import simulationvariablecreator.umbsamp

    config["generatedvars"]["rxncoor"] = simulationvariablecreator.common.readrxncoor(simulationrootdirectory + "/" + config['umbsamp']['rxncoordefinitionfilepath']["value"])


    simulationvariablecreator.umbsamp.checkforpreqs(config)
    productionfiles=simulationvariablecreator.umbsamp.generatesteps(config)
    filewriteconfig=simulationvariablecreator.umbsamp.processproduceforoutput(productionfiles,config)

    import fileio.writecharmm
    filetasks=fileio.writecharmm.interpretcharmmtemplate(config["umbsamp"]["templatefilepath"]["value"])




import fileio.writecharmm
fileio.writecharmm.execute(filewriteconfig,filetasks)


