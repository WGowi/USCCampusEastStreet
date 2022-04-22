// pages/search/search.js
Page({

    /**
     * 页面的初始数据
     */
    data: {
        kind: '',
        detail: []
    },

    onLoad: function (options) {
        // this.data.kind = options.kind
        // console.log(this.data.kind)
        this.setData({
            kind: options.kind
        })
    },

    handleInput(e) {
        const {
            value
        } = e.detail;
        if (!value.trim()) {
            return;
        }
        console.log(this.data.kind==0)
        if (this.data.kind == 0) {
            console.log('0')
            wx.request({
                url: 'http://IP:PORT/search/lost?context=' + value,
                data: {},
                header: {
                    'content-type': 'application/json'
                },
                method: 'GET',
                dataType: 'json',
                responseType: 'text',
                success: (result) => {
                    console.log(result)
                    this.setData({
                        detail: result.data.data
                    })
                },
                fail: () => {},
                complete: () => {}
            });
        } else if (this.data.kind == 1) {
            console.log('1')
            wx.request({
                url: 'http://IP:PORT/search/found?context=' + value,
                data: {},
                header: {
                    'content-type': 'application/json'
                },
                method: 'GET',
                dataType: 'json',
                responseType: 'text',
                success: (result) => {
                    this.setData({
                        detail: result.data.data
                    })
                },
                fail: () => {},
                complete: () => {}
            });
        } else {
            console.log('2')
            wx.request({
                url: 'http://IP:PORT/search/info?context=' + value,
                data: {},
                header: {
                    'content-type': 'application/json'
                },
                method: 'GET',
                dataType: 'json',
                responseType: 'text',
                success: (result) => {
                    this.setData({
                        detail: result.data.data
                    })
                },
                fail: () => {},
                complete: () => {}
            });
        }
    }
})