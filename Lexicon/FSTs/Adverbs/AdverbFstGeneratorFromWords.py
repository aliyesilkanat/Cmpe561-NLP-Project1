
# coding: utf-8

# In[223]:


import sys
import itertools
from anytree import Node, RenderTree,Resolver,ChildResolverError,NodeMixin,PreOrderIter


# In[224]:


class CustomNode( NodeMixin):  # Add state number feature
    def __init__(self, name, state_number, parent=None):
        super(CustomNode, self).__init__()
        self.name=name
        self.state_number=state_number
        self.parent=parent


# In[220]:


state_number=0
top=CustomNode("root",state_number)
r = Resolver('name')

with open(sys.argv[1]) as f:
    words = f.readlines()
    words.sort()
    for word in words:
        trimmed_word=word.rstrip()
        root=top
        for i in range(len(trimmed_word)):
            try:
                n=r.get(root,trimmed_word[i])
            except ChildResolverError:
                state_number+=1
                n=CustomNode(trimmed_word[i],state_number,root)
            root=n


# In[221]:


#for pre, _, node in RenderTree(top):
#    treestr = u"%s%s" % (pre, node.name)
#    print(treestr.ljust(8), node.state_number)
def print_as_tabs(prev_state,next_state,input_label,output_label):
    print(str(prev_state) + "\t" + str(next_state) + "\t"+ str(input_label) + "\t" + str(output_label))


# In[222]:


p=PreOrderIter(top)
p=itertools.islice(p,1,None) #pass root

print_as_tabs(0,1,"<s>","<s>")
print_as_tabs(1,0,"<eps>","<eps>")
print_as_tabs(0,2,"</s>","</s>")
print_as_tabs(2,0,"<eps>","<eps>")
print_as_tabs(0,3,"<unk>","<unk>")
print_as_tabs(3,0,"<eps>","<eps>")
for n in p:
    parent_state_number=n.parent.state_number
    if n.parent.state_number!=0:
        parent_state_number+=3
    print_as_tabs(parent_state_number,n.state_number+3,n.name,n.name)
    if n.is_leaf:
        print_as_tabs(n.state_number+3,0,"+ADV","#")
print("0")

