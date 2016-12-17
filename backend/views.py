#encoding: utf-8

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import json
import controller
from zhiyuw import function as fun
from zhiyuw.config import reset_setting, global_settings

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
        elif action=='audit':
            data = fun.warp_data(req.POST)
            r = controller.audit_post(data)
            return HttpResponse(json.dumps(r),content_type="application/json")
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

from django import forms
class bannerForm(forms.Form):
    url = forms.CharField(max_length=1024)
    src = forms.FileField()

@login_required
def admin(req, action):
    if not req.user.is_superuser:
        msg = '你没有相关权限！'
        return render_to_response('backend/msg.html', locals())
    settings = setting
    if req.method=='GET':
        if action=='list' :
            page = req.GET.get('page', 1)
            if int(page) < 1:
                page = 1
            last_page = controller.get_admin_pages(req)
            adminlist = controller.get_admin_list(req, page)
            return render_to_response("backend/adminlist.html", locals())
        elif action=='new':
            return render_to_response("backend/addadmin.html", locals())
        elif action=='setting':
            website_settings = controller.get_settings()
            return render_to_response("backend/setting.html", locals())
        elif action=='banner':
            banners = controller.get_banners()
            return render_to_response("backend/banner.html", locals())
    elif req.method=='POST':
        if action=='new':
            r = controller.add_admin(req.POST)
            if r:
                return HttpResponseRedirect('/backend/admin/list/')
            else:
                msg = '用户名已存在'
                return render_to_response('backend/msg.html', locals())
        elif action=='setting':
            r = controller.update_setting(req.POST)
            if r:
                msg = '更新网站设置成功'
                reset_setting(global_settings)
            else:
                msg = '更新网站设置失败'
            return render_to_response('backend/msg.html', locals())
        elif action=='banner':
            id = req.POST.get('id', 0)
            if id: ##delete
                if controller.del_banner(id):
                    msg = '删除成功'
                    reset_setting(global_settings)
                else:
                    msg = '删除失败'
                return HttpResponse(json.dumps({'errorCode':0, 'msg' : msg}),content_type="application/json")
            else: ##add
                import os
                from um import imageUp
                img_dir = "%s/static/backend/images/banner" % os.getcwd()
                file_path = imageUp.save_image(bannerForm, req.POST, req.FILES, img_dir, 'src')
                if file_path:
                    url = req.POST.get('url')
                    t = req.POST.get('t')
                    if controller.add_banner(url, file_path, t):
                        msg = "添加成功"
                        reset_setting(global_settings)
                    else:
                        msg = '添加失败'
                else:
                    msg = '保存图片失败'
                return render_to_response('backend/msg.html', locals())

        id = req.POST.get('id', 0)
        if id:
            if action=='reset_passwd':
                controller.reset_admin_passwd(id)
                msg = '密码设置为：000000'
            else:
                controller.audit_admin(id, action)
                msg = ''
            return HttpResponse(json.dumps({'errorCode':0, 'msg' : msg}),content_type="application/json")
        else:
            msg = 'id 无效'
            return render_to_response("backend/msg.html", locals())

@login_required
def manage(req, action):
    settings = setting
    if req.method=='GET':
        if action=='agreen':
            agreen = controller.get_agreen()
            return render_to_response("backend/agreen.html", locals())
        else:
            msg = '无效url访问'
        return render_to_response("backend/msg.html", locals())
    else:
        if action=='agreen':
            content = req.POST.get('content', '')
            if content.strip():
                if controller.update_agreen(content):
                    msg = '更新协议成功'
                else:
                    msg = '更新协议失败，请联系管理员'
            else:
                msg = '内容无效'
            return render_to_response("backend/msg.html", locals())


@login_required
def users(req, action):
    settings = setting
    if req.method=='GET':
        if action=='list':
            page = req.GET.get('page', 1)
            keys = req.GET.get('keys', '')
            if int(page) < 1:
                page = 1
            last_page = controller.get_user_pages(req)
            if keys:
                userlist = controller.get_user_list(req, page, 10, keys)
            else:
                userlist = controller.get_user_list(req, page)
            return render_to_response("backend/userslist.html", locals())
    else:
        id = req.POST.get('id', 0)
        if id:
            if action=='reset_passwd':
                controller.reset_user_passwd(id)
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

@login_required
def profile(req):
    settings = setting
    if req.method=='GET':
        data = fun.warp_data(req.GET)
        info = controller.get_user_info(data)
        # print info
        return render_to_response("backend/profile.html", locals())
    else:
        return HttpResponse({'errorCode' : 'method not supported!'},content_type="application/json")

@login_required
def resetpw(req):
    settings = setting
    if req.method=='GET':
        return render_to_response("backend/resetpw.html", locals())
    else:
        uid = req.user.id
        username = req.user.username
        data = req.POST
        oldpasswd = data.get('oldpasswd')
        passwd = data.get('passwd')
        r = controller.update_admin_passwd(uid, username, oldpasswd, passwd)
        if r:
            msg = '密码修改成功'
        else:
            msg = '密码修改失败,请确认密码输入正确'
        return render_to_response("backend/msg.html", locals())

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
            if not req.user.is_active:
                msg = '该用户未生效'
            return render_to_response("backend/msg.html", locals())


from um import imageUp
def postimage(req):
    if req.method=='GET':
        return HttpResponse("unsupport method")
    # print dir(req.FILES)
    data = imageUp.imageup(req.FILES['upfile'])
    return HttpResponse(json.dumps(data), content_type="application/json")