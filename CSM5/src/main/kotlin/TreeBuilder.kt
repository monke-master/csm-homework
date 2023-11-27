import guru.nidi.graphviz.attribute.Label
import guru.nidi.graphviz.attribute.Rank
import guru.nidi.graphviz.attribute.Rank.RankDir
import guru.nidi.graphviz.engine.Format
import guru.nidi.graphviz.engine.Graphviz
import guru.nidi.graphviz.model.Factory
import java.io.File
import java.io.IOException
import java.nio.file.Paths


class TreeBuilder {
    private var graph = Factory.graph().directed().graphAttr().with(Rank.dir(RankDir.TOP_TO_BOTTOM))

    fun addNode(
        id: String?,
        lastId: String?,
        branch: String?,
        lastBranch: String?,
        message: String?,
        lastMessage: String?
    ) {
        val parentNode = Factory.node(lastId)
            .with(
                Label.lines(
                    lastBranch,
                    lastMessage
                )
            )
        val newNode = Factory.node(id)
            .with(
                Label.lines(
                    branch,
                    message
                )
            )
        graph = graph.with(parentNode.link(newNode))
    }

    fun saveTree(filePath: String?) {
        try {
            val path = Paths.get(filePath)
            Graphviz.fromGraph(graph).render(Format.PNG).toFile(File(path.toString()))
            println("Tree saved to: " + path.toAbsolutePath())
        } catch (e: IOException) {
            System.err.println("Error: Unable to save the tree")
            e.printStackTrace()
        }
    }

    fun saveGraphvizTree(filePath: String?) {
        try {
            val path = Paths.get(filePath)
            Graphviz.fromGraph(graph).render(Format.DOT).toFile(File(path.toString()))
            println("Tree saved to: " + path.toAbsolutePath())
        } catch (e: IOException) {
            System.err.println("Error: Unable to save the tree")
            e.printStackTrace()
        }
    }
}
