
# coding: utf-8

# In[5]:


import pywrapfst as ofst
import easygui 
LEX_PATH='Lexicon/FSTs/'
categories =['Verbs','Nouns','Pronouns','Adjectives','Adverbs','Propositions','Auxillary Verbs'] 
MORPH_PATH='Morphophonemics/'
rules = ['y-ie','silente','einsert']
LEX="LEX"
MORPH="MORPH"


# In[6]:


def set_input_fsm_int(input_string,ifst,isys):
    i=0
    while input_string[i]!='+':
        #print(str(i)+ " " + str(i+1)+ " " + input_string[i])
        print >> ifst, str(i)+ " " + str(i+1)+ " " + input_string[i]
        i+=1
    props=input_string[i+1:].split('+')
    for p in props:
        #print(str(i) + " " + str(i+1)+" +" +p)
        print >> ifst, str(i) + " " + str(i+1)+" +" +p
        i+=1
    print >> ifst, str(i)

    #print(i)
    try:
        return ifst.compile()
    except:
        return None
def set_input_fsm_surf(input_string,ifst):
    for i in range(len(input_string)):
        #print ( ifst, str(i)+ " " + str(i+1)+ " " + input_string[i])
        print >> ifst, str(i)+ " " + str(i+1)+ " " + input_string[i]
    print >> ifst, str(len(input_string))
    #print(i)
    try:
        return ifst.compile()
    except:
        return None
def transduce((fst,ifst,isys),input_string,strategy):
    if strategy==LEX:
        a=set_input_fsm_int(input_string,ifst,isys)
    else:
        a=set_input_fsm_surf(input_string,ifst)
    if a==None:
        return "";
    else:
        b=ofst.compose(a,fst)
        b.set_input_symbols(isys)
        b.set_output_symbols(isys)
        b.project(project_output=True)
        lines=b.text(acceptor=True).split("\n")
        output=""
        for l in lines:
            sp=l.split("\t")
            if len(sp)==3 and sp[2]!='<eps>':
                output+=sp[2]
        return output
def get_lex_fst(name):
    syms=ofst.SymbolTable.read_text(LEX_PATH+name+'/symbols.txt')
    fst=ofst.Fst.read(LEX_PATH+name+'/'+name.lower()+'.fst')
    return fst,ofst.Compiler(isymbols=syms,osymbols=syms,acceptor=True),syms  
def get_morph_fst(name):
    syms=ofst.SymbolTable.read_text(MORPH_PATH+'symbols.txt')
    fst=ofst.Fst.read(MORPH_PATH+name.lower()+'.fst')
    return fst,ofst.Compiler(isymbols=syms,osymbols=syms,acceptor=True),syms  


# In[7]:


def run_lex2int(input_string):
    matches=""
    found=False
    for i in categories:
        match=transduce(get_lex_fst(i),input_string,LEX)
        if match!="":
            matches+=match+"\n"
            found=True
    if found==False:
        print("No match!")
    return matches
def run_int2surf(input_string):
    matches=""
    found=False
    for i in rules:
        match=transduce(get_morph_fst(i),input_string,MORPH)
        if '+' in match:
            return match.replace("^","").replace("+","")
    if found==False:
        return input_string


# In[9]:


a=easygui.enterbox(title="Enter lexical form")
if '+' not in a:
    easygui.textbox(text="No match, because you did not enter any POS tag")
elif a!=None and a!="":
    results_int=run_lex2int(a)
    if len(results_int)>0:
        output="Intermediate form:\n"+results_int
        result_surface=""
        for form in results_int.split("\n"):
            result_surface+=run_int2surf(form)+"\n"
        easygui.textbox(title="Results",text=output + "\nSurface form:\n" + result_surface)
    else:
        easygui.textbox(text="No match!")

