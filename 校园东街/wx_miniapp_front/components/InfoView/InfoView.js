import common from "../../utils/public"
// components/InfoView/InfoView.js
Component({
    /**
     * 组件的属性列表
     */
    properties: {
        myTitle:{
            type:String,
            value:''
        },
        myContent:{
            type:String,
            value:''
        },
        myUrl:{
            type:String,
            value:''
        },
        myImgUrl:{
            type:String,
            value:''
        }
    },

    /**
     * 组件的初始数据
     */
    data: {
        dataList: [{
            title: "这是一个标题",
            content: "这个一个内容"
        }]
    },

    
    /**
     * 组件的方法列表
     */
    methods: {

    }
})