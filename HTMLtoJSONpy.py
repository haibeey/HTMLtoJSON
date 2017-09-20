import sys 
import re
import json


class HTMLtoJSON(object):
    htmlTagStart=re.compile("<(?:[a-z\' '\=]+)>")
    htmlTagEnd=re.compile("</(?:[a-z\' '\=]+)>")

    def __init__(self,element):
        self.element=element
        
    def getJSONfromHTML(self):
        return json.dumps(self.elementNode(self.element))
    
    def getAttributes(self,string):
        try:
            reg=re.compile("</?(?:[a-z\' '\=]+)>").search(string).span()
            string=string[reg[0]+1:reg[1]-1]
            string=string.split()
            string=string[1:len(string)] #remove element
            #this would cost a little
            return {i.split("=")[0]:i.split("=")[1] for i in string}
        except Exception:
            return {}

    def getName(self,string,span):
        return string[span[0]+1:span[1]-1]

    def elementNode(self,element):
        hst=HTMLtoJSON.htmlTagStart.search(element)
        het=HTMLtoJSON.htmlTagEnd.search(element)
    
        if hst and het:
            main={'name':self.getName(element,hst.span()),
                  'textContent':"",
                  'attributes':{},
                  'children':[]
                    }
            childrenAndText=self.findChildrenAndText(element)
            main['textContent']=childrenAndText[1]

            for i in range(len(childrenAndText[0])):
                main['children'].append(self.elementNode(childrenAndText[0][i]))
            return main
        else:
            return element
        
    def sameTag(self,tag1,tag2):
        a=tag1[1:len(tag1)-1]
        b=tag2[2:len(tag1)-1]
        return a==b
        
    def  findChildrenAndText(self,element):
        reg=re.compile("</?(?:[a-z\' '\=]+)>")
        tags=[i.span() for i in reg.finditer(element)]
        if len(tags)==2:
            return [],element[tags[0][1]:tags[1][0]]
        first=tags[0];last=tags[-1]
        tags=tags[1:len(tags)-1]
        text=""
        children=[]
        x=0
        while x<len(tags):
            cur=x+1
            i=1
            while i!=0 and cur<len(tags):
                if HTMLtoJSON.htmlTagStart.match(element[tags[cur][0]:tags[cur][1]]):
                    i+=1
                if HTMLtoJSON.htmlTagEnd.match(element[tags[cur][0]:tags[cur][1]]):
                    i-=1
                cur+=1
            if(i==0):
                children.append(element[tags[x][0]:tags[cur-1][1]])
            x=cur
        if abs(tags[0][0]-first[1])>=1:
            sub=HTMLtoJSON.htmlTagStart.sub("",element[first[1]:tags[0][0]])
            text+=sub
        if abs(tags[-1][1]-last[0])>=1:
            sub=HTMLtoJSON.htmlTagEnd.sub("",element[tags[-1][1]:last[0]])
            text+="\n"
            text+=sub
        return children,text



def commandLineOption():
    arg=sys.argv
    inputFile=open(arg[1],'r')
    content=inputFile.read()
    inputFile.close()
    htj=HTMLtoJSON(content)
    with open(arg[2],"w") as f:
        f.write(htj.getJSONfromHTML())
if __name__!="__main__":
    commandLineOption()    
#j=HTMLtoJSON("<div><head><title>nonoe</title></head><body><div><textarea id='tx'class='a'></textarea></div><div ></div><script></script></body></div>")
#print(j.getJSONfromHTML())
