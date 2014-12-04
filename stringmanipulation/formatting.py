def generateformatspecfromdecimals(lenstr,lenbeforepoint,lenafterpoint):
    formatspec=""

    if lenafterpoint==0:
        cvar="d"
        fvaladd=""

    elif lenafterpoint>0:
        cvar="f"
        fvaladd="."+str(lenafterpoint)


    formatspec='{:0>'+str(lenstr)+fvaladd+cvar+'}'


    return formatspec

def autogennumstringfromlength(number,veclen):
    import math
    fieldwidth=int(math.floor(math.log(veclen,10))+1)

    stringformat='{:0>'+str(fieldwidth)+'d}'
    string=stringformat.format(number)
    return string

def genvaluecommentstring(config):
    return config["value"]+" -   "+config["comment"]
