import zlib
import os
import graphviz


commits_info = []
file_pathes = []
for dirname, dirnames, filenames in os.walk('.git\objects'):
    for subdirname in dirnames:
        print(os.path.join(dirname, subdirname))


    for filename in filenames:
        if 'pack' in dirname or 'info' in dirname: continue
        file_pathes.append(os.path.join(dirname, filename))
        with open(os.path.join(dirname, filename), 'rb') as object_file:
            raw_object_content = zlib.decompress(object_file.read())

        header, content = raw_object_content.split(b'\x00', maxsplit=1)
        object_type, content_size = header.decode().split()

        try:
            content = content.decode()
        except UnicodeDecodeError:
            pass

        if ("commit" in object_type):
            commits_info.append([filename, content, graphviz.Digraph(content.split('\n')[-2])])

parent_graph = graphviz.Digraph()
for commit in commits_info:
    parent = commit[1].split('\n')[1].split(' ')[1]
    parent_name = parent[2:]
    have_parent = False
    for commit_sub in commits_info:
        if commit_sub[0] == parent_name:
            commit_sub[2].subgraph(commit[2])
            have_parent = True
    if not(have_parent):
        parent_graph = commit[2]

print(parent_graph.source)