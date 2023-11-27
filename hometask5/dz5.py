import os
import re


class Commit:
    type = ""
    branch_name = ""

    branch_from = ""
    merge_from = ""

    message = ""
    commit_id = ""
    last_commit_id = ""

    def __init__(self, commit_id, message, type_c, last_commit_id=None, branch_from=None, merge_from=None):
        self.type = type_c
        self.commit_id = commit_id
        self.message = message
        if last_commit_id is not None:
            self.last_commit_id = last_commit_id
        if branch_from is not None:
            self.branch_from = branch_from
        if merge_from is not None:
            self.merge_from = merge_from

    def get_type(self):
        return self.type

    def get_branch_from(self):
        return self.branch_from

    def get_merge_from(self):
        return self.merge_from

    def get_message(self):
        return self.message

    def get_commit_id(self):
        return self.commit_id

    def get_last_commit_id(self):
        return self.last_commit_id

    def __str__(self):
        return f'Commit №{self.commit_id}' \
               f' Type: {self.type}' \
               f' Last commit id: {self.last_commit_id}' \
               f' Message: {self.message}' \
               f' Branch from (if exists): {self.branch_from}' \
               f' Merge from (if exists): {self.merge_from}'


class Branch:
    name = ""
    commits = []

    def __init__(self, name):
        self.name = name
        self.commits = []

    def get_name(self):
        return self.name

    def get_commits(self):
        return self.commits

    def add_commit(self, commit: Commit):
        commit.branch_name = self.name
        self.commits.append(commit)

    def __str__(self):
        res = "Branch {name = " + self.name + " commits: "
        for commit in self.commits:
            res += str(commit) + "\n"
        res += "}"
        return res


class GitDataProcess:
    branches = []

    def __init__(self):
        self.branches = []

    def add_branch(self, branch):
        self.branches.append(branch)

    def get_message_from_branch(self, commit_id, branch_name):
        for branch in self.branches:
            if branch.get_name() == branch_name:
                for commit in branch.get_commits():
                    if commit.get_commit_id() == commit_id:
                        return commit.get_message()
        print(f'Message (branch: {branch_name}, commit id: {commit_id}) not found')
        return "error"

    # создание графа
    def make_tree(self, path):
        tb = TreeBuilder(path)

        for branch in self.branches:
            for commit in branch.get_commits():
                if commit.get_type() == "init":
                    pass
                elif commit.get_type() == "commit":
                    last_commit = None
                    for branch_c in self.branches:
                        for commit_c in branch_c.get_commits():
                            if commit_c.get_commit_id() == commit.get_last_commit_id():
                                if not (commit_c.branch_name == commit.branch_name) and commit_c.get_type() == "branch":
                                    continue
                                last_commit = commit_c
                                node_parent = Node(last_commit)
                                node_child = Node(commit)
                                tb.add_node(node_parent, node_child)
                                break
                elif commit.get_type() == "merge":
                    merge_from = commit.get_merge_from()
                    for branch_b in self.branches:
                        if branch_b.get_name() == merge_from:
                            for commit_c in branch_b.get_commits():
                                if commit_c.get_commit_id() == commit.get_last_commit_id():
                                    last_commit = commit_c
                                    node_parent = Node(last_commit)
                                    node_child = Node(commit)
                                    tb.add_node(node_parent, node_child)
                                    break
                elif commit.get_type() == "branch":
                    pass
                else:
                    print(f"error: commit type {commit.get_type()} not found")
        tb.save_tree()

    def __str__(self):
        res = "GitDataProcess{ Branches: "
        for branch in self.branches:
            res += str(branch) + "\n"
        res += "}"
        return res

class Node:
    parent = None
    children = []
    data = None

    def __init__(self, data, parent=None):
        self.data = data
        self.parent = parent
        self.children = []
        if self.parent is not None:
            self.parent.add_child(self)

    def get_data(self):
        return self.data

    def add_child(self, child):
        self.children.append(child)

    def show(self, level=0):
        print("\t" * level + str(self.data))
        for child in self.children:
            child.show(level + 1)


class TreeBuilder:
    path = ""
    nodes = []

    def __init__(self, path):
        self.path = path
        self.nodes = []

    def add_node(self, parent, new):
        temp = [parent, new]
        self.nodes.append(temp)

    def save_tree(self):
        print("digraph G {\n")
        for node in self.nodes:
            temp = "\""
            temp += node[0].get_data().branch_name + "\\n"
            temp += node[0].get_data().get_message()

            temp += "\" -> \""
            temp += node[1].get_data().branch_name + "\\n"
            temp += node[1].get_data().get_message()
            temp += "\""

            print(temp + "\n")
        print("}")



def read_files(path):
    gd = GitDataProcess()
    path_commits = path.replace("\\", "/") + ".git/logs/refs/heads"
    for filename in os.listdir(path_commits):
        with open(os.path.join(path_commits, filename), "r", encoding="utf-8") as file:
            branch = Branch(filename)
            for line in file:
                commit_info = line.split()
                last_commit_id = commit_info[0]
                current_commit_id = commit_info[1]
                commit_message = ""
                commit_message_match = re.search(r": (.+)", line)
                if commit_message_match:
                    commit_message = commit_message_match.group(1)

                commit = None
                if "commit (initial)" in line:
                    commit = Commit(current_commit_id, commit_message, "init")
                elif "commit" in line:
                    commit = Commit(current_commit_id, commit_message, "commit", last_commit_id=last_commit_id)
                elif "merge" in line:
                    merge_name = ""
                    merge_name_match = re.search(r"(?<=merge) (.+)", line)
                    if merge_name_match:
                        merge_name = merge_name_match.group(1)
                    merge_name = merge_name.strip().split(":")[0]
                    commit = Commit(current_commit_id, commit_message, "merge", last_commit_id=last_commit_id, merge_from=merge_name)
                elif "branch: Created from" in line:
                    branch_name = ""
                    branch_name_match = re.search(r"(?<=branch: Created from) (.+)", line)
                    if branch_name_match:
                        branch_name = branch_name_match.group(1)
                    branch_name = branch_name.strip()
                    commit = Commit(current_commit_id, commit_message, "branch", last_commit_id=last_commit_id, branch_from=branch_name)

                if commit is not None:
                    branch.add_commit(commit)
            gd.add_branch(branch)
    return gd


if __name__ == "__main__":
    test_path = str(input("Input git path directory: "))

    process = read_files(test_path)
    process.make_tree("output.txt")

