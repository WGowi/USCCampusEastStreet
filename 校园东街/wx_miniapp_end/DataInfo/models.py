from django.db import models


# Create your models here.
# 寻物启事模型类
class Lost(models.Model):
    id = models.BigIntegerField(primary_key=True)
    title = models.CharField("标题", max_length=100)
    description = models.TextField("描述")
    contact = models.CharField("联系人", max_length=100)
    tel = models.CharField("联系方式", max_length=11)
    find_or_lost_address = models.CharField("遗失地点", max_length=100)
    find_or_lost_time = models.CharField("遗失时间", max_length=100)
    black_address = models.CharField("归还地点", max_length=100)
    public_time = models.CharField("发布时间", max_length=100)
    img_url = models.CharField("图片路径", max_length=100)

    class Meta:
        db_table = 'Lost'
        verbose_name = '寻物启事'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


# 失物招领模型类
class Found(models.Model):
    id = models.BigIntegerField(primary_key=True)
    title = models.CharField("标题", max_length=100)
    description = models.TextField("描述")
    contact = models.CharField("联系人", max_length=100)
    tel = models.CharField("联系方式", max_length=11)
    find_or_lost_address = models.CharField("拾取地点", max_length=100)
    find_or_lost_time = models.CharField("拾取时间", max_length=100, default='null')
    black_address = models.CharField("归还地点", max_length=100)
    public_time = models.CharField("发布时间", max_length=100)
    img_url = models.CharField("图片路径", max_length=100)

    class Meta:
        db_table = 'Found'
        verbose_name = '失物招领'
        verbose_name_plural = verbose_name


# 校园资讯模型类
class Info(models.Model):
    id = models.IntegerField(primary_key=True, default=0)
    title = models.CharField('标题', max_length=100)
    kind = models.CharField('类别', max_length=100)
    department = models.CharField('部门', max_length=100)
    public_time = models.CharField('发布时间', max_length=100)
    content = models.TextField("内容")
    reply = models.TextField("回复")
    identity = models.CharField('身份', max_length=100)
    img_url = models.CharField("图片路径", max_length=100)

    class Meta:
        db_table = 'Info'
        verbose_name = '校园信息'
        verbose_name_plural = verbose_name


# 考研信息模型类
class YZW(models.Model):
    School = models.CharField("学校", max_length=100)  # 学校名称
    Place = models.CharField("所在地", max_length=100)  # 学校所在地
    Graduate_School = models.CharField("研究生院", max_length=100)  # 是否有研究生院 0表示无，1表示有
    Self_Scribing = models.CharField('自划线', max_length=100)  # 是否为自划线院校 0表示无，1表示有
    PhD = models.CharField('博士点', max_length=100)  # 是否有博士点 0表示无，1表示有
    Disciplines = models.CharField('学科门类', max_length=100)  # 学科门类
    Subject_Category = models.CharField('学科类别', max_length=100)  # 学科类别
    Major = models.CharField('专业', max_length=100)  # 专业名称
    College = models.CharField('院系所', max_length=100)  # 院系所
    Research_Direction = models.CharField('研究方向', max_length=100)  # 研究方向
    Learning_Style = models.CharField('学习方式', max_length=100)  # 学习方式
    Instructor = models.CharField('指导老师', max_length=100)  # 指导老师
    Number = models.CharField('招生人数', max_length=100)  # 招生人数
    Remarks = models.TextField('备注')  # 备注
    Lesson_1 = models.CharField('课程1', max_length=100)
    Lesson_2 = models.CharField('课程2', max_length=100)
    Lesson_3 = models.CharField('课程3', max_length=100)
    Lesson_4 = models.CharField('课程4', max_length=100)

    class Meta:
        db_table = 'YZW'
        verbose_name = '考研信息'
        verbose_name_plural = verbose_name


# 学科信息模型类
class SubjectInfo(models.Model):
    discipline = models.CharField("学科门类", max_length=100)
    subject = models.CharField("学科类别", max_length=100)

    class Meta:
        db_table = 'SubjectInfo'
        verbose_name = '学科信息'
        verbose_name_plural = verbose_name
