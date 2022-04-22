var common = {
    getStrLen: function (str, len) {
        console.log(str)
        if (str.length > len) {
            return str.substr(0, len) + "..."
        } else {
            return str
        }
    },
}

module.exports = common