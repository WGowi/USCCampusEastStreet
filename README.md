# USCCampusEastStreet
一个采用scrapy爬虫以Django为后端的微信小程序

[toc]

# 第一章 系统概要分析

在上一章完成的相关技术介绍上，在这章中本文我们将会对以上提到的方面，做出更加详细可行的解决方案，这一章主要的内容是对爬虫系统、后端Django以及前端微信小程序的概要设计，主要是从设计原则及目标、体系结构、功能结构和数据库设计上来介绍了系统的整体架构。

（先介绍总体框架，再分部介绍每个的功能）

## 1.1 系统总体设计

### 1.1.1 系统组成部分分析

![img](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202204222323710.jpg)

图 三.1系统总体架构图

### 1.1.2 系统运行流程

对系统工作流程进行如下分析：

\1.  首先Django后端通过ORM对象关系映射形成响应的数据库表

\2.  Scrapy爬虫通过连接相对应的数据库，往表中添加响应的数据

\3.  Django后端的Admin面板可以对scrapy爬虫添加的数据进行管理

\4.  前端微信小程序通过发送request请求给Django后端，Django后端响应来自前端的请求，并获得其携带的相关参数，向数据库中请求相关信息

\5.  数据库接受来自后端的请求，并返回响应的数据

\6.  Django后端接受来自数据库的数据，并转化为相应的格式发送给微信小程序

\7.  微信小程序得到相应的数据后，渲染页面并显示相关信息

 

## 1.2 爬虫总体设计介绍

### 1.2.1 爬取对象简介

本文实现的爬虫以南华大学阳光教育服务大厅的教育阳光信息列表清单模块（http://nhedu.tabbyedu.com/column/lbqd/index.shtml）以及失物招领模块（http://nhedu.tabbyedu.com/column/swlt/index.shtml）以及中国研究生招生信息网的硕士目录模块（https://yz.chsi.com.cn/zsml/zyfx_search.jsp）作为爬取对象，爬取教育阳光信息列表清单模块的每一个帖子的ID、标题、内容、类别、部门、回复、身份以及附件图片；爬取失物招领模块的ID、标题、细节描述、联系人、联系方式、拾取或遗失时间、拾取或遗失地点、招领地点；爬取硕士目录的学校名称、学校所在地、招生院系、招生人数、考试科目、研究方向、指导老师、学科门类、学科类别、学习方式、招生专业、是否自划线、是否拥有研究生院、是否拥有博士点。

南华大学阳光教育服务大厅是南华大学关于学生生活的一个平台，作为爬取对象有着立足本校的意义，同时南华大学阳光教育服务大厅是采用动态加载的、有着才用js下载等反爬虫措施中国研究生招生信息网的硕士目录则有着IP检测等反爬虫措施，而这将帮助我们更加细致的了解爬虫与反反爬的工作原理和流程。

 

### 1.2.2  爬虫总体架构设计

本文将爬虫分为三个模块即网页信息抓取模块、中间件模块以及数据处理模块。

网页信息抓取模块首先根据定义的URL地址分析网页element结构，在根据开发者定义的xpath来提取相关字段。

中间件模块，通过User-Agent伪装，代理IP等技术实现反反爬。

数据处理模块将对爬虫爬取的数据进行相关处理，然后在mysql数据库中实现持久化存储。

 

## 1.3 Django后端总体设计介绍

### 1.3.1 ORM对象关系映射设计

Django可以通过ORM对象关系映射把继承自models.Model的python类映射成数据库中的表，把类内属性映射为数据中的字段,并且Django为ORM提供了相应的数据类型如CharField即可映射为mysql中的varchar。这样使得开发者在程序设计时更加关注类的本身，而非数据库。极大了提高了程序的可移植性。降低了程序与数据库的耦合性。

同时类内属性的设计也更爬虫爬取的字段相关，要根据scrapy爬虫中的items.py定义的scrapy.Field()来设计模型类。

 

### 1.3.2 View视图设计

Django框架中View视图主要负责数据逻辑的处理，数据接口的实现，同时与Template模版类以前实现界面的显示[27]。而本文中使用了微信小程序作为前端，使用View主要对其数据接口的实现。其目的是为了响应来自前端的request请求。

View主要为前端提供了获取失物招领的信息、获取寻物启事的信息、获取校园资讯、对寻物启事内容进行搜索，对失物招领信息进行搜索、对校园资讯进行搜索、获取学科类别与学科门类的信息，导出考研院校信息。

同时通过urls.py,把相应的URL地址与其视图进行绑定。即可以通过url对视图的发生访问请求。

 

### 1.3.3 admin面板设计 

Django为数据库管理员提供了可视化的数据库管理面板，可以对数据库中数据进行操作。

开发者只需要在admin.py中设计继承自admin.ModelAdmin的类，并且将模型类与其进行绑定即可，快速便捷。

## 1.4 微信小程序总体设计介绍

### 1.4.1 微信小程序功能设计

微信小程序主要是负责前端界面的显示，微信小程序界面主要分为主页、广场页、考研信息页、搜索页、详情页、客服页等。

且微信小程序通过发送request请求给后端，后端响应来自微信小程序的request请求并返回其相关数据

 

### 1.4.2 微信小程序界面设计

其主页、广场页、考研信息页、搜索页、详情页、客服页各界面的作用如下：

(1).  主页主要负责显示最近发布的五条失物招领与寻物启事，点击即可跳转到相应的详情页。

(2).  广场页可以分别显示失物招领、寻物启事、以及校园资讯并支持下拉式刷新，并且为其提供相应的搜索服务，同时支持跳转到相应的详情页。

(3).  考研信息页主要是负责对发送请求获取excel格式相应的考研信息。

(4).  搜索页支持对失物招领、寻物启事、以及校园资讯进行模糊式搜索，并且支持点击跳转详情页。

(5).  详情页支持对失物招领、寻物启事、以及校园资讯详细信息的显示。

(6).  客服页主要负责与客服的对话

 

## 1.4 系统概要

### 1.4.1 系统组成部分分析

![img](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202204222323710.jpg)

图 3.1 系统总体架构图

### 1.4.1系统运行流程

对系统工作流程进行如下分析：

1.   首先Django后端通过ORM对象关系映射形成响应的数据库表

1.   Scrapy爬虫通过连接相对应的数据库，往表中添加响应的数据

1.   Django后端的Admin面板可以对scrapy爬虫添加的数据进行管理

1.   前端微信小程序通过发送request请求给Django后端，Django后端响应来自前端的请求，并获得其携带的相关参数，向数据库中请求相关信息

1.   数据库接受来自后端的请求，并返回响应的数据

1.   Django后端接受来自数据库的数据，并转化为相应的格式发送给微信小程序

1.   微信小程序得到相应的数据后，渲染页面并显示相关信息



 

# 第二章 系统的详细设计与实现

在上一章系统概要设计的基础上，本章主要介绍系统的详细设计，以及实现原理，主要从怎么设计爬虫字段到ORM的对象关系映射，从爬虫字段的提取到数据库的存储。

 

## 2.1 scrapy爬虫详细设计

### 2.1.1 网页爬取策略的设计

网络爬虫的主要任务是在互联网中爬行，下载目标网页的内容。本文主要采用深度优先搜索[28]作为爬虫爬取策略。爬虫首先从spider目录下获得初始的URL地址。其中本文我们以研招网硕士目录（https://yz.chsi.com.cn/zsml/queryAction.do）为例来分析可知，浏览器对网页发送post请求并且携带参数如下：

 

 

表 四.1研招网硕士目录post请求发送数据分析

| 表单数据 | 含义         | 示例     | 示例含义 |
| -------- | ------------ | -------- | -------- |
| ssdm     | 省市代码     | 43       | 湖南省   |
| dwmc     | 单位名称     | 南华大学 | 南华大学 |
| mldm     | 门类代码     | 08       | 工学     |
| yjxkdm   | 研究学科代码 | 0835     | 软件工程 |
| zymc     | 专业名称     | 软件工程 | 软件工程 |
| xxfs     | 学习方式     | 1        | 全日制   |

表 4.1 研招网硕士目录post请求发送数据分析

 

分析网页的element结构。提取相关字段并存入item中。同时爬虫通过爬取获取网页的详情页以及下一页的链接，进行详情页的爬取以及翻页操作。

![img](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202204222323742.jpg)

图 四.1研招网学校页的href

图4.1研招网学校页的href

 

如图4.1所示我们可以通过利用response.xpath(‘//tbody/tr//a/@href’)来对具体学校的URL地址进行提取。同理我们可以对下一页的操作进行分析可以得知只需要携带一个pageno参数即可完成翻页操作。

通过抓取网页信息后，我的得到了相关字段，并我们要放入数据库中进行持久化存储，这里本文我们引入mysql，首先我们在itempipelines.py中获得我们的item，然后通过open_spider对数据进行连接，这里本文连接数据库选用的是pymysql。然后在process_item中通过编写sql语句将数据保存于数据库中，最后通过close_spider来关闭于数据库的连接。

### 2.1.2 动态网页的处理

南华大学阳光教育服务大厅网站主要采用js动态渲染来防止恶意爬虫。

Scrapy是现在十分流行的爬虫框架，但是他有其不足之处，即Scrapy没有Javascript engine, 因此它无法爬取JavaScript生成的动态网页，只能爬取静态网页，而在现代大部分网页都会采用JavaScript来丰富网页的功能。所以，这无疑Scrapy的遗憾之处。所以本文决定使用scrapy-splash模块。Splash是一个就是一个Javascript渲染服务。它是一个实现了HTTP API的轻量级浏览器，Splash是用Python实现的，同时使用Twisted和QT[29]。Twisted（QT）用来让服务具有异步处理能力，以发挥webkit的并发能力。其实scrapy也是一个基于Twisted的网络爬虫框架。两者结合更能发挥其Twisted的异步能力

为了在scrapy中引用Splash服务，我们首先要在docker上安装splash，并且开启splash服务。然后在终端中执行pip install scrapy-splash，为其安装支持splash的第三方库。最后在settings.py中为配置splash的URL地址并其开启下载中间件与爬虫中间件。

 

SPLASH_URL = 'http://192.168.59.103:8050'

 

SPIDER_MIDDLEWARES = {

  'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,

}

DOWNLOADER_MIDDLEWARES = {

  'scrapy_splash.SplashCookiesMiddleware': 723,

  'scrapy_splash.SplashMiddleware': 725,

  'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,

}

其中scrapy可以通过调用scrapy-splash提供的SplashRequest来实现对网页的动态渲染。

SplashRequest(

​      url=url,

​      callback=self.parse,

​      args={"wait": 10},

​      endpoint="render.html",

​    )

在南华大学阳光教育服务大厅网站失物招领模块已经无法通过分析href获取下一页的URL地址

![img](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202204222323914.jpg)

图 四.2南华大学阳光教育服务大厅网站失物招领模块下一页的html结构

图 4.2南华大学阳光教育服务大厅网站失物招领模块下一页的html结构

 

开发者我们可以通过编写Lua脚本实现对浏览器的模拟点击操作

next_page_lua_script = """

​        function main(splash, args)

​         assert(splash:go(args.url))

​         assert(splash:wait(0.5))

​         splash:runjs(args.script)

​         assert(splash:wait(0.5))

​         return splash:html()

​        end

​        """

### 2.1.3 javaScript逆向分析

当爬虫我们抓取网页端数据时，经常被加密参数、加密数据所困扰，如何快速定位这些加解密函数，尤为重要。当我们进入失物招领的详情页时，就会发现有些帖子提供了下载附近的功能。同样文件的URL地址是用JavaScript提供的。一般有两种方式来实现文件的下载，其中一种是通过自动化测试脚本selenium来模拟浏览器操作实现。此操作往往需要符合浏览器版本的webdriver来驱动，而且为保持性会话操作，虽然实现起来比较简单，但是往往效率比较低。这里本文选用JavaScript逆向分析来获取的文件所在的URL地址[30]。

![img](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202204222323920.jpg)

图 四.3南华大学阳光教育服务大厅网站失物招领模块详情页附件的html结构

图 4.3南华大学阳光教育服务大厅网站失物招领模块详情页附件的html结构

 

但是当完成JavaScript逆向操作时，获得到的文件的URL是经过加密处理的而且是一次性使用的。这里本文我们引入阿里云的oss对象存储技术，本文使用正则表达式来对文件种类进行判断并获取帖子的唯一ID，当附近为图片时，将文件重新命名为帖子的ID，并将将文件下载转存至阿里云中实现文件的持久化存储。同时阿里云也为开发者我们提供了相应的URL来地址来访问相应我们的文件。

### 2.1.4 User-Agent伪装与IP代理

很多网站都有相应的反爬虫措施，本文主要采用随机User-Agent来实现User-Agent伪装，因为scrapy本身提供的User-Agent为固定的格式很容易被网站识别为恶意爬虫，首先本文先建立了一个User-Agent池，然后利用python库random在其中进行随机选择，从而实现随机User-Agent伪装。同样的当一个IP对网站请求多次的时候，网站也会认为这是一个恶意爬虫，从而对此IP实现封禁操作。本文引用快代理的隧道IP代理，从而实现IP代理，使得每次发送请求是改变IP。并且在scrapy的settings.py中开启相应的中间件。

1.1  

 

## 2.2 Django后端详细设计

### 2.2.1 ORM对象关系映射的设计

由于Django为开发者提供了models.Model的python类到数据库的映射操作所以我们只需要完成对models.Model的python类实现即可。本文主要实现了以下五个模型类，并完成了对数据库映射操作形成了相应的数据库表。（这里不要用表来表示，用ER图来表示）

![img](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202204222323922.jpg)

图 四.4Lost类图

![img](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202204222323923.jpg)

图 四.5Lost ER图

 

![img](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202204222323382.jpg)

图 四.6Found类图

 

![img](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202204222323516.jpg)

图 四.7Found ER图

![img](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202204222323551.jpg)

图 四.8YZW类图

![img](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202204222323558.jpg)

图 四.9YZW ER图

 

![img](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202204222323557.jpg)

图 四.10SubjectInfo类图

 

![img](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202204222323570.jpg)

图 四.11Subject ER图

 

| 属性                 | 数据类型        | 最大长度 | 是否为空 | 映射字段             | 映射数据类型 | 备注         |
| -------------------- | --------------- | -------- | -------- | -------------------- | ------------ | ------------ |
| id                   | BigIntegerField |          | 否       | id                   | Bigint       | 主键，帖子ID |
| title                | CharField       | 100      | 否       | title                | Varchar(100) | 标题         |
| description          | TextField       |          | 否       | description          | Text         | 描述         |
| contact              | CharField       | 100      | 否       | contact              | Varchar(100) | 联系人       |
| tel                  | CharField       | 11       | 否       | tel                  | Varchar(11)  | 联系方式     |
| find_or_lost_address | CharField       | 100      | 否       | find_or_lost_address | Varchar(100) | 遗失地点     |
| find_or_lost_time    | CharField       | 100      | 否       | find_or_lost_time    | Varchar(100) | 遗失时间     |
| black_address        | CharField       | 100      | 否       | black_address        | Varchar(100) | 招领地点     |
| public_time          | CharField       | 100      | 否       | public_time          | Varchar(100) | 发布日前     |
| img_url              | CharField       | 100      | 否       | img_url              | Varchar(100) | 图片URL      |

表 4.2 Lost模型类与Lost表

 

 

| 属性                 | 数据类型        | 最大长度 | 是否为空 | 映射字段             | 映射数据类型 | 备注         |
| -------------------- | --------------- | -------- | -------- | -------------------- | ------------ | ------------ |
| id                   | BigIntegerField |          | 否       | id                   | Bigint       | 主键，帖子ID |
| title                | CharField       | 100      | 否       | title                | Varchar(100) | 标题         |
| description          | TextField       |          | 否       | description          | Text         | 描述         |
| contact              | CharField       | 100      | 否       | contact              | Varchar(100) | 联系人       |
| tel                  | CharField       | 11       | 否       | tel                  | Varchar(11)  | 联系方式     |
| find_or_lost_address | CharField       | 100      | 否       | find_or_lost_address | Varchar(100) | 拾取地点     |
| find_or_lost_time    | CharField       | 100      | 否       | find_or_lost_time    | Varchar(100) | 拾取时间     |
| black_address        | CharField       | 100      | 否       | black_address        | Varchar(100) | 招领地点     |
| public_time          | CharField       | 100      | 否       | public_time          | Varchar(100) | 发布日前     |
| img_url              | CharField       | 100      | 否       | img_url              | Varchar(100) | 图片URL      |

 

表 4.2 Found模型类与Found表

 

| 属性        | 数据类型     | 最大长度 | 是否为空 | 映射字段   | 映射数据类型 | 备注         |
| ----------- | ------------ | -------- | -------- | ---------- | ------------ | ------------ |
| id          | IntegerField |          | 否       | id         | int          | 主键，帖子ID |
| title       | CharField    | 100      | 否       | title      | Varchar(100) | 标题         |
| kind        | CharField    | 100      | 否       | kind       | Varchar(100) | 种类         |
| department  | CharField    | 100      | 否       | department | Varchar(100) | 部门         |
| public_time | CharField    | 100      | 否       | pulic_time | Varchar(100) | 发布时间     |
| content     | TextField    |          | 否       | content    | text         | 内容         |
| reply       | TextField    |          | 否       | reply      | Varchar(100) | 回复         |
| identity    | CharField    | 100      | 否       | identity   | Varchar(100) | 身份         |
| img_url     | CharField    | 100      | 否       | img_url    | Varchar(100) | 图片URL      |

表 4.3 Info模型类与Info表

 

| 属性       | 数据类型        | 最大长度 | 是否为空 | 映射字段   | 映射数据类型 | 备注     |
| ---------- | --------------- | -------- | -------- | ---------- | ------------ | -------- |
| id         | BigIntegerField |          | 否       | id         | bigint       | 主键     |
| discipline | CharField       | 100      | 否       | discipline | Varchar(100) | 学科门类 |
| subject    | CharField       | 100      | 否       | subject    | Varchar(100) | 学科类别 |

表 4.3 SubjectInfo模型类与Subject Info表

 

| 属性               | 数据类型        | 最大长度 | 是否为空 | 映射字段           | 映射数据类型 | 备注     |
| ------------------ | --------------- | -------- | -------- | ------------------ | ------------ | -------- |
| id                 | BigIntegerField |          | 否       | id                 | int          | 主键     |
| School             | CharField       | 100      | 否       | School             | Varchar(100) | 学校     |
| Place              | CharField       | 100      | 否       | Place              | Varchar(100) | 所在地   |
| Graduate_School    | CharField       | 100      | 否       | Graduate_School    | Varchar(100) | 研究生院 |
| Self_Scribing      | CharField       | 100      | 否       | Self_Scribing      | Varchar(100) | 自划线   |
| PhD                | CharField       | 100      | 否       | PhD                | Varchar(100) | 博士点   |
| Disciplines        | CharField       | 100      | 否       | Disciplines        | Varchar(100) | 学科门类 |
| Subject_Category   | CharField       | 100      | 否       | Subject_Category   | Varchar(100) | 学科类别 |
| Major              | CharField       | 100      | 否       | Major              | Varchar(100) | 专业     |
| College            | CharField       | 100      | 否       | College            | Varchar(100) | 学院     |
| Research_Direction | CharField       | 100      | 否       | Research_Direction | Varchar(100) | 研究方向 |
| Learning_Style     | CharField       | 100      | 否       | Learning_Style     | Varchar(100) | 学习方式 |
| Instructor         | CharField       | 100      | 否       | Instructor         | Varchar(100) | 导师     |
| Number             | CharField       | 100      | 否       | Number             | Varchar(100) | 招生人数 |
| Remarks            | TextField       |          | 否       | Remarks            | Text         | 备注     |
| Lesson1            | CharField       | 100      | 否       | Lesson1            | Varchar(100) | 科目一   |
| Lesson2            | CharField       | 100      | 否       | Lesson2            | Varchar(100) | 科目二   |
| Lesson3            | CharField       | 100      | 否       | Lesson3            | Varchar(100) | 科目三   |
| Lesson4            | CharField       | 100      | 否       | Lesson4            | Varchar(100) | 科目四   |

表 4.4 YZW模型类与YZW表

 

当每次对数据库进行修改时，都只需要对Django中的模型类进行操作，然后执行迁移操作即可。迁移是Django 将你对模型的修改（例如增加一个字段，删除一个模型）应用至数据库架构中的方式。它们被设计的尽可能自动化。

 

### 2.2.2 Django数据接口的设计

Django通过在 Django 框架中，视图是接收 Web 请求并返回 Web 响应的 Python 函数或类。响应可以是简单的 HTTP 响应、HTML 模板响应或将用户重定向到另一个页面的 HTTP 重定向响应。视图包含将信息作为响应以任何形式返回给用户所需的逻辑。作为最佳实践，处理视图的逻辑保存在views.py的Django 应用程序的文件中。

本文主要采用Json作为返回信息，其定义的视图类与相应的URL进行绑定，可以通过访问相应的URL来发送请求。

表 四.2 Django后端返回信息与URL绑定情况

| URL地址             | 携带参数                               | 绑定视图           | 返回类型 | 描述                                              |
| ------------------- | -------------------------------------- | ------------------ | -------- | ------------------------------------------------- |
| data/yzw            | n:请求页码  yjxkmd:研究学科代码        | getYZWData         | json     | 以每页25条信息的格式返回第n页考研信息             |
| data/lost           | page:请求页码                          | getLostData        | json     | 以每页5条信息的格式按最新时间次序返回寻物启事信息 |
| data/found          | page:请求页码                          | getFoundData       | json     | 以每页5条信息的格式按最新时间次序返回失物招领信息 |
| data/info           | page:请求页码                          | getInfoData        | json     | 以每页5条信息的格式按最新时间次序返回校园资讯信息 |
| data/lostdetail     | id:帖子id                              | getLostDetailInfo  | json     | 返回寻物启事具体帖子信息                          |
| data/founddetail    | id:帖子id                              | getfoundDetailInfo | json     | 返回失物招领具体帖子信息                          |
| data/infodetail     | id:帖子id                              | getInfoDetailInfo  | json     | 返回校园资讯具体帖子信息                          |
| data/subject        | id:学科门类代码                        | getSubjectInfo     | json     | 返回学科门类与学科类别配对信息                    |
| data/subject/detail | mldm:学科门类代码  yjxkdm:研究学科代码 | getYZWDetail       | xlxs     | 返回具体考研信息                                  |
| search/lost         | context：搜索内容                      | searchLost         | json     | 返回搜索到的寻物启事信息                          |
| search/found        | context：搜索内容                      | searchFound        | json     | 返回搜索到的失物招领信息                          |
| search/info         | context：搜索内容                      | searchInfo         | json     | 返回搜索到的校园资讯信息                          |

表 4.5 Django后端返回信息与URL绑定情况

 

## 2.3 微信小程序详细设计

### 2.3.1  用户界面设计

微信小程序主要由三部分组成分别是首页、广场页以及考研信息页。

微信小程序主页主要由四部分组成分别为轮播图，最近遗失、最近拾取以及联系客服。其中最近遗失与最近拾取展示最近五条信息并且点击就可以跳转到相应的详情页。

广场页则由搜索栏，Tab标签页以及滚动信息栏组成。Tab页分为三部分分别为寻物启事、失物招领以及校园资讯，点击就可以在三者中实现自由切换。点击寻物启事则下边滚动信息栏显示的为寻物启事信息且为动态加载的形式实现，每次当信息触底时，微信小程序会自动加载出后五条信息。同时点击搜索栏，则会跳转进入到搜索页，搜索与Tab栏中选中标签一致的内容，并实现变输入变动态加载，同时点击其搜索结果就会跳转进入详情页，详情页显示相关的信息以及图片。

考研信息页主要由两个下拉框组成，第一个为学科门类，第二个则为学科类别，其中学科类别的显示由学科门类所决定，并支持下载其文件。

 

### 2.3.2 网络请求设计

在微信小程序端，每一个page页面或者component组件都有一个以js结尾的JavaScript文件来控制页面的交互，JavaScript可以使得微信小程序拥有动态式交互能力。

![img](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202204222323915.jpg)

图 四.12Tab标签栏

图4.4 Tab标签栏

 

如上图4.4所示，Tab标签可以实现三种类别的自由切换。同时使得下方滚动信息栏的内容与Tab标签栏选中内容保持一致，其中每一个Tab栏的标签页的URL也各不相同。

同时在微信小程序中通过调用wx.request(Object object)访问开发者提供的URL地址从而实现访问服务器获取相关数据的目的。同时该API只支持对json文件的解析工作。所以Django后端主要返回的数据为json文件。

为了实现文件的下载，微信官方为其设计了一个wx.downloadFile(Object object)API接口。其主要功能是下载文件资源到本地。客户端直接发起一个 HTTPS GET 请求，返回文件的本地临时路径 (本地路径)，单次下载允许的最大文件为 200MB。由此我们可以通过相应的URL发送下载文件的请求，并且将文件保存到本地临时路径中。然后通过wx.openDocument（Object object）API来打开下载下来的文件。

![img](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202204222323009.jpg)

图 四.13微信小程序网络分析图

 

图4.5 微信小程序网络分析图

 

# 第三章 系统总体结构分析以及运行情况

在上一章中文本已经详细地介绍了系统的详细设计与实现思路，在这一章，本文着重介绍各子系统的运行情况以及结构。

## 3.1 爬虫系统

### 3.1.1 YZW爬虫运行结果展示

执行YZW爬虫可见spider会从网页上抓取相应的字段，并转换为sql语句存入数据库中![img](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202204222323143.jpg)

图 五.1爬虫YZW运行情况

图5.1 爬虫YZW运行情况![img](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202204222323149.jpg)

图 五.2数据库表YZW截图

图5.2 数据库表YZW截图

 

### 3.1.2 Lost_and_found爬虫运行结果展示

在docker中开启splash服务，并执行Lost_and_found爬虫。

![img](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202204222323151.jpg)

图 五.3爬虫Lost_and_found运行情况

图5.3 爬虫Lost_and_found运行情况

可见爬虫通过splash服务实现了对动态网页的字段提取，同时应用JavaScript逆向分析的方法成功获得了图片的URL路径，若不存在图片则使用默认图片，并存储在阿里云的oss对象存储中，又通过执行sql语句把数据放入mysql中做持久化存储。

![img](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202204222323153.jpg)

图 五.4阿里云oss对象存储情况

图5.4 阿里云oss对象存储情况

![img](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202204222323317.jpg)

图 五.5数据库表Lost截图

图5.5 数据库表Lost截图

![img](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202204222323624.jpg)

图 五.6爬虫complaint运行情况

图5.6 爬虫complaint运行情况

![img](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202204222323762.jpg)

图 五.7数据库表Info截图

图5.7数据库表Info截图

## 3.2 Django 后端系统

### 3.2.1 Django ORM对象关系映射

当进入Django项目目录时，执行python3 manage.py makemigrations与python3 manage.py migrate命令，可知Django通过对象关系映射把继承自models.Model的类映射成数据库中的表。

![img](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202204222323798.jpg)

图 五.8Django模型类

 

图5.8 Django模型类![img](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202204222323799.jpg)

图 五.9 Django通过ORM映射数据库

图5.9 Django通过ORM映射数据库

### 3.2.2 视图访问

浏览器可以通过视图与之绑定的url来访问相关视图，并可以通过携带参数的形式来访问视图中的特定内容![img](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202204222323818.jpg)

图 五.10lost视图

图5.10 lost视图![img](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202204222323871.jpg)

图 五.11在lost数据库中搜索身份证

图5.11在lost数据库中搜索身份证

![img](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202204222323152.jpg)

图 五.12下载0812计算机科学与技术

图5.12 下载0812计算机科学与技术

### 3.2.3 admin面板

在Django项目目录时，执行python3 manage.py createsuperuser命令，便会注册超级管理员用户。就可以通过URL IP：PORT/admin访问admin面板，即可以对数据库中数据进行可视化操作。![img](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202204222323166.jpg)

图 五.13创建超级管理员

图5.13 创建超级管理员

![img](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202204222323490.jpg)

图 五.14超级管理员登录面板

图5.14 超级管理员登录面板![img](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202204222323511.jpg)

图 五.15查看YZW数据库信息

 

图5.15 查看YZW数据库信息

 

![img](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202204222323523.jpg)

图 五.16修改YZW数据库中的信息

图5.16 修改YZW数据库中的信息

 

 

## 3.3 微信小程序

### 3.3.1  微信小程序界面展示

微信小程序主要负责与用户的交互以及界面显示效果。

![img](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202204222323548.jpg)

图 五.17主页

图5.17主页

![img](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202204222323611.jpg)

图 五.18广场页寻物启事

图5.20 广场页寻物启事

![img](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202204222323751.jpg)

图 五.19广场页校园资讯

图5.21 广场页校园资讯

![img](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202204222323791.jpg)

图 五.20搜索页

图5.21搜索页

 

 

![img](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202204222323086.jpg)

图 五.21寻物启事详情页

图5.22寻物启事详情页

![img](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202204222323102.jpg)

图 五.22失物招领详情页

图5.23失物招领详情页

![img](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202204222323103.jpg)

图 校园资讯详情页

图5.24校园资讯详情页

 

 

![img](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202204222323110.jpg)

图 五.23学科门类下拉框

图5.25学科门类下拉框

![img](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202204222323301.jpg)

图 五.24学科类别下拉框

图5.26学科类别下拉框

![img](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202204222323311.jpg)

图 五.25文件分享

图5.26文件分享

![img](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202204222323449.jpg)

图 五.26联系客服

图5.27联系客服



#  第四章 修改项目配置信息



## 4.1 爬虫项目配置

### 4.1.1 USC_Sunshine



![image-20220422233406281](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202204222334406.png)

对阿里云OSS、Mysql数据库与splash进行配置



### 4.1.2 YZW



![image-20220422233524983](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202204222335105.png)

对mysql数据库以及快代理进行相关配置



## 4.2 Django



![image-20220422233644077](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202204222336200.png)

对数据库进行配置



## 4.3 微信小程序



![image-20220422233805984](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202204222338112.png)

![image-20220422233828956](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202204222338188.png)

![image-20220422233853251](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202204222338387.png)

![image-20220422233920665](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202204222339742.png)

![image-20220422233948865](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202204222339994.png)

![image-20220422234009322](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202204222340467.png)



修改微信小程序js文件中对IP地址以及端口号



# 第五章 运行项目

在docker中启动splash服务



进入 wx_miniapp_end目录中，并在终端输入



```shell
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser
```



进入spider/yzw与spider/usc_sunshine中运行start.py



启动微信开发者工具，编译代码

























