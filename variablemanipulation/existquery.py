'''
Created on Jun 24, 2014

@author: isp
'''
def existheaderandkey(header,key,config):
    try:
        config[header][key]
        eh=1
    except:
        eh=0
        
    return eh
        