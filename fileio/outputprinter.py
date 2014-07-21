
def postinfo(string,level,dbglevel):
    import inspect
    import universal
    
  
    
    
    if level<=universal.printlevel:    
        print string
        
    
    if  dbglevel<=universal.debuglevel:
        stackinfo=inspect.stack()
        cdata=""
        for info in stackinfo[1:len(stackinfo)]:
            cdata=cdata+"\t\t"+info[3]+":"+info[4][0].strip()+"\t\tline:"+str(info[2])+ "\t\tfile: "+info[1] + "\n"
    
        cdata=cdata[:-1]        
        print cdata
    
    
    


    
    
    
    
    
    
