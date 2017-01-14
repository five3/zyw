#encoding: utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import json
import controller
from zhiyuw import function as fun
from django.template import RequestContext
from zhiyuw import controller as controller2

def request_login(func):
    def __warp(req):
        if not req.session.get('isLogin'):
            return HttpResponseRedirect('/zhiyuw/login')
        if req.session.get('3rd_not_init'):
            return HttpResponseRedirect('/zhiyuw/3rd_yd?uid=%s' % req.session['info']['id'])
        ret = func(req)
        return ret
    return __warp

@request_login
def index(req):
    data = fun.warp_data(req.GET)
    # print req.session['info']
    uid = req.session['info'].get('id', 0)
    cate = data.get('cate','')
    page = req.GET.get('page')
    if not page or int(page)==0:
        page = 1
    post_list = controller.get_post_list(req, uid, cate, page)
    cates = controller.get_user_cates(uid)
    print cates
    return render_to_response("members/index.html", locals(), context_instance = RequestContext(req))

@request_login
def post(req, action):
    uid = req.session['info'].get('id', 0)
    if req.method=='GET':
        cates = controller.get_user_cates(uid)
        cate_list1, cate_list2 = controller.get_cate_list()
        if action=='new':
            post_info = {}
            return render_to_response("members/post.html", locals(), context_instance = RequestContext(req))
        elif action=='edit':
            post_info = controller.get_post_info(req.GET.get('id',0))
            return render_to_response("members/post.html", locals(), context_instance = RequestContext(req))
        elif action=='del':
            id = req.GET.get('id')
            if controller.del_post(id):
                return HttpResponseRedirect('/members')
            else:
                msg = '删除失败'
                return render_to_response("members/msg.html", locals(), context_instance = RequestContext(req))
    elif req.method=='POST':
        if action=='save':
            uid = req.session['info']['id']
            uname = req.session['info']['username']
            data = fun.warp_data(req.POST)
            r = controller.save_post(req, data, uid, uname)
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
@request_login
def postimage(req):
    uid = req.session['info']['id']
    utype = req.session['info']['utype']
    if req.method=='GET':
        return HttpResponse("unsupport method")
    # print req.FILES.keys()
    data = imageUp.imageup(req.FILES['upfile'])
    # print req.GET
    if 'editorid' in req.GET or 'type' in req.GET:
        return HttpResponse(json.dumps(data),content_type="application/json")

    cates = controller.get_user_cates(uid)
    if data['state']=='SUCCESS':
        if controller.update_photo_img(data['abs_url'], utype, uid):
            return HttpResponseRedirect('/members/profile')
        msg = '上传头像失败'
        return render_to_response("members/msg.html", locals(), context_instance = RequestContext(req))

@request_login
def profile(req):
    uid = req.session['info']['id']
    utype = req.session['info']['utype']
    # print req.session['info']
    if req.method=='GET':
        cates = controller.get_user_cates(uid)
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

@request_login
def password(req):
    uid = req.session['info']['id']
    cates = controller.get_user_cates(uid)
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

@request_login
def bgmusic(req):
    uid = req.session['info']['id']
    if req.method=='GET':
        cates = controller.get_user_cates(uid)
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

@request_login
def zhaopin(req):
    uid = req.session['info']['id']
    uname = req.session['info']['username']
    if req.method=='GET':
        cates = controller.get_user_cates(uid)
        return render_to_response("members/zhaopin.html", locals(), context_instance = RequestContext(req))
    else:
        data = fun.warp_data(req.POST)
        if controller.post_zhaopin(req, data, uid, uname):
            msg = '职位发布成功！'
        else:
            msg = '职位发布失败'
        return render_to_response("members/msg.html", locals(), context_instance = RequestContext(req))

@request_login
def shuoshuo(req):
    uid = req.session['info']['id']
    if req.method=='GET':
        id = req.GET.get('id')
        if id:
            t = req.GET.get('t')
            if not t=='del':
                msg = controller.get_qiye_comment(id)
                return render_to_response("members/raw.html", locals(), context_instance = RequestContext(req))
            else:
                controller.del_qiye_comment(id)
        page = req.GET.get('page', 1)
        shuoshuo_list = controller.get_shuoshuo_list(uid, page)
        cates = controller.get_user_cates(uid)
        return render_to_response("members/shuoshuo.html", locals(), context_instance = RequestContext(req))
    else:
        data = fun.warp_data(req.POST)
        pass

@request_login
def pinpai(req):
    uid = req.session['info']['id']
    utype = req.session['info']['utype']
    data = {'userid':uid, 't':utype}
    info = controller2.get_user_info(data)
    bg_img = '/static/members/cy_images/images/bg01.jpg'
    if req.method=='GET':
        count = controller.get_count(uid)
        cates = controller.get_user_cates(uid)
        return render_to_response("members/pinpai.html", locals(), context_instance = RequestContext(req))

@request_login
def tianchi(req):
    uid = req.session['info']['id']
    utype = req.session['info']['utype']
    data = {'userid':uid, 't':utype}
    info = controller2.get_user_info(data)
    bg_img = '/static/members/cy_images/images/bg03.jpg'
    if req.method=='GET':
        focus_count = controller.get_focus_count(uid)
        page = int(req.GET.get('page', 1))
        gread = req.GET.get('gread', '')
        total_page = controller.get_tianchi_count(uid, gread)
        if page<1:
            page = 1
        if page>total_page and total_page>0:
            page = total_page
        my_tianchi = controller.get_tianchi(uid, gread, page)
        # print my_tianchi
        cates = controller.get_user_cates(uid)
        return render_to_response("members/tianchi.html", locals(), context_instance = RequestContext(req))

@request_login
def xiangwang(req):
    uid = req.session['info']['id']
    utype = req.session['info']['utype']
    data = {'userid':uid, 't':utype}
    info = controller2.get_user_info(data)
    bg_img = '/static/members/cy_images/images/bg02.jpg'
    if req.method=='GET':
        total_page = controller.get_xiangwang_count(uid)
        page = int(req.GET.get('page', 1))
        if page<1:
            page = 1
        if page>total_page and total_page>0:
            page = total_page
        my_xiangwang = controller.get_xiangwang(uid, page)
        cates = controller.get_user_cates(uid)
        return render_to_response("members/xiangwang.html", locals(), context_instance = RequestContext(req))

@request_login
def daohang(req, action):
    uid = req.session['info']['id']
    utype = req.session['info']['utype']
    data = {'userid':uid, 't':utype}
    info = controller2.get_user_info(data)
    if req.method=='GET':
        urls = controller.get_user_urls(uid)
        cates = controller.get_user_cates(uid)
        return render_to_response("members/daohang.html", locals(), context_instance = RequestContext(req))
    elif req.method=='POST':
        data = req.POST
        result = {'errorCode':0, 'msg':''}
        if action=='save':
            nid = data.get('nid', '').strip()
            name = data.get('name', '')
            url = data.get('url', '')
            if not name.strip() or not url.strip():
                result = {'errorCode':-1, 'msg':'字段不能为空'}
                return HttpResponse(json.dumps(result),content_type="application/json")
            r = controller.save_url(uid, nid, name, url)
            if r:
                return HttpResponse(json.dumps(result),content_type="application/json")
            else:
                result = {'errorCode':-2, 'msg':'保存失败'}
                return HttpResponse(json.dumps(result),content_type="application/json")
        elif action=='delete':
            nid = data.get('nid', '')
            if nid.strip():
                r = controller.del_url(uid, nid)
                if r:
                    return HttpResponse(json.dumps(result),content_type="application/json")
                else:
                    result = {'errorCode':-3, 'msg':'删除失败'}
                    return HttpResponse(json.dumps(result),content_type="application/json")
            else:
                return HttpResponse('no nid',content_type="application/json")
        else:
            return HttpResponse('not well',content_type="application/json")

@request_login
def money(req):
    uid = req.session['info']['id']
    if req.method=='GET':
        utype = req.session['info']['utype']
        data = {'userid':uid, 't':utype}
        info = controller2.get_user_info(data)
        history = controller.get_money_history(uid)
        cates = controller.get_user_cates(uid)
        return render_to_response("members/money_history.html", locals(), context_instance = RequestContext(req))
    elif req.method=='POST':
        account = req.POST.get('account')
        num = req.POST.get('money', '0').strip()
        error = 0
        if not num.isdigit():
            error = -1
        elif int(num)<0:
            error = -2
        if error<0:
            result = {'errorCode':-1, 'msg':'输入错误'}
            return HttpResponse(json.dumps(result),content_type="application/json")
        r = controller.log_money(uid, account, int(num))
        if r:
            result = {'errorCode':0, 'msg':''}
            return HttpResponse(json.dumps(result),content_type="application/json")
        else:
            result = {'errorCode':-1, 'msg':'赠送失败'}
            return HttpResponse(json.dumps(result),content_type="application/json")

@request_login
def cate(req):
    data = fun.warp_data(req.GET)
    uid = req.session['info'].get('id', 0)
    name = data.get('name','')
    page = req.GET.get('page')
    if not page or int(page)==0:
        page = 1
    post_list = controller.get_cate3_list(req, uid, name, page)
    cates = controller.get_user_cates(uid)
    return render_to_response("members/index.html", locals(), context_instance = RequestContext(req))
