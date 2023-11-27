class Branch(val name: String) {

    private val commits = ArrayList<Commit>()


    fun getCommits(): List<Commit> {
        return commits
    }

    fun addCommit(commit: Commit) {
        commits.add(commit)
    }
}

