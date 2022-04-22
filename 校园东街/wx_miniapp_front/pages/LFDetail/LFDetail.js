// pages/LFDetail/LFDetail.js
Page({

    /**
     * 页面的初始数据
     */
    data: {
        detail: [],
        kind:''
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function (options) {
        var kind = options.kind
        var id = options.id
        console.log(options.kind)
        // var kind = 1
        // var id = 1
        var url
        if (kind == 0) {
            url = 'http://IP:PORT/data/lostdetail?id=' + id
        } else {
            url = 'http://IP:PORT/data/founddetail?id=' + id
        }
        console.log(url)
        wx.request({
            // if (kind===1){}
            url: url,
            data: {},
            header: {
                'content-type': 'application/json'
            },
            method: 'GET',
            dataType: 'json',
            responseType: 'text',
            success: (result) => {
                // console.log(result)
                this.setData({
                    detail: result.data.data[0],
                    kind
                })
            },
            fail: () => {},
            complete: () => {}
        });
    },

    clickImg() {
        wx.previewImage({
            current: this.data.detail.img_url,
            urls: [this.data.detail.img_url],
            success: (result) => {

            },
            fail: () => {},
            complete: () => {}
        });
    },
    
    /**
     * 生命周期函数--监听页面初次渲染完成
     */
    onReady: function () {

    },

    /**
     * 生命周期函数--监听页面显示
     */
    onShow: function () {

    },

    /**
     * 生命周期函数--监听页面隐藏
     */
    onHide: function () {

    },

    /**
     * 生命周期函数--监听页面卸载
     */
    onUnload: function () {

    },

    /**
     * 页面相关事件处理函数--监听用户下拉动作
     */
    onPullDownRefresh: function () {

    },

    /**
     * 页面上拉触底事件的处理函数
     */
    onReachBottom: function () {

    },

    /**
     * 用户点击右上角分享
     */
    onShareAppMessage: function () {

    }
})