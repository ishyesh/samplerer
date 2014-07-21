
def genrandomnumber():  #Generate a random number

    import random
    numval=random.randrange(10000,90000)

    return numval


def decrangegen(start,stop,step):
    r = start
    while r < stop:
            yield r
            r += step

def decrange(start,stop,step):
    inum=decrangegen(start,stop,step)
    numrange=list()
    for vals in inum:
        numrange.append(round(vals,14))

    return numrange

def productoflist(listin):
    prodval=1;
    for s in listin:
        prodval=s*prodval

    return prodval


#This converts something like "{[1:0.1:4] [0:5]}   { [5 ]}" where {} indicates sequential groups and [] indicates sequential dimensions in a group
# into a list of lists

def interpretmatrixstring(stringin):

    #This sub-sub-function does the proper syntax manipulation to interpret
    def interpretmatrixentry(cstr):
        cstr=cstr.lstrip('[')
        cstr=cstr.rstrip(']')
        sepin=cstr.split(':')
        cout=cstr


        if len(sepin)==1:
            if "x" in sepin[0]:
                strana=sepin[0].split("x")
                cout=[float(strana[0])]*int(strana[1])
            else:
                cout=[float(sepin[0])]

        if len(sepin)==2:
            cout=decrange(float(sepin[0]),float(sepin[1])+1,1)

        if len(sepin)==3:
            cout=decrange(float(sepin[0]),float(sepin[2])+1,float(sepin[1]))


        return cout

    group=0
    dim=0
    findim=0
    startcollect=0

    matsum=list()


    totaldim=0
    totalgroup=0

    for chars in stringin:
        if chars == "{":
            group +=1
            dim=0
        if chars == "[":
            dim +=1
            startcollect=1
            cstr=""

        totaldim=max(totaldim,dim)
        totalgroup=max(totalgroup,group)

    for ngr in range(totalgroup):
        matsum.append([])
        for ndi in range(totaldim):
            matsum[ngr].append([])

    group=0
    dim=0
    findim=0
    startcollect=0

    for chars in stringin:
        if chars == "{":
            group +=1
            dim=0
        if chars == "[":
            dim +=1
            startcollect=1
            cstr=""

        if chars == "]":
            startcollect=0
            findim=1

        if startcollect:
            cstr=cstr+chars

        if findim:
            matsum[group-1][dim-1]=interpretmatrixentry(cstr)
            findim=0

    return matsum


def getallcombinations(listin):

    valeach=list()
    for g in listin:
        valeach.append(len(g))

    permuteval=permutecomb(valeach)
    combostore=list()
    for stepeach in range(len(permuteval)):
        combostore.append(list())

        for stepdim in range(len(listin)):
            combostore[stepeach].append(listin[stepdim][permuteval[stepeach][stepdim]])

    return  combostore



def permutecomb(valeach):
    import math

    totalcombos=1
    diml=0
    diveach=list()
    for valstep in valeach:
        diml+=1
        totalcombos=totalcombos*valstep

    diveach=[]
    for val in range(diml):
        diveach.append(productoflist(valeach[val+1:]))


    combomat=list()
    for cidx in range(totalcombos):
        combomat.append("")
        combomat[cidx]=list();
        for cdim in range(diml):
            combomat[cidx].append("")


    for cidx in range(totalcombos):
        for cdim in range(diml):
            combomat[cidx][cdim]=int(math.floor( float(cidx  / diveach[cdim] ))) % valeach[cdim]

    return combomat


def getformatting(listin):

    involvesdecimal=0
    lenstr=list()
    lenbeforedec=list()
    lenafterdec=list()

    lenbeforedec.append(0)
    lenafterdec.append(0)


    pointsafterdec=0
    for val in listin:
        for cidx in range(len(val)):
            cval=str(val[cidx])
            if "." in cval:
                involvesdecimal=1
            lenstr.append(len(cval))

            if involvesdecimal:
                lenbeforedec.append(len(cval.strip('.')[0]))
                lenafterdec.append(len(cval.strip('.')[1]))


    return max(lenstr),max(lenbeforedec),max(lenafterdec)



def producespacedvectors(vectorfrom,vectorto,spacing):
    import numpy, math
    import copy


    a=numpy.array(vectorfrom)
    b=numpy.array(vectorto)

    dist=numpy.linalg.norm(b-a)

    nsteps=math.ceil(dist/spacing)
    ngrad=numpy.ndarray.tolist(numpy.multiply((b-a),(1/nsteps)))


    vectorlist=list()
    cstart=vectorfrom
    for step in range(int(nsteps)):
        for dim in range(len(ngrad)):
            cstart[dim]=round(float(float(cstart[dim])+float(ngrad[dim])),5)

        vectorlist.append(copy.copy(cstart))


    return vectorlist




