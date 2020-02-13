class EventBus {
    constructor() {
        this.subscriptions = {}
    }

    emit(id, data, ...args) {
        if (typeof this.subscriptions[id] == 'undefined') {
            return
        }

        for (const callback of this.subscriptions[id]) {
            callback(data, ...args)
        }
    }

    on(id, callback) {
        if (typeof this.subscriptions[id] == 'undefined') {
            this.subscriptions[id] = []
        }
        this.subscriptions[id].push(callback)
    }

    off(id, callback) {
        if (typeof this.subscriptions[id] == 'undefined') {
            return
        }

        if (callback == null) {
            delete this.subscriptions[id]
        } else {
            this.subscriptions[id].splice(
                this.subscriptions[id].indexOf(callback), 1
            )
        }
    }
}