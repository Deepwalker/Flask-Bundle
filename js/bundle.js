BundleAPI = new function(){
    this.build = function(apis) {
        var api
        var current_node
        var new_api = new Object()
        for (i in apis) {
            api = apis[i]
            current_node = new_api
            for (p in api.path) {
                node = api.path[p]
                if (!(node in current_node)) current_node[node] = new Object()
                current_node = current_node[node]
            }
            for (j in api.methods) {
                method = api.methods[j]
                current_node[method] = function (args) {
                        func = arguments.callee
                        return new_api.caller(func.api, method, args)
                    }
                current_node[method].api = api
            }
        }
        console.log(new_api)
        new_api.caller = this.defaultCaller
        return new_api
    }

    this.formatURL = function(url, args) {
        var iUrl = url
        for (a in args) {
            iUrl = iUrl.replace('{' + a + '}', args[a])
        }
        return iUrl
    }

    this.defaultCaller = function(api, method, args) {
        url = BundleAPI.formatURL(api.url, args)
        return $.ajax(url, {'method': method})
    }
}()
