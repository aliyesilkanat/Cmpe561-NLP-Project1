import pywrapfst as ofst
import easygui 
FST_PATH='Lexicon/FSTs/'
categories =['Verbs','Nouns','Pronouns','Adjectives','Adverbs','Propositions'] 
def set_input_fsm(input_string,ifst,isys):
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

def transduce((fst,ifst,isys),input_string):
    a=set_input_fsm(input_string,ifst,isys)
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
    syms=ofst.SymbolTable.read_text(FST_PATH+name+'/symbols.txt')
    fst=ofst.Fst.read(FST_PATH+name+'/'+name.lower()+'.fst')
    return fst,ofst.Compiler(isymbols=syms,osymbols=syms,acceptor=True),syms  

def run(input_string):
    matches=""
    found=False
    for i in categories:
        match=transduce(get_fst(i),input_string)
        if match!="":
            matches+=(transduce(get_fst(i),input_string)+"\n")
            print(transduce(get_fst(i),input_string))
            found=True
    if found==False:
        print("No match!")
    return matches



a=easygui.enterbox(title="Enter lexical form")
if a!=None:
    results=run(a)
    if len(results)>0:
        easygui.textbox(text=results)
    else:
        easygui.textbox(text="No match!")
