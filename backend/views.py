#encoding: utf-8

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import json
import controller
from zhiyuw import function as fun

setting = {'site_name': '职语网'}

@login_required
def index(req):
    settings = setting
    post_list = controller.get_post_list(1, 5)
    comment_list = controller.get_comment_list(1, 5)
    return render_to_response("backend/index.html", locals())

@login_required
def post(req, action):
    settings = setting
    if req.method=='GET':
        if action=='new':
            cate_list1, cate_list2 = controller.get_cate_list()
            post_info = {}
            return render_to_response("backend/post.html", locals())
        elif action=='edit':
            cate_list1, cate_list2 = controller.get_cate_list()
            post_info = controller.get_post_info(req.GET.get('id',0))
            return render_to_response("backend/post.html", locals())
        elif action=='list':
            page = req.GET.get('page')
            if not page:
                page = 1
            if int(page)>0:
                post_list = controller.get_post_list(page)
            else:
                post_list = []
            return render_to_response("backend/postlist.html", locals())
    elif req.method=='POST':
        if action=='save':
            data = fun.warp_data(req.POST)
            r = controller.save_post(data)
            if r:
                return HttpResponseRedirect('/backend/post/list/')
            else:
                msg = '保存失败'
            return render_to_response("backend/msg.html", locals())
        elif action=='del':
            data = fun.warp_data(req.POST)
            id = data.get('id')
            if controller.del_post(id):
                result = {'errorCode':0, 'msg':'删除成功'}
            else:
                result = {'errorCode':-1, 'msg':'删除失败'}
            return HttpResponse(json.dumps(result),content_type="application/json")

@login_required
def comments(req, action):
    settings = setting
    if req.method=='GET':
        if action=='new':
            comment_info = {}
            return render_to_response("backend/comments.html", locals())
        elif action=='edit':
            id = req.GET.get('id')
            if not id:
                id = 0
            comment_info = controller.get_comment_info(id)
            return render_to_response("backend/comments.html", locals())
        elif action=='list':
            page = req.GET.get('page')
            if not page:
                page = 1
            if int(page)>0:
                comment_list = controller.get_comment_list(page)
            else:
                comment_list = []
            return render_to_response("backend/commentslist.html", locals())
    elif req.method=='POST':
        data = req.POST
        if action=='save':
            r = controller.save_comment(data)
            if r:
                return HttpResponseRedirect('/backend/comments/list/')
            else:
                msg = '保存失败'
            return render_to_response("backend/msg.html", locals())
            return HttpResponse(json.dumps(data),content_type="application/json")
        elif action=='del':
            id = data.get('id')
            if controller.del_comment(id):
                result = {'errorCode':0, 'msg':'删除成功'}
            else:
                result = {'errorCode':-1, 'msg':'删除失败'}
            return HttpResponse(json.dumps(result),content_type="application/json")

@login_required
def category(req, action):
    settings = setting
    if req.method=='GET':
        if action=='new':
            return render_to_response("backend/category.html", locals())
        elif action=='edit':
            post_info = {}
            return render_to_response("backend/category.html", locals())
        elif action=='list':
            post_list = {}
            return render_to_response("backend/categorylist.html", locals())
    elif req.method=='POST':
        if action=='save':
            data = req.POST
            return HttpResponse(data,content_type="application/json")
        elif action=='del':
            data = req.POST
            return HttpResponse(data,content_type="application/json")

def login(req):
    return render_to_response("backend/login.html", setting)

from um import imageUp
def postimage(req):
    if req.method=='GET':
        return HttpResponse("unsupport method")
    # print dir(req.FILES)
    data = imageUp.imageup(req.FILES['upfile'])
    # print data
    return HttpResponse(data, content_type="application/json")