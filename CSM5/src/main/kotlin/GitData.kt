import java.util.*


class GitData {
    private val branches = ArrayList<Branch>()


    fun addBranch(branch: Branch) {
        branches.add(branch)
    }

    fun makeFiles(path: String?) {
        val builder = TreeBuilder()
        for (branch in branches) {
            val commits = branch.getCommits()
            for (i in commits.indices) {
                val commit = commits[i]
                when (commit.type) {
                    "init" -> {}
                    "commit" -> builder.addNode(
                        commit.id,
                        commit.lastId,
                        branch.name,
                        branch.name,
                        commit.message,
                        commits[i - 1].message
                    )
                    "newbranch" -> {}
                    "merge" -> builder.addNode(
                        commit.id,
                        commit.lastId,
                        branch.name,
                        commit.mergeFrom,
                        commit.message,
                        getMessageFromAnotherBranch(commit.lastId!!, commit.mergeFrom!!)
                    )

                    else -> println("ERROR: commit type not found")
                }
            }
        }
        builder.saveGraphvizTree(path)
        builder.saveTree(path)
    }

    private fun getMessageFromAnotherBranch(id: String, branchName: String): String {
        for (branch in branches) {
            if (branch.name == branchName) {
                for (commit in branch.getCommits()) {
                    if (commit.id == id) {
                        return commit.message
                    }
                }
            }
        }
        println("Message not found for $id in branch $branchName")
        return "ERROR"
    }
}
