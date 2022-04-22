import math
import os
from math import ceil

import pandas as pd
import re
import requests
from django.shortcuts import render
from .models import YZW, Lost, Found, Info, SubjectInfo
from django.http import HttpResponse, JsonResponse, FileResponse


# Create your views here.
# 获取考研信息
def getYZWData(request):
    n = int(request.GET.get('n'))
    yjxkmd = str(request.GET.get('yjxkmd'))
    l = len(YZW.objects.filter(Major__contains=yjxkmd).all())
    page = 25
    max_n = int(l / 25)
    if n > max_n:
        n = max_n
    if n < 0:
        n = 0
    data = {}
    YZWData = YZW.objects.filter(Major__contains=yjxkmd).order_by('School', 'College', 'Major').all()[
              n * page:(n + 1) * page].values()
    data["data"] = list(YZWData)
    # 以json格式返回
    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})


# 获取寻物启事信息
def getLostData(request):
    # 获取请求页码
    cur_page = int(request.GET.get('page'))
    page_size = 5
    l = len(Lost.objects.all())
    total_page = math.ceil(l / page_size)
    data = {}
    # 翻页处理，对最后一页的处理，按照最新信息排序
    if cur_page < total_page:
        LostData = Lost.objects.all().order_by('-public_time').values()[(cur_page - 1) * page_size:cur_page * page_size]
    else:
        if cur_page != total_page:
            cur_page = total_page
        LostData = Lost.objects.all().order_by('-public_time').values()[(cur_page - 1) * page_size:l]
    data['total_page'] = total_page
    data['cur_page'] = cur_page
    data['page_size'] = page_size
    data["data"] = list(LostData)
    # 以json格式返回
    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})


# 获取失物招领信息
def getFoundData(request):
    # 获取请求页码
    cur_page = int(request.GET.get('page'))
    page_size = 5
    l = len(Found.objects.all())
    total_page = math.ceil(l / page_size)
    data = {}
    # 翻页处理，对最后一页的处理，按照最新信息排序
    if cur_page < total_page:
        FoundData = Found.objects.all().order_by('-public_time').values()[
                    (cur_page - 1) * page_size:cur_page * page_size]
    else:
        if cur_page != total_page:
            cur_page = total_page
        FoundData = Found.objects.all().order_by('-public_time').values()[(cur_page - 1) * page_size:l]
    data['total_page'] = total_page
    data['cur_page'] = cur_page
    data['page_size'] = page_size
    data["data"] = list(FoundData)
    # 以json格式返回
    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})


# 获取校园资讯信息
def getInfoData(request):
    # 获取请求页码
    cur_page = int(request.GET.get('page'))
    page_size = 5
    l = len(Info.objects.all())
    total_page = math.ceil(l / page_size)
    data = {}
    # 翻页处理，对最后一页的处理，按照最新信息排序
    if cur_page < total_page:
        InfoData = Info.objects.all().order_by('-public_time').values()[(cur_page - 1) * page_size:cur_page * page_size]
    else:
        if cur_page != total_page:
            cur_page = total_page
        InfoData = Info.objects.all().order_by('-public_time').values()[(cur_page - 1) * page_size:l]
    data['total_page'] = total_page
    data['cur_page'] = cur_page
    data['page_size'] = page_size
    data["data"] = list(InfoData)
    # 以json格式返回
    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})


# 获取寻物启事信息信息
def getLostDetailInfo(request):
    # 获取需查询信息
    id = request.GET.get('id')
    print(id)
    data = {}
    lostDetailInfo = Lost.objects.filter(id=id).order_by('-public_time').values()
    data["data"] = list(lostDetailInfo)
    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})


# 获取失物招领详细信息
def getFoundDetailInfo(request):
    # 获取需查询信息
    id = request.GET.get('id')
    print(id)
    data = {}
    foundDetailInfo = Found.objects.filter(id=id).order_by('-public_time').values()
    data["data"] = list(foundDetailInfo)
    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})


# 获取校园资讯详细信息
def getInfoDetailInfo(request):
    # 获取需查询信息
    id = request.GET.get('id')
    print(id)
    data = {}
    InfoDetailInfo = Info.objects.filter(id=id).order_by('-public_time').values()
    data["data"] = list(InfoDetailInfo)
    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})


# 获取学科门类与学科类别配对信息
def getSubjectInfo(request):
    # 获取需查询信息
    id = request.GET.get('id')
    id = int(id) + 1
    if id == 15:
        id = '(zyxw)'
    else:
        if id < 10:
            id = '(0' + str(id) + ')'
        else:
            id = '(' + str(id) + ')'
    data = {}
    SubjectInfoList = SubjectInfo.objects.filter(discipline__contains=id).values()
    data["data"] = list(SubjectInfoList)
    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})


# 获取考研科目详细信息
def getYZWDetail(request):
    # 获取需查询信息
    mldm = request.GET.get('mldm')
    yjxkdm = request.GET.get('yjxkdm')
    mldm = int(mldm) + 1
    if mldm == 15:
        mldm = '(zyxw)'
    else:
        if mldm < 10:
            mldm = '(0' + str(mldm) + ')'
        else:
            mldm = '(' + str(mldm) + ')'
    SubjectInfoList = SubjectInfo.objects.filter(discipline__contains=mldm).values()
    yjxk = SubjectInfoList[int(yjxkdm)]['subject']
    # 获取学科名
    regex_str = ".*?([\u4E00-\u9FA5]+).*?"
    yjxk = re.findall(regex_str, yjxk)
    # xkml=re.findall(regex_str, yjxk)
    file_path = '../data/' + mldm + yjxk[0] + '.xlsx'
    # 判断是否存在数据有，则直接返回，没有测在本地创建数据
    if not os.path.exists(file_path):
        data = {}
        subjectDetailInfoList = YZW.objects.filter(Subject_Category=yjxk[0]).values()
        data["data"] = list(subjectDetailInfoList)
        export_excel(data['data'], file_path)

    down_file = open(file_path, 'rb')
    f_name = file_path.split('/')[-1]
    response = FileResponse(down_file, filename=f_name, as_attachment=True)
    response['Content-Type'] = 'application/octet-stream'
    return response


# 按标题搜索寻物启事
def searchLost(request):
    # 获取需查询信息
    context = request.GET.get('context')
    searchContextList = Lost.objects.filter(title__icontains=context).order_by('-public_time').values()
    data = {}
    data['data'] = list(searchContextList)
    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})


# 按标题搜索招领启事
def searchFound(request):
    # 获取需查询信息
    context = request.GET.get('context')
    searchContextList = Found.objects.filter(title__icontains=context).order_by('-public_time').values()
    data = {}
    data['data'] = list(searchContextList)
    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})


# 按标题搜索校园资讯
def searchInfo(request):
    # 获取需查询信息
    context = request.GET.get('context')
    searchContextList = Info.objects.filter(title__icontains=context).order_by('-public_time').values()
    data = {}
    data['data'] = list(searchContextList)
    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})


def export_excel(export, path):
    # 将字典列表转换为DataFrame
    pf = pd.DataFrame(list(export))
    # 指定字段顺序
    order = ['id', 'School', 'Place', 'Graduate_School', 'Self_Scribing', 'PhD', 'Disciplines', 'Subject_Category',
             'Major', 'College', 'Research_Direction', 'Learning_Style', 'Instructor', 'Number', 'Remarks', 'Lesson_1',
             'Lesson_2', 'Lesson_3', 'Lesson_4']
    pf = pf[order]

    # 指定生成的Excel表格名称
    file_path = pd.ExcelWriter(path)
    # 输出
    pf.to_excel(file_path, encoding='utf-8', index=False)
    # 保存表格
    file_path.save()
