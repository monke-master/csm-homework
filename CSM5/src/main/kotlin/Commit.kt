class Commit {
    var type // init, newbranch, merge, commit
            : String
        private set
    var branchFrom: String? = null
        private set
    var mergeFrom: String? = null
        private set
    var message: String
        private set
    var id: String
        private set
    var lastId: String? = null
        private set

    constructor(id: String, message: String) {
        type = "init"
        this.id = id
        this.message = message
    }

    constructor(id: String, lastId: String?, message: String) {
        type = "commit"
        this.id = id
        this.lastId = lastId
        this.message = message
    }

    constructor(id: String, lastId: String?, message: String, branchFrom: String?) {
        type = "newbranch"
        this.id = id
        this.lastId = lastId
        this.message = message
        this.branchFrom = branchFrom
    }

    constructor(id: String, lastId: String?, message: String, mergeFrom: String?, merge: Boolean) {
        type = "merge"
        this.id = id
        this.lastId = lastId
        this.message = message
        this.mergeFrom = mergeFrom
    }
}

