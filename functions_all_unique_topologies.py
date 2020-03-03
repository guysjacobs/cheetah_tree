###Simple function to generate lists of possible unique bifurcating tree topologies.
###Used in Rai et al "Ancient mtDNA from the extinct Indian cheetah supports unexpectedly deep divergence from African cheetahs"
###There are presumably much better algorithms to achieve a similar goal with larger numbers of taxa.

###GSJ Dec 2019

import numpy as np
import ete3
import copy

print RuntimeWarning("recursive_generate_topologies_bifurcating_unique only works if neighbour_list doesn't contain repeated taxa.")
print RuntimeWarning("recursive_generate_topologies_bifurcating_unique is only really fast enough for up to 7 or perhaps 8 taxa.")

def recursive_generate_topologies_bifurcating_unique(neighbour_list = ['1', '2', '3'], tree_list = [], tree_id_set_ete = set()):
    """
    This generates all possible bifurcating trees for the neighbour_list of *non-repeating* taxa.
    It uses the ete3 method get_topology_id to ensure that only unique topology trees are kept.
    It only works in reasonable time if len(neighbout_list) is <=7 or perhaps 8.
    """
    if len(neighbour_list) == 2:
        new_tree = "(%s,%s);" %(neighbour_list[0], neighbour_list[1])
        new_tree_ete_id = ete3.Tree(newick = new_tree).get_topology_id()
        if new_tree_ete_id not in tree_id_set_ete:
            tree_list.append(new_tree)
            tree_id_set_ete.add(new_tree_ete_id)
    else:
        for i in xrange(len(neighbour_list)):
            for j in xrange(i):
                remaining = copy.copy(neighbour_list)
                if i > j:
                    left = remaining.pop(remaining.index(neighbour_list[i]))
                    right = remaining.pop(remaining.index(neighbour_list[j]))
                else:
                    left = remaining.pop(remaining.index(neighbour_list[j]))
                    right = remaining.pop(remaining.index(neighbour_list[i]))
                recursive_generate_uniquetopologies(["(%s,%s)" %(left, right)] + remaining, tree_list = tree_list, tree_id_set_ete = tree_id_set_ete)
                if len(tree_list) % 1000 == 0:
                    print "Generated %d trees" %(len(tree_list))
    return tree_list

def writeout_tree_list(fileout, tree_list):
    with open(fileout, 'w') as f:
        for tree in tree_list:
            f.write(tree + '\n')
    return None
