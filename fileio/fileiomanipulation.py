

class StripTabsAndBlanks(object):  #This creates an file object that other functions can use.  This function automatically removes blank lines and tabs from the input file
    def __init__(self,f):
        self.fileobj = open(f)
        self.data = ( x.strip() for x in self.fileobj )
    def readline(self):
        try:
            currentline=next(self.data)
        except:
            return

        while len(currentline)==0:
            try:
                currentline=next(self.data)
            except:
                return

        return currentline
    def close(self):
            self.fileobj.close()


def makedirectory(directory):
    import os
    if not os.path.exists(directory):
        os.makedirs(directory)
