import re

artists=['uniq poet',]

def regexTitle(string):
    #getting title
    try:
        #fiding artist name
        found1=re.findall(r'.+\s[-]',string)
        artist=found1[0][:-1]
        
        #removing artist name from string
        string=string.replace(found1[0],'')
        
        #getting unwanted string
        try:
            found2 = re.findall(r'[[|(].*[]|)]',string,re.IGNORECASE)
            title=string.replace(found2[0],'')
        except:
            title=string
        
    except Exception as ec:
        print(ec)
        title=string
        artist=""
        
    return{'title':title.strip(),
           'artist':artist.strip()}
    
if __name__=="__main__":
    string = "Harry Styles - Golden Official Video"
    desc=regexTitle(string)
    print(desc)
    