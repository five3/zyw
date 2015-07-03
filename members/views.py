#encoding: utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import json
import controller
from zhiyuw import function as fun
from django.template import RequestContext

def index(req):
    if not req.session.get('isLogin'):
        return HttpResponseRedirect('/zhiyuw/login')
    data = fun.warp_data(req.GET)
    # print req.session['info']
    uid = req.session['info'].get('id', 0)
    cate = data.get('cate','')
    page = req.GET.get('page')
    if not page:
        page = 1
    post_list = controller.get_post_list(uid, cate, page)
    return render_to_response("members/index.html", locals(), context_instance = RequestContext(req))

def post(req, action):
    if not req.session.get('isLogin'):
        return HttpResponseRedirect('/zhiyuw/login')
    if req.method=='GET':
        cate_list1, cate_list2 = controller.get_cate_list()
        if action=='new':
            post_info = {}
            return render_to_response("members/post.html", locals(), context_instance = RequestContext(req))
        elif action=='edit':
            post_info = controller.get_post_info(req.GET.get('id',0))
            return render_to_response("members/post.html", locals(), context_instance = RequestContext(req))
    elif req.method=='POST':
        if action=='save':
            uid = req.session['info']['id']
            uname = req.session['info']['username']
            data = fun.warp_data(req.POST)
            r = controller.save_post(data, uid, uname)
            if r:
                return HttpResponseRedirect('/members')
            else:
                msg = '保存失败'
            return render_to_response("members/msg.html", locals(), context_instance = RequestContext(req))
        elif action=='del':
            data = fun.warp_data(req.POST)
            id = data.get('id')
            if controller.del_post(id):
                result = {'errorCode':0, 'msg':'删除成功'}
            else:
                result = {'errorCode':-1, 'msg':'删除失败'}
            return HttpResponse(json.dumps(result),content_type="application/json")

from um import imageUp
def postimage(req):
    if not req.session.get('isLogin'):
        return HttpResponseRedirect('/zhiyuw/login')
    uid = req.session['info']['id']
    utype = req.session['info']['utype']
    if req.method=='GET':
        return HttpResponse("unsupport method")
    # print req.FILES.keys()
    data = imageUp.imageup(req.FILES['upfile'])
    if data['state']=='SUCCESS':
        if controller.update_photo_img(data['abs_url'], utype, uid):
            return HttpResponseRedirect('/members/profile')
    msg = '上传头像失败'
    return render_to_response("members/msg.html", locals(), context_instance = RequestContext(req))

def profile(req):
    if not req.session.get('isLogin'):
        return HttpResponseRedirect('/zhiyuw/login')
    uid = req.session['info']['id']
    utype = req.session['info']['utype']
    if req.method=='GET':
        info = controller.get_profile(uid, utype)
        if utype=='ktq':
            zhuanye = controller.get_zhuanye_list()
            return render_to_response("members/cprofile.html", locals(), context_instance = RequestContext(req))
        else:
            zhiwei = controller.get_zhiwei_list()
            return render_to_response("members/gprofile.html", locals(), context_instance = RequestContext(req))
    elif req.method=='POST':
        data = fun.warp_data(req.POST)
        # print data
        r = controller.update_profile(data, utype, uid)
        if r:
            msg = '更新资料成功'
        else:
            msg = '更新资料失败'
        return render_to_response("members/msg.html", locals(), context_instance = RequestContext(req))

def password(req):
    if not req.session.get('isLogin'):
        return HttpResponseRedirect('/zhiyuw/login')
    uid = req.session['info']['id']
    if req.method=='GET':
        return render_to_response("members/password.html", locals(), context_instance = RequestContext(req))
    else:
        data = fun.warp_data(req.POST)
        if data.get('new')==data.get('renew'):
            r = controller.set_password(data, uid)
            # print r
            if r:
                msg = '密码设置成功！'
            else:
                msg = '密码设置失败'
        else:
            msg = '确认密码不一致'
        return render_to_response("members/password.html", locals(), context_instance = RequestContext(req))

def bgmusic(req):
    if not req.session.get('isLogin'):
        return HttpResponseRedirect('/zhiyuw/login')
    uid = req.session['info']['id']
    if req.method=='GET':
        return render_to_response("members/bgmusic.html", locals(), context_instance = RequestContext(req))
    else:
        src = req.POST.get('src', None)
        r = controller.set_bg_music(src, uid)
        # print r
        if r:
            req.session['info']['bgmusic'] = src
            msg = '背景音乐设置成功！'
        else:
            msg = '背景音乐设置失败'
        return render_to_response("members/bgmusic.html", locals(), context_instance = RequestContext(req))