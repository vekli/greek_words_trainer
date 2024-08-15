import random
import pickle
import os
import sys


workbuffer_size=2       #How many words in repeating buffer
penalty=2               #How many correct andwers before memorized


dictionaryIn={}
dictionaryOut={}
workbuffer={}
penaltybuffer={}


profile_name=sys.argv[1]

dictI='dictI_'+profile_name+'.uf'
dictO='dictO_'+profile_name+'.uf'
dictB='dictB_'+profile_name+'.uf'
dictP='dictP_'+profile_name+'.uf'

if (os.path.isfile(dictI) and os.path.isfile(dictO) and os.path.isfile(dictB) and os.path.isfile(dictP)) is False:
  #First start
  with open('list.txt',encoding="utf-8") as f:
    for line in f:
     line=line.rstrip()
     translation=line
     line=f.readline()
     line=line.rstrip()
     dictionaryIn.update({line:translation})
  #Fill out workbuffer
  for  k in range(workbuffer_size): 
   a,b= random.choice(list(dictionaryIn.items()))
   del dictionaryIn[a]
   workbuffer.update({a:b})
   penaltybuffer.update({a:penalty})
  dictionaryOut.update({"0":"0"})
  with open(dictI, 'wb') as f:
    pickle.dump(dictionaryIn, f)
  with open(dictO, 'wb') as f:
    pickle.dump(dictionaryOut, f)
  with open(dictB, 'wb') as f:
    pickle.dump(workbuffer, f)
  with open(dictP, 'wb') as f:
    pickle.dump(penaltybuffer, f)
  
else:   
    
 with open(dictI, 'rb') as f:
    dictionaryIn = pickle.load(f)
    f.close()
 with open(dictO, 'rb') as f:
    dictionaryOut = pickle.load(f)
    f.close()
 with open(dictB, 'rb') as f:
    workbuffer = pickle.load(f)
    f.close()
 with open(dictP, 'rb') as f:
    penaltybuffer = pickle.load(f)
    f.close()



while True:
  Gword, Eword = random.choice(list(workbuffer.items()))
  print("  ",end='')
  print(Gword,end='')
  print(" - ",end='')
  print(Eword)

  Gword_hidden=Gword
  Gword_hidden=Gword_hidden.replace("\u03AC","\u03B1")     #α
  Gword_hidden=Gword_hidden.replace("\u03AD","\u03B5")     #ε
  Gword_hidden=Gword_hidden.replace("\u03CC","\u03BF")     #ο
  Gword_hidden=Gword_hidden.replace("\u03CD","\u03C5")     #υ
  Gword_hidden=Gword_hidden.replace("\u03CE","\u03C9")     #ω
  Gword_hidden=Gword_hidden.replace("\u03AE","\u03B7")     #η
  Gword_hidden=Gword_hidden.replace("\u03AF","\u03B9")     #ι
  Gword_hidden=Gword_hidden.replace("\u0386","\u0391")     #Α
  Gword_hidden=Gword_hidden.replace("\u0388","\u0395")     #Ε
  Gword_hidden=Gword_hidden.replace("\u038C","\u039F")     #Ο
  Gword_hidden=Gword_hidden.replace("\u038E","\u03A5")     #Υ
  Gword_hidden=Gword_hidden.replace("\u038F","\u03A9")     #Ω
  Gword_hidden=Gword_hidden.replace("\u0389","\u0397")     #Η
  Gword_hidden=Gword_hidden.replace("\u038A","\u0399")     #Ι  
   
  input_var = input("> ")
  if Gword_hidden==input_var:
        print("  Correct.")
        penaltybuffer[Gword]-=1
        penaltybuffer.update({Gword:penaltybuffer[Gword]})
  else:
        print("  Incorrect.")
  if penaltybuffer[Gword] == 0:  
      del workbuffer[Gword]
      dictionaryOut.update({Gword:Eword})
      while len(workbuffer) < workbuffer_size:
       a,b= random.choice(list(dictionaryIn.items()))
       del dictionaryIn[a]
       workbuffer.update({a:b})
       penaltybuffer.update({a:penalty})
      
  with open(dictI, 'wb') as f:
    pickle.dump(dictionaryIn, f)
  with open(dictO, 'wb') as f:
    pickle.dump(dictionaryOut, f)
  with open(dictB, 'wb') as f:
    pickle.dump(workbuffer, f)
  with open(dictP, 'wb') as f:
    pickle.dump(penaltybuffer, f)
  print("------------------------------------")


 


        
