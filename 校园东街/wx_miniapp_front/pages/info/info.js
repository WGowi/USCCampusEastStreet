//Page Object
Page({
  data: {
    tabs: [{
      id: 0,
      value: '寻物启事',
      isActive: true
    }, {
      id: 1,
      value: '招领启事',
      isActive: false
    }, {
      id: 2,
      value: '校园资讯',
      isActive: false
    }],
    cur_index: 0,
    search_url: '/pages/search/search?kind=0',
    lostData: [],
    cur_lost_page: 1,
    lost_total_page: 0,
    foundData: [],
    cur_found_page: 1,
    found_total_page: 0,
    infoData: [],
    cur_info_page: 1,
    info_total_page: 0,
  },
  //options(Object)
  onLoad: function (options) {
    this.getLostList()
    this.getFoundList()
    this.getInfoList()
  },

  handleTabsItemChange(e) {
    // console.log(e)
    const {
      index
    } = e.detail;
    let {
      tabs
    } = this.data;
    let {
      search_url
    } = this.data;
    tabs.forEach((v, i) => i === index ? this.data.cur_index = v.id : v.isActive = false);
    tabs[this.data.cur_index].isActive = true;
    search_url = '/pages/search/search?kind=' + this.data.cur_index
    this.setData({
      tabs,
      search_url
    })
  },

  getLostList() {
    wx.request({
      url: 'http://IP:PORT/data/lost?page=' + this.data.cur_lost_page,
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
          lostData: [...this.data.lostData, ...result.data.data],
          cur_lost_page: this.data.cur_lost_page + 1,
          lost_total_page: result.data.total_page
        })
      },
      fail: () => {},
      complete: () => {}
    });
  },

  getFoundList() {
    wx.request({
      url: 'http://IP:PORT/data/found?page=' + this.data.cur_found_page,
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
          foundData: [...this.data.foundData, ...result.data.data],
          cur_found_page: this.data.cur_found_page + 1,
          found_total_page: result.data.total_page
        })
      },
      fail: () => {},
      complete: () => {}
    });
  },

  getInfoList() {
    wx.request({
      url: 'http://IP:PORT/data/info?page=' + this.data.cur_info_page,
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
          infoData: [...this.data.infoData, ...result.data.data],
          cur_info_page: this.data.cur_info_page + 1,
          info_total_page: result.data.total_page
        })
      },
      fail: () => {},
      complete: () => {}
    });
  },

  onReachBottom() {
    if (this.data.tabs[0].isActive === true) {
      if (this.data.cur_lost_page < this.data.lost_total_page) {
        this.getLostList()
      } else {
        wx.showToast({
          title: '页面加载完成',
          icon: 'none',
          image: '',
          duration: 1500,
          mask: false,
          success: (result) => {

          },
          fail: () => {},
          complete: () => {}
        });
      }
    }
    if (this.data.tabs[1].isActive === true) {
      if (this.data.cur_found_page < this.data.found_total_page) {
        this.getFoundList()
      } else {
        wx.showToast({
          title: '页面加载完成',
          icon: 'none',
          image: '',
          duration: 1500,
          mask: false,
          success: (result) => {

          },
          fail: () => {},
          complete: () => {}
        });
      }
    }
    if (this.data.tabs[2].isActive === true) {
      if (this.data.cur_info_page < this.data.info_total_page) {
        this.getInfoList()
      } else {
        wx.showToast({
          title: '页面加载完成',
          icon: 'none',
          image: '',
          duration: 1500,
          mask: false,
          success: (result) => {

          },
          fail: () => {},
          complete: () => {}
        });
      }
    }
  }

});