



def checkforpreqs(config):
    import numpy
    import fileio.outputprinter
    import variablemanipulation.existquery
    crxncoor=config['generatedvars']['rxncoor']

    doexit=0

    if variablemanipulation.existquery.existheaderandkey('umbsamp_setup','centers',config)==0:
        fileio.outputprinter.postinfo("No umbrella sampling centers specified.  Specify \"range=\" under ""[umbsamp-setup]""",1,4)
        doexit=1
    if variablemanipulation.existquery.existheaderandkey('umbsamp_setup','kval',config)==0:
        fileio.outputprinter.postinfo("No umbrella sampling force constants specified.  Specify \"kval=\" under ""[umbsamp-setup]""",1,4)
        doexit=1

    if doexit==1:
        fileio.outputprinter.postinfo("Exiting",1,4)
        return


def generatesteps(config):
    import fileio.outputprinter

    dimnames=config["generatedvars"]["rxncoor"]["names"]
    ndim=len(dimnames)



    reactioncenter_toparse=config["umbsamp_setup"]["centers"]["value"]
    forcevals_toparse=config["umbsamp_setup"]["kval"]["value"]

    import variablemanipulation.numberoperations
    reactioncenter = variablemanipulation.numberoperations.interpretmatrixstring(reactioncenter_toparse)
    forcevals = variablemanipulation.numberoperations.interpretmatrixstring(forcevals_toparse)


    producefiles=dict()
    producefiles["SamplingCenters"]=list()
    producefiles["HarmonicPotential"]=list()
    producefiles["ReactionCoordinateString"]=list()

    fileio.outputprinter.postinfo("Converting umbrella sampling centers into a square grid",3,4)
    for stepg in range(len(reactioncenter)):
        ccentcomb=variablemanipulation.numberoperations.getallcombinations(reactioncenter[stepg])
        producefiles["SamplingCenters"] = producefiles["SamplingCenters"] +ccentcomb

        cforcecomb=variablemanipulation.numberoperations.getallcombinations(forcevals[stepg])
        if len(cforcecomb) != len(ccentcomb):
            if len(cforcecomb) == 1:
                cforcecomb = cforcecomb * len(ccentcomb)


        if len(cforcecomb) != len(ccentcomb):
            fileio.outputprinter.postinfo("For group " + str(stepg+1) +", the length of centers ("+str(len(ccentcomb))+") does not match length of kvals (" + str(len(cforcecomb))+")",0,4)

        producefiles["HarmonicPotential"] = producefiles["HarmonicPotential"] + cforcecomb




    producefiles["SimulationNumber"]=list()

    import variablemanipulation.numberoperations

    samplingstartposition_temp=variablemanipulation.numberoperations.interpretmatrixstring(config["umbsamp_setup"]["startingcentervalue"]["value"])[0]
    samplingstartposition=list()
    for vals in samplingstartposition_temp:
        samplingstartposition=samplingstartposition+vals



    producefiles["EquilSteps"]=list()

    for stepg in range(len(producefiles["SamplingCenters"])):

        producefiles["SimulationNumber"]=producefiles["SimulationNumber"]+[[stepg]]
        producefiles["ReactionCoordinateString"].append(config["generatedvars"]["rxncoor"])
        producefiles["EquilSteps"].append(variablemanipulation.numberoperations.producespacedvectors(samplingstartposition,producefiles["SamplingCenters"][stepg],float(config["umbsamp_ratchetdynamics"]["ratchetinggradient"]["value"])))

    import simulationvariablecreator.common

    producefiles["FolderName"]=simulationvariablecreator.common.createfoldername("n",producefiles["SimulationNumber"],"c",producefiles["SamplingCenters"],"k",producefiles["HarmonicPotential"])

    stradd=config["umbsamp"]["simulationdirectoryname"]["value"] + "/"

    producefiles["FolderName"]=[stradd + cdir + "/"  for cdir in producefiles["FolderName"] ]



    producefiles["ReactionCoordinateNames"]=config["generatedvars"]["rxncoor"]["names"]


    return producefiles



def processproduceforoutput(producefiles,config):
    import variablemanipulation.configmanipulation


    configwrite=list()
    for stepindex in range(len(producefiles["FolderName"])):
        tempconfig=dict()
        tempconfig["main"]=dict()
        tempconfig["main"]["simulationdirectory"]=dict()
        tempconfig["umbsamp_setup"]=dict()
        tempconfig["umbsamp_ratchetdynamics"]=dict()
        tempconfig["umbsamp_ratchetdynamics"]["equilrxncoorsteps"]=dict()
        tempconfig["umbsamp_setup"]["simulationcenter"]=dict()
        tempconfig["umbsamp_setup"]["forceconstant"]=dict()
        tempconfig["umbsamp_setup"]["reactioncoornames"]=dict()
        tempconfig["umbsamp_setup"]["rxncoorstring"]=dict()

        tempconfig["umbsamp_ratchetdynamics"]["equilrxncoorsteps"]["value"]= producefiles["EquilSteps"][stepindex]
        tempconfig["umbsamp_setup"]["simulationcenter"]["value"]=producefiles["SamplingCenters"][stepindex]
        tempconfig["umbsamp_setup"]["forceconstant"]["value"]=producefiles["HarmonicPotential"][stepindex]
        tempconfig["umbsamp_setup"]["reactioncoornames"]["value"]=producefiles["ReactionCoordinateNames"]
        tempconfig["main"]["simulationdirectory"]["value"]=producefiles["FolderName"][stepindex]
        tempconfig["umbsamp_setup"]["rxncoorstring"]["value"]=producefiles["ReactionCoordinateString"][stepindex]

        newconfig=variablemanipulation.configmanipulation.evaluateinorder(config, tempconfig)
        writeconfig=newconfig
        configwrite.append(writeconfig)

    return configwrite






