Page({
    data: {
        disciplineArray: ['(01)哲学', '(02)经济学', '(03)法学', '(04)教育学', '(05)文学', '(06)历史学', '(07)理学', '(08)工学', '(09)农学', '(10)医学', '(11)军事学', '(12)管理学', '(13)艺术学', '(14)交叉学科', '(zyxw)专业学位'],
        objectDisciplineArray: [{
                id: 0,
                name: '(01)哲学'
            },
            {
                id: 1,
                name: '(02)经济学'
            },
            {
                id: 2,
                name: '(03)法学'
            },
            {
                id: 3,
                name: '(04)教育学'
            },
            {
                id: 4,
                name: '(05)文学'
            },
            {
                id: 5,
                name: '(06)历史学'
            },
            {
                id: 6,
                name: '(07)理学'
            },
            {
                id: 7,
                name: '(08)工学'
            },
            {
                id: 8,
                name: '(09)农学'
            },
            {
                id: 9,
                name: '(10)医学'
            },
            {
                id: 10,
                name: '(11)军事学'
            },
            {
                id: 11,
                name: '(12)管理学'
            },
            {
                id: 12,
                name: '(13)艺术学'
            },
            {
                id: 13,
                name: '(14)交叉学科'
            },
            {
                id: 14,
                name: '(zyxw)专业学位'
            },
        ],
        disciplineIndex: 0,
        subjectArray: [],
        subjectIndex: 0,
    },
    bindDisciplineChange: function (e) {
        console.log('picker发送选择改变，携带值为', e.detail.value)
        this.setData({
            disciplineIndex: e.detail.value,
            subjectIndex: 0
        })
        this.getSubject(e.detail.value)
    },

    bindSubjectChange: function (e) {
        console.log('picker发送选择改变，携带值为', e.detail.value)
        this.setData({
            subjectIndex: e.detail.value
        })
    },

    bindDownloadFile: function (e) {
        wx.downloadFile({
            url: 'http://IP:PORT/data/subject/detail?mldm=' + this.data.disciplineIndex + '&yjxkdm=' + this.data.subjectIndex,
            success: (result) => {
                console.log('success')
                console.log(this.data.subjectIndex)
                console.log(this.data.disciplineIndex)
                if (result.statusCode === 200) {
                    wx.openDocument({
                        filePath: result.tempFilePath,
                        fileType: 'xlsx',
                        showMenu: true,
                        success: (result) => {
                            console.log('open file')
                        },
                        fail: () => {},
                        complete: () => {}
                    });
                }
            },
            fail: () => {},
            complete: () => {}
        });
    },

    onLoad: function (options) {
        this.getSubject(0)
    },

    getSubject: function (id) {
        wx.request({
            url: 'http://IP:PORT/data/subject?id=' + id,
            data: {},
            header: {
                'content-type': 'application/json'
            },
            method: 'GET',
            dataType: 'json',
            responseType: 'text',
            success: (result) => {
                let myarray = new Array()
                for (let index = 0; index < result.data.data.length; index++) {
                    myarray.push(result.data.data[index].subject)
                }
                this.setData({
                    subjectArray: myarray
                })
                // console.log(this.subjectArray)
            },
            fail: () => {},
            complete: () => {}
        });
    }

})