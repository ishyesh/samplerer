'''
Created on Jun 24, 2014

@author: isp
'''

def readrxncoor(rxncoordef):
    f=open(rxncoordef,'r')
    lines=f.readlines()
    rxncoor=dict()
    rxncoor["text"]=list()
    for cline in lines:
        rxncoor["text"].append(cline.strip())
        if "nrxn" in cline:
            splitindx=cline.split();
            rxncoor["amount"]=int(splitindx[3])
            rxncoor["names"]=splitindx[4:len(splitindx)]



    return rxncoor



def createfoldername(*argsin):
    import variablemanipulation.numberoperations
    import stringmanipulation.formatting

    formatspecstore=list()
    lendname=list()
    for idxin in range(1,len(argsin),2):
        [lenstr,lenbeforedec,lenafterdec]=variablemanipulation.numberoperations.getformatting(argsin[idxin])
        formatspecstore.append(stringmanipulation.formatting.generateformatspecfromdecimals(lenstr,lenbeforedec,lenafterdec))
        lendname.append(len(argsin[idxin]))

    lendname=min(lendname)

    foldernames=list()
    for stepdir in range(0,lendname):
        strwrite=""
        formatcounter=-1
        for stepsim in range(1,len(argsin),2):
            formatcounter+=1
            for steplist in argsin[stepsim][stepdir]:
                strwrite=strwrite+argsin[stepsim-1]+formatspecstore[formatcounter].format(steplist)+"_"


        foldernames.append(strwrite.rstrip('_'))

    return foldernames



