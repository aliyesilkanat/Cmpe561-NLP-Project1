
# coding: utf-8

# In[73]:


import pywrapfst as ofst
import sys
FST_PATH='Morphophonemics/'
rules = ['y-ie','silente','einsert']
import easygui 


def set_input_fsm(input_string,ifst):
    for i in range(len(input_string)):
        #print ( ifst, str(i)+ " " + str(i+1)+ " " + input_string[i])
        print >> ifst, str(i)+ " " + str(i+1)+ " " + input_string[i]
    print >> ifst, str(len(input_string))
    #print(i)
    try:
        return ifst.compile()
    except:
        return None

def transduce((fst,ifst,isys),input_string):
    a=set_input_fsm(input_string,ifst)
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
def get_fst(name):
    syms=ofst.SymbolTable.read_text(FST_PATH+'symbols.txt')
    fst=ofst.Fst.read(FST_PATH+name.lower()+'.fst')
    return fst,ofst.Compiler(isymbols=syms,osymbols=syms,acceptor=True),syms  


# In[74]:


def run(input_string):
    matches=""
    found=False
    for i in rules:
        match=transduce(get_fst(i),input_string)
        if '+' in match:
            return match.replace("^","").replace("+","")
    if found==False:
        return input_string


# In[82]:


a=easygui.enterbox(title="Enter intermediate form")
if a!=None:
    results=run(a)
    if len(results)>0:
        easygui.textbox(text=results)
    else:
        easygui.textbox(text="No match!")

