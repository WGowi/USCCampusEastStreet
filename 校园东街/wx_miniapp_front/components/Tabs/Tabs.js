//Component Object
Component({
  properties: {
    tabs: {
      type: Array,
      value: []
    }

  },
  data: {

  },
  methods: {
    handleItemTap(e) {
      // console.log(e)
      const {
        index
      } = e.currentTarget.dataset;
      // console.log(index)
      this.triggerEvent("tabsItemChange",{index})
    }
  },
  created: function () {

  },
  attached: function () {

  },
  ready: function () {

  },
  moved: function () {

  },
  detached: function () {

  },
});