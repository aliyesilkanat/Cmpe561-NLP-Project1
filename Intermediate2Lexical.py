
# coding: utf-8

# In[58]:


import pywrapfst as ofst
import easygui 
FST_PATH='Lexicon/FSTs/'
categories =['Verbs','Nouns','Pronouns','Adjectives','Adverbs','Propositions','Auxillary Verbs'] 


# In[59]:


def set_input_fsm(input_string,ifst):
    input_string=input_string[::-1]
    for i in range(len(input_string)):
        #print(str(i)+ " " + str(i+1)+ " " + input_string[i])
        print >> ifst, str(i)+ " " + str(i+1)+ " " + input_string[i]
    #print (str(i+1))
    print >> ifst,str(i+1)
    try:
        return ifst.compile()
    except:
        return None
def transduce((fst,ifst,isys),input_string):
    a=set_input_fsm(input_string,ifst)
    if a==None:
        return "";
    else:
        b=ofst.compose(fst,a)
        b.set_input_symbols(isys)
        lines=b.text(acceptor=True).split("\n")
        output=""
        for l in lines:
            sp=l.split("\t")
            if len(sp)==4 and sp[2]!='<eps>':
                if sp[2][0]=='+':
                    output+=sp[2][::-1]
                else:
                    output+=sp[2]
        return output[::-1]
def get_fst(name):
    syms=ofst.SymbolTable.read_text(FST_PATH+name+'/symbols.txt')
    fst=ofst.Fst.read(FST_PATH+name+'/'+name.lower()+'.fst')
    return ofst.reverse(fst),ofst.Compiler(isymbols=syms,osymbols=syms,acceptor=True),syms  


# In[64]:


def run(input_string):
    matches=""
    found=False
    for i in categories:
        match=transduce(get_fst(i),input_string)
        if match!="":
            matches+=match+"\n"
            found=True
    if found==False:
        print("No match!")
    return matches


# In[68]:


a=easygui.enterbox(title="Enter intermediate form")
if a!=None and a!="" :
    results=run(a)
    if len(results)>0:
        easygui.textbox(title="Results",text=results)
    else:
        easygui.textbox(text="No match!")

