from gtts import gTTS
import random
import pickle
import os
import sys
#from io import BytesIO
import pygame
import time



workbuffer_size=3       #How many words in repeating buffer
penalty=2               #How many correct andwers before memorized


dictionaryIn={}
dictionaryOut={}
workbuffer={}
penaltybuffer={}


profile_name=sys.argv[1]
mode=sys.argv[2]

words_counter=0
bad_counter=0

dictI='dictI_'+profile_name+'.uf'
dictO='dictO_'+profile_name+'.uf'
dictB='dictB_'+profile_name+'.uf'
dictP='dictP_'+profile_name+'.uf'

def play_word(word):
  tts = gTTS(word,lang="el", slow=False)
  pf=open('tmp.mp3','wb')
  tts.write_to_fp(pf)
  pf2=BytesIO(open('tmp.mp3','rb').read())
  pf.close()
  xx=pygame.mixer.Sound(pf2)
  pygame.mixer.Sound.play(xx)
  
def remove_tonos(word):
  word_wo_tonos=word
  word_wo_tonos=word_wo_tonos.replace("\u03AC","\u03B1")     #α
  word_wo_tonos=word_wo_tonos.replace("\u03AD","\u03B5")     #ε
  word_wo_tonos=word_wo_tonos.replace("\u03CC","\u03BF")     #ο
  word_wo_tonos=word_wo_tonos.replace("\u03CD","\u03C5")     #υ
  word_wo_tonos=word_wo_tonos.replace("\u03CE","\u03C9")     #ω
  word_wo_tonos=word_wo_tonos.replace("\u03AE","\u03B7")     #η
  word_wo_tonos=word_wo_tonos.replace("\u03AF","\u03B9")     #ι
  word_wo_tonos=word_wo_tonos.replace("\u0386","\u0391")     #Α
  word_wo_tonos=word_wo_tonos.replace("\u0388","\u0395")     #Ε
  word_wo_tonos=word_wo_tonos.replace("\u038C","\u039F")     #Ο
  word_wo_tonos=word_wo_tonos.replace("\u038E","\u03A5")     #Υ
  word_wo_tonos=word_wo_tonos.replace("\u038F","\u03A9")     #Ω
  word_wo_tonos=word_wo_tonos.replace("\u0389","\u0397")     #Η
  word_wo_tonos=word_wo_tonos.replace("\u038A","\u0399")     #Ι  
  
  return word_wo_tonos
  
def test_word(Gw,Ew):
  print("  ",end='')
  if(mode == "dictant"):
    print("hidden",end='') 
  else:
    print(Gw,end='')
  print(" - ",end='')
  print(Ew)
  Gword_hidden=remove_tonos(Gw)
  input_var = input("> ")
  if Gword_hidden==input_var:
   return 1
  else:
   return 0
      
def remove_word_from_buffer(Gw,Ew):
    del workbuffer[Gw]
    dictionaryOut.update({Gw:Ew})
        
        
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
   penaltybuffer.update({a:random.randint(1,penalty)})
  #dictionaryOut.update({"0":"0"})
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


pygame.mixer.init()

while True:
  Gword, Eword = random.choice(list(workbuffer.items()))
  words_counter+=1
  play_word(Gword)
 
  if test_word(Gword,Eword):
        print("  Correct.")
        penaltybuffer[Gword]-=1
        penaltybuffer.update({Gword:penaltybuffer[Gword]})
        if penaltybuffer[Gword] == 0:  
           remove_word_from_buffer(Gword, Eword)  
           
           while len(workbuffer) < workbuffer_size:
            a,b= random.choice(list(dictionaryOut.items())) 
            if test_word(a,b):
              a,b = random.choice(list(dictionaryIn.items()))
              del dictionaryIn[a]    
              print("New word added",end='')  
              print(" "+a+" - "+b) 
            else:            
              del dictionaryOut[a] 
              print("Incorrect")        
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
        #play_word("Μπράβο!")
        #time.sleep(1)
  else:
        if(mode == "dictant"):
          print("  ",end='')
          print(Gword) 
        print("  Incorrect.")
        bad_counter+=1
        #play_word("Κακώς!")
        #time.sleep(1)
  print("------------------------------------ ",end='')   
  print(words_counter,end='')
  print(" words session. ",end='')
  print(int((bad_counter/words_counter)*100),end='')
  print("% err. ",end='')
  print(len(dictionaryOut),end='')
  print(" words learned. ")
  


 


        
