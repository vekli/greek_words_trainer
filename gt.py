from gtts import gTTS
import random
import pickle
import os
import sys
from io import BytesIO
import pygame
import time
from colorama import Fore


workbuffer_size=15       #How many words in repeating buffer
penalty=5               #How many correct andwers before memorized


dictionaryIn={}
dictionaryOut={}
workbuffer={}
penaltybuffer={}

list_beginner="list_beginner.txt"
list_preintermediate="list_preintermediate.txt"
list_intermediate="list_intermediate.txt"
list_upperintermediate="list_upperintermediate.txt"
list_advanced="list_advanced.txt"

if len(sys.argv)==4:
  profile_name=sys.argv[1]
  mode=sys.argv[2]
  level=sys.argv[3]
elif len(sys.argv)==3:
  profile_name=sys.argv[1]
  mode=sys.argv[2]
  level="beginner"
elif len(sys.argv)==2:
  profile_name=sys.argv[1]
  mode="copy"
  level="beginner"
elif len(sys.argv)==1:
  profile_name="test"
  mode="copy"
  level="beginner"

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
  pf.close()
  pf2=BytesIO(open('tmp.mp3','rb').read())
   
  if pf2:
      xx=pygame.mixer.Sound(pf2)
      pygame.mixer.Sound.play(xx)
  else:
      print("gTTS error")
      
      
def check_vowel(symbol):
    if symbol=="\u03B1" or symbol=="\u03B5" or symbol=="\u03BF" or symbol=="\u03C5" or symbol=="\u03C9" or symbol=="\u03B7" or symbol=="\u03B9" or symbol=="\u0391" or symbol=="\u0395"or symbol=="\u039F"or symbol=="\u03A5" or symbol=="\u03A9" or symbol=="\u0397" or symbol=="\u0399":      
      return 1
    else:
      return 0
      
      
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
  
  print("  ",end='')
  Gword_hidden_list=list(Gword_hidden)
  for k in range(0,len(Gword_hidden_list)):
      if check_vowel(Gword_hidden_list[k]):
       print(f"{Fore.RED}"+Gword_hidden_list[k],end='') 
      else:
       print(f"{Fore.BLUE}"+Gword_hidden_list[k]+f"{Fore.WHITE}",end='')  
      if check_vowel(Gword_hidden_list[k]) and k!=(len(Gword_hidden_list)-1) and check_vowel(Gword_hidden_list[k+1])==0 and Gword_hidden_list[k+1]!="\u0020":
        print("-",end='')
  print(f"{Fore.WHITE}")     
  
  """
  for k in range(0,len(Gword_hidden_list)): 
      print(Gword_hidden_list[k],end='')  
      if k!=(len(Gword_hidden_list)-1):
        print("-",end='')
  print("") 
  """
  
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
  if level=="beginner":
   list_file=list_beginner
  if level=="pintermediate":
   list_file=list_preintermediate
  if level=="intermediate":   
   list_file=list_intermediate
  if level=="uintermediate":
   list_file=list_upperintermediate
  if level=="advanced":
   list_file=list_advanced
  with open(list_file,encoding="utf-8") as f: 
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
        print(f"{Fore.GREEN}  Correct.{Fore.WHITE}")
        penaltybuffer[Gword]-=1
        penaltybuffer.update({Gword:penaltybuffer[Gword]})
        if penaltybuffer[Gword] == 0:  
           remove_word_from_buffer(Gword, Eword)  
           
           while len(workbuffer) < workbuffer_size:
            a,b= random.choice(list(dictionaryOut.items()))
            play_word(a)
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
        print(f"{Fore.RED}   Incorrect.{Fore.WHITE}")
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
  


 


        
