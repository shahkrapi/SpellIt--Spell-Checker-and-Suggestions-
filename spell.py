import re
from tkinter import *
import string
import tkinter.scrolledtext as st

dictionary ={}
freq_words={}

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def freq_list():
  f =  open('frequency.txt','r')
  test= f.readlines()
  for t in test:
    t=t.strip()
    n = t.split("\t")
    key = n[0]
    freq_words[key]=n[1]

def get_freq(word):
  if word in freq_words:
    freq=freq_words[word]
    return int(freq)
  else:
    return 1

def sort(list):
  dic={}
  sorted_list=[]
  for w in list:
    key=w
    dic[key]=get_freq(w)
  sort1=sorted(dic.items(), key=lambda x: x[1],reverse=True)
  for m in sort1:
    sorted_list.append(m[0])
  return sorted_list

def make_dict():
  f =  open('words.txt','r')
  test= f.readlines()
  words=[]
  for w in test:
    w = w.strip()
    words.append(w)
  for w in words:
    key = w[:2]
    dictionary.setdefault(key,[]).append(w)

def search_in_dict(word):
  key = word[:2]
  if key in dictionary.keys():
    if word in dictionary[key]:
      return True
    else:
      return False
  else:
    return False

def edits1(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)
  
def check_n_suggest():
 flag = 0
 data = t.get(1.0, 'end-1c')
 words=re.findall("[a-z']+", data.lower())
 for w in words:
  for c in string.punctuation:
    w= w.replace(c,"")
  is_correct = search_in_dict(w)
  if(is_correct==False):
    corr =  w.upper() + " Wrongly spelt. Possible corrections are : "
    flag = 1
    pos='1.0'
    index=t.search(w,pos,END)
    pos = '{}+{}c'.format(index, len(w))
    t.tag_add('wrong_word',index,pos)
    suggestion=[]
    poss = edits1(w)
    for word in poss:
      if(search_in_dict(word)):
        suggestion.append(word)
    sug=sort(suggestion)
    t2.insert(INSERT,corr)
    t2.insert(INSERT,sug)
    t2.insert(INSERT,"\n\n")
 if(flag==0):
  t2.insert(INSERT,"Correctly spelled document\n")
  
root = Tk()
topf = Frame(root)
topf.pack()
midf = Frame(root)
make_dict()
freq_list()
midf.pack()
botf = Frame(root)
botf.pack()
t2 = st.ScrolledText(botf,width=100,height=10)
t2.insert(INSERT,"Check your suggestions here\n")
t2.pack()
t = st.ScrolledText(topf,width=100,height=30)
t.tag_config('wrong_word',background="yellow")
b1 = Button(midf,text="submit",command=check_n_suggest)
b1.pack()
t.pack()
root.mainloop()
