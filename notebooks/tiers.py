"""
Tiers - hierarchical label handling
v.0.0.1 - 2023-09-20

Copyright (c) 2023 Mikko Impiö
 
Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Dependencies: pandas, bigtree
"""
import bigtree
import pandas as pd

def leaf_relations(row):
    """Handles the pairwise relations for a dataset row"""
    r = []
    for i in range(1,len(row)):
        if not pd.isna(row.iloc[-i]):
            r.append((row.iloc[-i], row.iloc[-i-1]))
    return r
    
def table2rel(df):
    """Turns a pandas DataFrame into a relational list"""
    r = []
    for i, row in df.iterrows():
        r.append(leaf_relations(row))
    r = [item for sublist in r for item in sublist]
    rel = pd.DataFrame(r, columns=["names", "parents"]).drop_duplicates()
    return rel

def zip_series(names, parents):
    """Turns two series into a zipped list"""
    names = names.values.tolist()
    parents = parents.values.tolist()
    rel_list = list(zip(parents, names))
    return rel_list

# Bigtree functions
def rel2tree(rel, names_col="names", parents_col="parents"):
    """Turns a relational dataframe into a Bigtree tree"""
    names = rel[names_col].values.tolist()
    parents = rel[parents_col].values.tolist()
    rel_list = list(zip(parents, names))
    return bigtree.list_to_tree_by_relation(rel_list)

def table2tree(df, names_col="names", parents_col="parents"):
    """Turns a pandas DataFrame into a Bigtree tree"""
    rel = table2rel(df)
    return rel2tree(rel, names_col=names_col, parents_col=parents_col)

def coarsen(labels, root, depth, return_map=False):
    """Coarsens a list of labels based on a depth in a tree"""
    new_map = {}
    for leaf in list(root.leaves):
        orig_label = leaf.name
        while leaf.depth > depth:
            leaf = leaf.parent
        
        new_map[orig_label] = leaf.name

    r = list(map(lambda x: new_map[x], labels)) 
    if return_map:
        return r, new_map
    return r

def prune_by_leaves(root, leaves):
    """Prunes a tree by a list of leaves that are left over"""
    paths = []
    for t in leaves:
        t = bigtree.find_name(root, t)
        if t:
            paths.append(t.path_name)
    return bigtree.list_to_tree(paths)

def get_label_map(taxon_table):
    """Returns a dict that maps taxon labels to their lowest known taxon 
    in a taxon table
    """
    taxa_map = {}
    for i in range(len(taxon_table)):
        label = taxon_table.iloc[i,-1]
        row = taxon_table.iloc[i, :-1]
        
        # Go through row values
        i = -1
        c = None
        while pd.isna(c):
            c = row.iloc[i]
            i -= 1
        taxa_map[label] = c
    return taxa_map

def simplify_tree(node):
    """Simplifies a tree so that every leaf has at least one sibling on the same level"""
    leaf_list = [x for x in node.leaves]

    leaf_map = {}

    path_list = []
    for leaf in leaf_list:
        name = leaf.name
        while leaf.siblings == ():
            leaf = leaf.parent
        leaf_map[name] = leaf.name
        path_list.append(leaf.path_name)
    return bigtree.list_to_tree(path_list), leaf_map

def simplify_labels(labels, root, return_map=False):
    _, smap = simplify_tree(root)

    new_labels = list(map(lambda x: smap[x], labels))
    if return_map:
        return new_labels, smap
    else:
        return new_labels

def LCA(root, taxon_a, taxon_b):
    """Returns the lowest common ancestor """
    node_a = bigtree.find_path(root, taxon_a)
    node_b = bigtree.find_path(root, taxon_b)

    if (not node_a) or (not node_b):
        return None

    if node_a == node_b:
        return node_a

    # Find deeper node
    if node_a.depth == node_b.depth:
        deeper = node_a
        higher = node_b
    elif node_a.depth > node_b.depth:
        deeper = node_a
        higher = node_b
    else:
        deeper = node_b
        higher = node_a

    while deeper.depth != higher.depth:
        deeper = deeper.parent

    while deeper != higher:
        deeper = deeper.parent
        higher = higher.parent
    return deeper
