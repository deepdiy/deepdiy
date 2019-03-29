def add_data_to_tree(tree,data,index_chain):
    if len(index_chain)==0:
        tree['children'].append(data)
    else:
        index_chain=[str(i) for i in index_chain]
        command='tree[\'children\']['+'][\'children\']['.join(index_chain)+'][\'children\'].append(data)'
        exec(command)
    return tree

def test():
    index_chain=[1,2,3,4]
    # index_chain=[]
    tree={'children':[{'children':[]},
    {'children':[{'children':[]},{'children':[]},
    {'children':[{'children':[]},{'children':[]},{'children':[]},
    {'children':[{'children':[]},{'children':[]},{'children':[]},{'children':[]},{'children':['here']}]}]}]}]}
    print(tree)
    print(add_data_to_tree(tree,'haha',index_chain))

if __name__ == '__main__':
    test()
