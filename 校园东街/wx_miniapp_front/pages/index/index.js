//Page Object
Page({
  data: {
    lostData: [],
    foundData: [],
    // lostDetailUrl:[],
  },
  //options(Object)
  onLoad: function (options) {
    wx.request({
      url: 'http://IP:PORT/data/lost?page=1',
      data: {},
      header: {
        'content-type': 'application/json'
      },
      method: 'GET',
      dataType: 'json',
      responseType: 'text',
      success: (result) => {
        this.setData({
          lostData: result.data.data,
        })
      },
      fail: () => {},
      complete: () => {}
    });
    wx.request({
      url: 'http://IP:PORT/data/found?page=1',
      data: {},
      header: {
        'content-type': 'application/json'
      },
      method: 'GET',
      dataType: 'json',
      responseType: 'text',
      success: (result) => {
        this.setData({
          foundData: result.data.data
        })
      },
      fail: () => {},
      complete: () => {}
    });
  },

});