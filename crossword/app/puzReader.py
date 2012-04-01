'''
Created on Mar 24, 2012

@author: alex
'''

import argparse, sys
from struct import unpack,unpack_from
from numpy import array, zeros


class puzFormat:
    #http://code.google.com/p/puz/wiki/FileFormat
    def read(self, filename):
        
        headerEnd = 0x34
        
        f = open(filename,'rb')
        data = f.read()
        self.readHeader(data)
        
        
        sol = data[headerEnd:headerEnd+self.width*self.height]
        self.readSolution(sol)
        
        board = data[headerEnd+self.width*self.height:headerEnd+(self.width*self.height)*2]
        self.readBoard(board)
        
    def readHeader(self,data):
        self.width = ord(data[0x2c])
        self.height = ord(data[0x2d])
        self.clueCount = unpack_from("<h",data,offset=0x2e)[0]
        
    def readSolution(self,data):
        #print data
        
        self.ansAcross = []
        
        answer = ''
        for char in data:
            if char == '.':
                if not len(answer) == 0:
                    self.ansAcross.append(answer)
                answer = ''
            else:
                answer += char
        #print self.ansAcross
        
    def readBoard(self,data):
        #print data
        
        self.board = zeros((self.height,self.width))
        
        for y in range(self.height):
            for x in range(self.width):
                self.board[x][y] = (data[y*self.height + x] == '.')
        
    def boardToHTML(self):
        html = "<html><head><script> function change() { alert('hello); } </script></head><body><table border=0.5 bgcolor=black>"
        for y in range(self.height):
            html += "<tr>"
            for x in range(self.width):
                if not self.board[x][y]:
                    html += "<td bgcolor=white ><input type=text onChange=\"alert('hello')\"/>&nbsp&nbsp&nbsp</td>"
                else:
                    html += "<td bgcolor=black>&nbsp&nbsp&nbsp</td>"
            html += "</tr>"
        html += "</table></body></html>"
        return html
                
        
    def __repr__(self):
        return str(self.width)+"x"+str(self.height)+"\nNumber of clues: "+str(self.clueCount)
        

def main(argv=None):
    #argparse grabs the filename for me
    parser = argparse.ArgumentParser(description='Match dates in given input file')
    parser.add_argument('filename', help='file to be examined')
    args = parser.parse_args()
    
    puz = puzFormat()
    puz.read(args.filename)
    print
    print puz
    
    f = open("out.html","w")
    f.write( puz.boardToHTML())


if __name__ == "__main__":
   sys.exit(main())