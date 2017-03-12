#！encoding: utf-8
from django.shortcuts import render_to_response
from zhiyuw.config import global_settings, reset_setting
from zhiyuw import controller
from members import controller as controller2
import zhiyuw.function as fun
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
import time, json

def valid_code(func):
    def __warp(req):
        if req.method=='POST':
            value = controller.validation_code(req.POST.get('code_id'))
            if not value or value!=req.POST.get('code'):
                msg = '验证码错误'
                return render_to_response("mobile/msg.html", locals(), context_instance = RequestContext(req))
        ret = func(req)
        return ret
    return __warp

def request_login(func):
    def __warp(req, *args):
        if not req.session.get('isLogin'):
            # msg = '你需要先<a href="/mobile/login" style="color:#069FE6">登录</a>才能访问'
            # return render_to_response("mobile/msg.html", locals(), context_instance = RequestContext(req))
            return HttpResponseRedirect('/mobile/login')
        if req.session.get('3rd_not_init'):
            return HttpResponseRedirect('/mobile/3rd_yd?uid=%s' % req.session['info']['id'])
        if (args):
            return func(req, *args)
        else:
            return func(req)
    return __warp

def index(req):
    # print req.session['site_host']
    req.session['banner_list_mobile']  = global_settings['banner_list_mobile']
    req.session['settings'] = global_settings['settings']
    logo_image = fun.get_site_logo(req)
    fsb_list = controller.get_fsb_list(req, 5)
    nxt_list = controller.get_nxt_list(req, 5)
    bw_list = controller.get_cate_list(req, 'bw', 5)
    xxc_list = controller.get_cate_list(req, 'xxc', 5)
    alh_list = controller.get_alh_list(req, 5)
    index_active = 'cur'
    return render_to_response("mobile/index.html", locals(), context_instance = RequestContext(req))

cate_dict = controller.get_cate_dict()
def list(req, cate):
    page = req.GET.get('page', '1')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    logo_image = fun.get_site_logo(req)
    packagelist = None
    cate_name = cate_dict.get(cate, '无效分类')
    cate_list = controller.get_cate_list(req, cate, 15, page)
    # blog_list = controller.get_cate_list(req, 'bw', 10)
    total = controller.get_cate_total(req, cate)
    total_page = fun.get_total_page(total, 20)
    return render_to_response("mobile/list.html", locals(), context_instance = RequestContext(req))

def member(req):
    page = req.GET.get('page', '1')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    logo_image = fun.get_site_logo(req)
    data = fun.warp_data(req.GET)
    page = data.get('page', 1)
    info = controller.get_user_info(data)
    article_list = controller.get_user_article(data, req, page)
    total_page = controller2.get_post_total(req, data.get('userid',0), None)
    return render_to_response("mobile/member.html", locals(), context_instance = RequestContext(req))

def second_cate(req, cate):
    logo_image = fun.get_site_logo(req)
    packagelist = None
    cate_name = cate_dict.get(cate, '无效分类')
    if cate:
        cate_list = controller.get_child_list(req, cate)
        # print cate_list
    return render_to_response("mobile/second_cate.html", locals(), context_instance = RequestContext(req))

def contact(req):
    logo_image = fun.get_site_logo(req)
    packagelist = None
    contact_active = 'cur'
    cate_name =  '联系我们'
    return render_to_response("mobile/contact.html", locals(), context_instance = RequestContext(req))

def ktq(req):
    logo_image = fun.get_site_logo(req)
    packagelist = None
    ktq_active = 'cur'
    ktq_list = [{'id': 1, 'zhuti': '主题名1', 'logo':'/static/uploadfiles/image/20150525/thumb_287a08c4865fda9bd348cfac4bf0b090.jpg', 'qiyeming':'企业名称', 'qiye_url':"#", 'credits':'新兵蛋', 'hangye':'财务', 'desc':'企业简介描述，不超过200字'},
                {'id': 2, 'zhuti': '百度一下，你就', 'logo':'/static/uploadfiles/image/20150526/bd_logo1.png', 'qiyeming':'百度', 'qiye_url':"http://www.baidu.com", 'credits':'老鸟单', 'hangye':'财务', 'desc':'企业简介描述，不超过200字'}] * 5
    name = req.GET.get('name')
    page = req.GET.get('page', '1')
    if page and page.isdigit:
        page = int(page)
    else:
        page = 1
    if page<1:
        ktq_list = []
    elif name:
        prepage = 'name=%s&page=%s' % (name, page-1)
        nextpage = 'name=%s&page=%s' % (name, page+1)
        ktq_list = controller.get_ktq_list(req, 20, name, page)
        base_path = '?name=%s&page=' % name
    else:
        prepage = 'page=%s' % (page-1,)
        nextpage = 'page=%s' % (page+1,)
        ktq_list = controller.get_ktq_list(req, 20, name, page)
        base_path = '?page='
    total = controller.get_ktq_total(req, name)
    total_page = fun.get_total_page(total, 20)
    return render_to_response("mobile/ktq.html", locals(), context_instance = RequestContext(req))

def gyq(req):
    logo_image = fun.get_site_logo(req)
    packagelist = None
    gyq_active = 'cur'
    name = req.GET.get('name')
    page = req.GET.get('page', '1')
    if page and page.isdigit:
        page = int(page)
    else:
        page = 1
    if page<1:
        gyq_list = []
    elif name:
        prepage = 'name=%s&page=%s' % (name, page-1)
        nextpage = 'name=%s&page=%s' % (name, page+1)
        gyq_list = controller.get_gyq_list(req, 20, name, page)
        base_path = '?name=%s&page=' % name
    else:
        prepage = 'page=%s' % (page-1,)
        nextpage = 'page=%s' % (page+1,)
        gyq_list = controller.get_gyq_list(req, 20, name, page)
        base_path = '?page='
    total = controller.get_gyq_total(req, name)
    total_page = fun.get_total_page(total, 20)
    return render_to_response("mobile/gyq.html", locals(), context_instance = RequestContext(req))

def login(req):
    logo_image = fun.get_site_logo(req)
    cate_name = '用户登录'
    if req.method=='GET':
        from zhiyuw.config import qq_appid
        third_appid = qq_appid
        return render_to_response("mobile/login.html", locals(), context_instance = RequestContext(req))
    elif req.method=='POST':
        data = fun.warp_data(req.POST)
        r = controller.auth(req, data)
        if r:
            # print r
            req.session['isLogin'] = True
            req.session['info'] = r
            return HttpResponseRedirect("/mobile")
        else:
            msg = '用户或密码错误'
            return render_to_response("mobile/msg.html", locals(), context_instance = RequestContext(req))

@valid_code
def register(req):
    logo_image = fun.get_site_logo(req)
    cate_name = '用户注册'
    if req.method=='GET':
        express, express_id = controller.get_valid_code()
        return render_to_response("mobile/register.html", locals(), context_instance = RequestContext(req))
    elif req.method=='POST':
        data = fun.warp_data(req.POST)
        if data['password']!=data['password2']:
            msg = '两次密码不一致'
        else:
            if req.META.has_key('HTTP_X_FORWARDED_FOR'):
                data['ip'] =  req.META['HTTP_X_FORWARDED_FOR']
            else:
                data['ip'] = req.META['REMOTE_ADDR']
            r = controller.reg_user(req, data)
            print r
            if r>0:
                msg = '注册用户成功，你现在可以<a href="/mobile/login" style="color:#069FE6;">登录</a>了'
            else:
                msg = '该用户名或邮箱已<a href="/mobile/register" style="color:#069FE6;">注册</a>'
        return render_to_response("mobile/msg.html", locals(), context_instance = RequestContext(req))

def agreen(req):
    logo_image = fun.get_site_logo(req)
    cate_name = '注册协议'
    if req.method=='GET':
        agreen = controller.get_agreen()
        return render_to_response("mobile/agreen.html", locals(), context_instance = RequestContext(req))

def logout(req):
    req.session['isLogin'] = False
    req.session['info'] = {}
    return HttpResponseRedirect("/mobile")

def article(req, cate, id):
    art = controller.get_article(id)
    if not art:
        msg = '当前文章不存在或者未生效，请联系管理员'
        return render_to_response("mobile/msg.html", locals(), context_instance = RequestContext(req))
    logo_image = fun.get_site_logo(req)
    packagelist = None
    cate_name = cate_dict.get(cate, '无效分类')
    referer = req.path
    timestamp = int(time.time())
    comments = controller.get_comments(id)
    pre_page, next_page = controller.get_context_page(req, cate, id)
    return render_to_response("mobile/article.html", locals(), context_instance = RequestContext(req))

@request_login
def post(req, action):
    if req.method=='GET':
        cate_list1, cate_list2 = controller2.get_cate_list()
        if action=='new':
            post_info = {}
            return render_to_response("mobile/post.html", locals(), context_instance = RequestContext(req))
    elif req.method=='POST':
        if action=='save':
            uid = req.session['info']['id']
            uname = req.session['info']['username']
            data = fun.warp_data(req.POST)
            r = controller2.save_post(req, data, uid, uname)
            if r:
                return HttpResponseRedirect('/mobile')
            else:
                msg = '保存失败'
            return render_to_response("mobile/msg.html", locals(), context_instance = RequestContext(req))

@request_login
def myarts(req):
    data = fun.warp_data(req.GET)
    # print req.session['info']
    uid = req.session['info'].get('id', 0)
    cate = data.get('cate','')
    page = req.GET.get('page')
    if not page or int(page)==0:
        page = 1
    post_list = controller2.get_post_list(req, uid, cate, page)
    total = controller2.get_post_total(req,  uid, cate)
    total_page = fun.get_total_page(total, 20)
    return render_to_response("mobile/myarts.html", locals(), context_instance = RequestContext(req))

@request_login
def xiangwang(req):
    uid = req.session['info']['id']
    utype = req.session['info']['utype']
    data = {'userid':uid, 't':utype}
    info = controller.get_user_info(data)
    if req.method=='GET':
        total_page = controller2.get_xiangwang_count(uid)
        page = int(req.GET.get('page', 1))
        if page<1:
            page = 1
        if page>total_page and total_page>0:
            page = total_page
        my_xiangwang = controller2.get_xiangwang(uid, page)
        return render_to_response("mobile/xiangwang.html", locals(), context_instance = RequestContext(req))

@request_login
def tianchi(req):
    uid = req.session['info']['id']
    utype = req.session['info']['utype']
    data = {'userid':uid, 't':utype}
    info = controller.get_user_info(data)
    if req.method=='GET':
        focus_count = controller2.get_focus_count(uid)
        page = int(req.GET.get('page', 1))
        gread = req.GET.get('gread', '')
        total_page = controller2.get_tianchi_count(uid, gread)
        if page<1:
            page = 1
        if page>total_page and total_page>0:
            page = total_page
        my_tianchi = controller2.get_tianchi(uid, gread, page)
        # print my_tianchi
        return render_to_response("mobile/tianchi.html", locals(), context_instance = RequestContext(req))

@request_login
def navigate(req, action):
    uid = req.session['info']['id']
    utype = req.session['info']['utype']
    data = {'userid':uid, 't':utype}
    info = controller.get_user_info(data)
    if req.method=='GET':
        urls = controller2.get_user_urls(uid)
        admin_urls = controller2.get_admin_urls()
        return render_to_response("mobile/navigate.html", locals(), context_instance = RequestContext(req))
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
            r = controller2.save_url(uid, nid, name, url)
            if r:
                return HttpResponse(json.dumps(result),content_type="application/json")
            else:
                result = {'errorCode':-2, 'msg':'保存失败'}
                return HttpResponse(json.dumps(result),content_type="application/json")
        elif action=='delete':
            nid = data.get('nid', '')
            if nid.strip():
                r = controller2.del_url(uid, nid)
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
def pinpai(req):
    uid = req.session['info']['id']
    utype = req.session['info']['utype']
    data = {'userid':uid, 't':utype}
    info = controller.get_user_info(data)
    cate_name =  '我的品牌'
    if req.method=='GET':
        count = controller2.get_count(uid)
        return render_to_response("mobile/pinpai.html", locals(), context_instance = RequestContext(req))

@request_login
def caifu(req):
    uid = req.session['info']['id']
    utype = req.session['info']['utype']
    data = {'userid':uid, 't':utype}
    info = controller.get_user_info(data)
    cate_name =  '我的财富'
    if req.method=='GET':
        count = controller2.get_count(uid)
        return render_to_response("mobile/caifu.html", locals(), context_instance = RequestContext(req))

@request_login
def money(req):
    uid = req.session['info']['id']
    if req.method=='GET':
        utype = req.session['info']['utype']
        data = {'userid':uid, 't':utype}
        info = controller.get_user_info(data)
        history = controller2.get_money_history(uid)
        return render_to_response("mobile/money_history.html", locals(), context_instance = RequestContext(req))
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
        r = controller2.log_money(uid, account, int(num))
        if r:
            result = {'errorCode':0, 'msg':''}
            return HttpResponse(json.dumps(result),content_type="application/json")
        else:
            result = {'errorCode':-1, 'msg':'赠送失败'}
            return HttpResponse(json.dumps(result),content_type="application/json")

def info(req, action):
    uid = req.session['info']['id']
    utype = req.session['info']['utype']
    data = {'userid':uid, 't':utype}
    info = controller.get_user_info(data)
    if req.method=='GET':
        info = controller2.get_user_profile(req.GET.get('userid','0'), action)
        if info:
            info = info[action]
        else:
            info = ''
        return render_to_response("mobile/info.html", locals(), context_instance = RequestContext(req))

def qq_login(req):
    if req.method=='GET':
        data = req.GET
        msg = '正在进行QQ登录操作，请稍后...'
        return render_to_response("mobile/qq.html", locals(), context_instance = RequestContext(req))
    elif req.method=='POST':
        qq_info = req.POST
        print qq_info
        open_id = qq_info['openId']
        r = controller.is_3rd_exist(open_id)
        if r:
            if r.get('utype'):
                result = {'errorCode':0, 'msg':'成功 ', 'url':'/mobile'}
            else:
                result = {'errorCode':0, 'msg':'成功 ', 'url':'/mobile/3rd_yd?uid=%s'%r.get('id')}
                # result = {'errorCode':0, 'msg':'成功 ', 'url':'/mobile'}
                req.session['3rd_not_init'] = True
        else:
            req.session['3rd_not_init'] = True
            uid = controller.add_3rd_user(req, qq_info ,'qq')
            result = {'errorCode':0, 'msg':'成功 ', 'url':'/mobile/3rd_yd?uid=%s'% uid}
            # result = {'errorCode':0, 'msg':'成功 ', 'url':'/mobile'}
        info = controller.auth_3rd(req, open_id, 'qq')
        req.session['isLogin'] = True
        req.session['info'] = info
        return HttpResponse(json.dumps(result), content_type="application/json")

def weixin_login(req):
    from zhiyuw.config import weixin_id, weixin_secret
    from utils.function import send_http
    if req.method=='GET':
        data = req.GET
        code = data.get('code')
        print weixin_id, weixin_secret, code
        get_token_url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code' % (weixin_id, weixin_secret, code)
        print get_token_url
        access_info = send_http(get_token_url)
        print access_info
        access_token = access_info.get('access_token')
        openid = access_info.get('openid')
        unionid = access_info.get('unionid')
        call_api_url = 'https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s' % (access_token, openid)
        weixin_info = send_http(call_api_url)
        print weixin_info
        r = controller.is_3rd_exist(unionid)
        if r:
            if r.get('utype'):
                page = '/mobile'
            else:
                page = '/mobile/3rd_yd?uid=%s'%r.get('id')
                req.session['3rd_not_init'] = True
        else:
            req.session['3rd_not_init'] = True
            uid = controller.add_3rd_user(req, weixin_info ,'weixin')
            page = '/mobile/3rd_yd?uid=%s'% uid
        info = controller.auth_3rd(req, unionid, 'weixin')
        req.session['isLogin'] = True
        req.session['info'] = info
        return HttpResponseRedirect(page)

def third_yd(req):
    logo_image = fun.get_site_logo(req)
    if req.method=='GET':
        uid = req.GET.get('uid')
        return render_to_response("mobile/3rd_yd.html", locals(), context_instance = RequestContext(req))
    elif req.method=='POST':
        data = req.POST
        print data
        if not data.get('uid') or data.get('uid')=='None':
            msg = '当前为非法提交'
            return render_to_response("mobile/msg.html", locals(), context_instance = RequestContext(req))
        r = controller.bind_3rd_info(data)
        if r:
            req.session['3rd_not_init'] = False
            req.session['info']['utype'] = data.get('utype')
            # print req.session['info']
            # return render_to_response("zhiyuw/reg_yd.html", locals(), context_instance = RequestContext(req))
            return HttpResponseRedirect('/mobile')
        else:
            msg = '手机或Email信息已绑定，添加信息失败。'
            return render_to_response("mobile/msg.html", locals(), context_instance = RequestContext(req))

import datetime
def forgotpwd(req):
    logo_image = fun.get_site_logo(req)
    if req.method=="GET":
        data = req.GET
        user_name = data.get('userName')
        sid = data.get('sid')
        if user_name and sid:
            r = controller.get_reset(user_name)
            d = datetime.datetime.now()
            if r.get('sid')==sid and r.get('ttl')>time.mktime(d.timetuple()):
                return render_to_response("mobile/forgotpw3.html", locals(), context_instance = RequestContext(req))
            else:
                msg = "链接无效或已过期！"
                return render_to_response("mobile/msg.html", locals(), context_instance = RequestContext(req))
        else:
            return render_to_response("mobile/forgotpw.html", locals(), context_instance = RequestContext(req))
    elif req.method=="POST":
        import uuid, hashlib
        from utils.function import send_reset_email
        data = req.POST
        account = data.get('account')
        password = data.get('password')
        if account:
            email = controller.get_email_by_account(account)
            if email:
                d1 = datetime.datetime.now()
                d2 = d1 + datetime.timedelta(hours=0.5)
                sid = '%s$%s$%s' % (email, d2.ctime(), uuid.uuid1())
                m2 = hashlib.md5()
                m2.update(sid)
                sid = m2.hexdigest()
                host = req.META['HTTP_HOST'].split(':')[0]
                r = controller.add_reset(email, sid, time.mktime(d2.timetuple()))
                if r:
                    url = 'http://%s/mobile/forgotpwd?sid=%s&userName=%s' % (host, sid, email)
                    print url
                    send_reset_email(url, email)
                    email_pre = email.split('@')[0]
                    index = len(email_pre)/3
                    email_mix = email[:index]+'**'+email[index+2:]
                    return render_to_response("mobile/forgotpw2.html", locals(), context_instance = RequestContext(req))
                else:
                    msg = '找回密码失败'
            else:
                msg = "无效的账户！"
            return render_to_response("mobile/msg.html", locals(), context_instance = RequestContext(req))
        elif password:
            sid = data.get('sid')
            user_name = data.get('userName')
            r = controller.get_reset(user_name)
            d = datetime.datetime.now()
            if r.get('sid')==sid and r.get('ttl')>time.mktime(d.timetuple()):
                if controller.reset_passwd(password, user_name):
                    return render_to_response("mobile/forgotpw4.html", locals(), context_instance = RequestContext(req))
                else:
                    msg = "密码已被更新"
            else:
                msg = "当前链接已过期！"
            return render_to_response("mobile/msg.html", locals(), context_instance = RequestContext(req))
        else:
            msg = "访问无效！"
            return render_to_response("mobile/msg.html", locals(), context_instance = RequestContext(req))

