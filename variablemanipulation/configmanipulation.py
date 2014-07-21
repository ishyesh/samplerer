def evaluateinorder(configbase,configadd):
    import copy
    configbase=copy.deepcopy(configbase)

    for headers in configadd:
        if headers not in configbase.keys():
            configbase[headers]=dict();


        for keys in configadd[headers]:

            if keys not in configbase[headers].keys():
                configbase[headers][keys]=dict()
                configbase[headers][keys]["value"]=dict()
                configbase[headers][keys]["comment"]=dict()

            configbase[headers][keys]["value"]=configadd[headers][keys]["value"]
            try:
                configbase[headers][keys]["comment"]=configadd[headers][keys]["comment"]
            except:
                configbase[headers][keys]["comment"]="!==no comment specified=="





    return configbase


def evaluate_configinherit(config):
    import variablemanipulation.configmanipulation
    inheritfromlist=list()
    inherittolist=list()
    for keys in config:
        for subkeys in config[keys]:
            if ".inherit" in subkeys:

                inherittolist.append(keys)
                inheritfromlist.append(config[keys][subkeys]["value"])

    for index in range(len(inherittolist)):
        cfrom=inheritfromlist[index]
        cto=inherittolist[index]
        tempfrom=dict()
        tempfrom[cto]=config[cfrom]
        tempto=dict()
        tempto[cto]=config[cto]
        newconf= variablemanipulation.configmanipulation.evaluateinorder( tempfrom,tempto)
        config= variablemanipulation.configmanipulation.evaluateinorder( config,newconf)

    return config
