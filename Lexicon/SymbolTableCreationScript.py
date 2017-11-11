import sys
symbols=set()

with open(sys.argv[1]) as f:
    lines=f.readlines()
    for line in lines:
        l=line.split('\t')
        if len(l) ==3:
            symbols.add(l[2])
            symbols.add(l[3].rstrip())
symbols.discard('<eps>')
symbols.discard('<s>')
symbols.discard('</s>')
symbols.discard('<unk>')
ls=list(symbols)
ls=['<eps>','<s>','</s>','<unk>']+ls
for i in range(len(ls)):
    print(str(ls[i])+ "\t"+ str(i))
    
