import java.io.BufferedReader
import java.io.File
import java.io.FileReader
import java.io.IOException
import java.util.regex.Pattern

fun applyRegex(input: String?, regex: String?): String {
    val pattern = Pattern.compile(regex)
    val matcher = pattern.matcher(input)
    return if (matcher.find()) {
        matcher.group(1)
    } else {
        ""
    }
}

// Создание графа
fun createGraph(branch: Branch, data: GitData, path: String) {
    val file = File(path)
    val bufferedReader = BufferedReader(FileReader(file))
    var line: String? = bufferedReader.readLine()
    println(branch.name)
    while (line != null) {
        val commitInfo = line.split(" ".toRegex()).dropLastWhile { it.isEmpty() }.toTypedArray()
        val lastCommitId = commitInfo[0]
        val currentCommitId = commitInfo[1]
        val commitMessage = applyRegex(line, ": (.+)")
        var commit: Commit? = null
        if (line.contains("commit (initial)")) {
            // init commit
            println("Init $lastCommitId $currentCommitId $commitMessage")
            commit = Commit(currentCommitId, commitMessage)
        } else if (line.contains("commit")) {
            // commit
            println("Commit $lastCommitId $currentCommitId $commitMessage")
            commit = Commit(currentCommitId, lastCommitId, commitMessage)
        } else if (line.contains("merge")) {
            // merge from
            val mergeIndex = line.indexOf("merge")
            if (mergeIndex != -1) {
                val mergeName = line.substring(mergeIndex + "merge".length).trim { it <= ' ' }.split(":".toRegex())
                    .dropLastWhile { it.isEmpty() }
                    .toTypedArray()[0]
                println("Merge from $mergeName $lastCommitId $currentCommitId $commitMessage")
                commit = Commit(currentCommitId, lastCommitId, commitMessage, mergeName, true)
            }
        } else if (line.contains("branch: Created from")) {
            // created from
            val branchIndex = line.indexOf("branch: Created from")
            if (branchIndex != -1) {
                val branchName = line.substring(branchIndex + "branch: Created from".length).trim { it <= ' ' }
                println("Created from $branchName $lastCommitId $currentCommitId $commitMessage")
                commit = Commit(currentCommitId, lastCommitId, commitMessage, branchName)
            }
        }
        commit?.let { branch.addCommit(commit) }
        line = bufferedReader.readLine()
    }
    data.addBranch(branch)
    bufferedReader.close()
}


fun main() {
    val testPath = "C:/AndroidProjects/Begit/"
    val pathCommits = testPath.replace("\\", "/") + ".git/logs/refs/heads"
    val data = GitData()
    val folder = File(pathCommits)
    val files = folder.listFiles()
    for (file in files) {
        if (file.isFile) {
            val branch = Branch(file.name)
            val filePath = file.absolutePath.replace("\\", "/")
            createGraph(branch, data, filePath)
        }
    }
    data.makeFiles(testPath)
}