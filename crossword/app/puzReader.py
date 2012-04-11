'''
Created on Mar 24, 2012

@author: alex
'''

import argparse, sys
from struct import unpack,unpack_from
from numpy import array, zeros

class Cell:
    def __init__(self,val,x,y):
        self.x = x
        self.y = y
        self.value = val
        


class PuzFormat:
    #http://code.google.com/p/puz/wiki/FileFormat
    def read(self, filename):
        
        headerEnd = 0x34
        
        f = open(filename,'rb')
        data = f.read()
        self.readHeader(data)
        
        start = headerEnd
        end = start+self.width*self.height
        sol = data[start:end]
        self.readSolution(sol)
        
        start = end + self.width*self.height
        strings = data[start:]
        self.readStrings(strings)
        
    def readHeader(self,data):
        self.width = ord(data[0x2c])
        self.height = ord(data[0x2d])
        self.clueCount = unpack_from("<h",data,offset=0x2e)[0]
        
    def readSolution(self,data):
        ''''self.board = [[]*self.height]*self.width
        
        for y in range(self.height):
            for x in range(self.width):
                self.board[x][y] = Cell(data[y*self.height + x],x,y)'''
        
        self.board = [[Cell(data[y*self.height + x],x,y) for x in range(self.width)] for y in range(self.height)]
                
    def readStrings(self,data):
        #print data
        self.title = self.readString(data)
        print self.title
        
        data = data[len(self.title)+1:]
        self.author = self.readString(data)
        print self.author
        
        data = data[len(self.author)+1:]
        self.copyright = self.readString(data)
        print self.copyright
        
        data = data[len(self.copyright)+1:]
        self.clues = []
        while len(data) >= 0:
            self.clues.append(self.readString(data))
            if len(self.clues[-1]) == 0:
                break
            print self.clues[-1]
            data = data[len(self.clues[-1])+1:]
    
    def readString(self,data):
        string = ''
        for char in data:
            if char == '\0':
                return string
            else:
                string += char
        return string
        
    def __repr__(self):
        return str(self.width)+"x"+str(self.height)+"\nNumber of clues: "+str(self.clueCount)
        

def main(argv=None):
    #argparse grabs the filename for me
    parser = argparse.ArgumentParser(description='Match dates in given input file')
    parser.add_argument('filename', help='file to be examined')
    args = parser.parse_args()
    
    puz = PuzFormat()
    puz.read(args.filename)
    print
    print puz


if __name__ == "__main__":
   sys.exit(main())