from giti.models import Repository
from settings import REPOSITORY_PATHS

def get_repo_or_404(name):
    assert REPOSITORY_PATHS.has_key(name)
    return Repository(name, REPOSITORY_PATHS[name])

def get_all_repositories():
    for name, path in REPOSITORY_PATHS.items():
        yield Repository(name, path)

def get_blob_or_404(commit, path):
    diff = commit.diff(paths=[path])
    if len(diff) > 0:
        return diff[0].b_blob
    if path:
        return commit.tree[path.strip('/')]
    else:
        return commit.tree
 
def get_tree_or_404(commit, path):
    if path:
        return commit.tree[path.strip('/')]
    else:
        return commit.tree
 
#def traverse_tree(tree, path):
#    if len(path) == 0 or path[0] == '':
#        return tree
#    nodes = [node for node in tree.trees if node.name == path[0]]
#    return traverse_tree(nodes[0], path[1:])


