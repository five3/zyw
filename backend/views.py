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
    post_list = controller.get_post_list(req, 1, 5)
    comment_list = controller.get_comment_list(req, 1, 5)
    return render_to_response("backend/index.html", locals())

@login_required
def post(req, action):
    settings = setting
    if req.method=='GET':
        cate_list1, cate_list2 = controller.get_cate_list()
        if action=='new':
            post_info = {}
            return render_to_response("backend/post.html", locals())
        elif action=='edit':
            post_info = controller.get_post_info(req.GET.get('id',0))
            return render_to_response("backend/post.html", locals())
        elif action=='list':
            page = req.GET.get('page')
            if not page:
                page = 1
            if int(page)>0:
                post_list = controller.get_post_list(req, page)
            else:
                post_list = []
            return render_to_response("backend/postlist.html", locals())
    elif req.method=='POST':
        if action=='save':
            data = fun.warp_data(req.POST)
            r = controller.save_post(req, data)
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
                comment_list = controller.get_comment_list(req, page)
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
            # return HttpResponse(json.dumps(data),content_type="application/json")
        elif action=='del':
            id = data.get('id')
            if controller.del_comment(id):
                result = {'errorCode':0, 'msg':'删除成功'}
            else:
                result = {'errorCode':-1, 'msg':'删除失败'}
            return HttpResponse(json.dumps(result),content_type="application/json")

@login_required
def gbook(req, action):
    settings = setting
    if req.method=='GET':
        if action=='view':
            id = req.GET.get('id')
            msg = controller.get_gbook_info(id)
            return render_to_response("backend/raw.html", locals())
        elif action=='del':
            id = req.GET.get('id')
            controller.del_gbook(id)
        page = req.GET.get('page',1)
        gbook_list = controller.get_gbook_list(req, page)
        return render_to_response("backend/gbooklist.html", locals())

@login_required
def users(req, action):
    settings = setting
    if req.method=='GET':
        if action=='list':
            page = req.GET.get('page', 1)
            userlist = controller.get_user_list(req, page)
            return render_to_response("backend/userslist.html", locals())
    else:
        id = req.POST.get('id', 0)
        if id:
            if action=='reset_passwd':
                controller.reset_passwd(id)
                msg = '密码设置为：000000'
            else:
                controller.audit_user(id, action)
                msg = ''
            return HttpResponse(json.dumps({'errorCode':0, 'msg' : msg}),content_type="application/json")
        else:
            msg = 'id 无效'
            return render_to_response("backend/msg.html", locals())

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
    settings = setting
    if req.method=='GET':
        return render_to_response("backend/login.html", locals())
    elif req.method=='POST':
        data = req.POST
        if controller.auth(req, data):
            return HttpResponseRedirect('/backend/')
        else:
            msg = '用户名或密码错误'
            return render_to_response("backend/msg.html", locals())


from um import imageUp
def postimage(req):
    if req.method=='GET':
        return HttpResponse("unsupport method")
    # print dir(req.FILES)
    data = imageUp.imageup(req.FILES['upfile'])
    return HttpResponse(json.dumps(data), content_type="application/json")