#!/usr/bin/python
import graphviz as gv 
import functools
digraph = functools.partial(gv.Digraph, format='svg')
def add_nodes(graph, nodes):
    for n in nodes:
        if isinstance(n, tuple):
            graph.node(n[0], **n[1])
        else:
            graph.node(n)
    return graph

def add_edges(graph, edges):
    for e in edges:
        if isinstance(e[0], tuple):
            graph.edge(*e[0], **e[1])
        else:
            graph.edge(*e)
    return graph

def show_graph(nodes,edges,img_name):
	print "show over"
	add_edges(add_nodes(digraph(), nodes), edges).render('img/' + img_name)
	#add_edges(add_nodes(digraph(), ['a','b','c']),[('a', 'b'),('a','c')]).render('img/g4')
# for test
#if __name__ == '__main__':
	#add_edges(add_nodes(digraph(), ['A', 'B', 'C']),[('A', 'B'), ('A', 'C'), ('B', 'C')]).render('img/g4')
#	show_graph(digraph)
