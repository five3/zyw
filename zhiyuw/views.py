#！encoding: utf-8

from django.shortcuts import render_to_response
from config import global_settings, reset_setting, qq_appid
import controller
import function as fun
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
import json
from utils.function import send_reset_email, send_http
# reset_setting(global_settings)
# print global_settings
def valid_code(func):
    def __warp(req):
        if req.method=='POST':
            value = controller.validation_code(req.POST.get('code_id'))
            if not value or value!=req.POST.get('code'):
                msg = '验证码错误'
                return render_to_response("zhiyuw/msg.html", locals(), context_instance = RequestContext(req))
        ret = func(req)
        return ret
    return __warp

def request_login(func):
    def __warp(req):
        if not req.session.get('isLogin'):
            msg = '你需要登录才能执行操作'
            return render_to_response("zhiyuw/msg.html", locals(), context_instance = RequestContext(req))
        ret = func(req)
        return ret
    return __warp

def index(req):
    # print req.session['site_host']
    req.session['banner_list']  = global_settings['banner_list']
    req.session['settings'] = global_settings['settings']
    logo_image = fun.get_site_logo(req)
    xxc_list = controller.get_cate_list(req, 'xxc', 5)
    tzl_list = controller.get_cate_list(req, 'tzl', 5)
    bw_list = controller.get_cate_list(req, 'bw', 5)
    ktq_list = controller.get_ktq_list(req, 10)
    gyq_list = controller.get_gyq_list(req, 10)
    alh_list = controller.get_alh_list(req, 5)
    fsb_list = controller.get_fsb_list(req, 5)
    zpcj_list = controller.get_cate_list(req, 'zpcj', 5)
    zxcj_list = controller.get_cate_list(req, 'zxcj', 5)
    gyrc_list = controller.get_cate_list(req, 'gyrc', 5)
    third_appid = qq_appid
    return render_to_response("zhiyuw/index.html", locals(), context_instance = RequestContext(req))

def kaituoqquan(req):
    logo_image = fun.get_site_logo(req)
    packagelist = None
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
    return render_to_response("zhiyuw/ktq.html", locals(), context_instance = RequestContext(req))

def gengyunqun(req):
    logo_image = fun.get_site_logo(req)
    packagelist = None
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
    return render_to_response("zhiyuw/gyq.html", locals(), context_instance = RequestContext(req))

cate_dict = {'alh':'CFO家园','xxc':'信息窗','zyk':'资源库','bw':'博文', 'fsb':'放松吧','nxt':'纳贤台',
             'lxwm':'联系我们','lyl':'留言栏', 'tzl':'通知栏', 'sh':'书画', 'sy':'摄影', 'bjys':'保健养生',
             'wxjl':'文学交流', 'ylxw':'娱乐新闻', 'zxmk':'招贤模块', 'zjmk':'自荐模块', 'rlzx':'人力资讯'}
cate_dict = controller.get_cate_dict()

def category(req, cate):
    page = req.GET.get('page', '1')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    logo_image = fun.get_site_logo(req)
    packagelist = None
    cate_name = cate_dict.get(cate, '无效分类')
    cate_list = controller.get_cate_list(req, cate, 15, page)
    blog_list = controller.get_cate_list(req, 'bw', 10)
    total = controller.get_cate_total(req, cate)
    total_page = fun.get_total_page(total, 20)
    return render_to_response("zhiyuw/category.html", locals(), context_instance = RequestContext(req))

def second_cate(req, cate):
    logo_image = fun.get_site_logo(req)
    packagelist = None
    cate_name = cate_dict.get(cate, '无效分类')
    blog_list = controller.get_cate_list(req, 'bw', 10)
    if cate:
        cate_list = controller.get_child_list(req, cate)
    return render_to_response("zhiyuw/second_cate.html", locals(), context_instance = RequestContext(req))

def gbook(req):
    logo_image = fun.get_site_logo(req)
    if req.method=="POST":
        data = fun.warp_data(req.POST)
        if not data.get('tel'):
            msg = '联系电话不能为空'
        elif not data['content']:
            msg = '内容不能为空'
        elif controller.post_gbook(req, data):
            msg = "提交成功"
        else:
            msg = "提交失败，请联系管理员"
        url = "/zhiyuw/gbook"
        return render_to_response("zhiyuw/msg.html", locals(), context_instance = RequestContext(req))
    else:
        cate_name = '留言栏'
        blog_list = controller.get_cate_list(req, 'bw', 10)
    return render_to_response("zhiyuw/gbook.html", locals(), context_instance = RequestContext(req))

def contact(req):
    logo_image = fun.get_site_logo(req)
    packagelist = None
    cate_name =  '联系我们'
    blog_list = controller.get_cate_list(req, 'bw', 10)
    return render_to_response("zhiyuw/contact_us.html", locals(), context_instance = RequestContext(req))

import time
def article(req, cate, id):
    art = controller.get_article(id)
    if not art:
        msg = '当前文章不存在或者未生效，请联系管理员'
        return render_to_response("zhiyuw/msg.html", locals(), context_instance = RequestContext(req))
    logo_image = fun.get_site_logo(req)
    packagelist = None
    cate_name = cate_dict.get(cate, '无效分类')
    blog_list = controller.get_cate_list(req, 'bw', 10)
    referer = req.path
    timestamp = int(time.time())
    comments = controller.get_comments(id)
    print cate
    pre_page, next_page = controller.get_context_page(req, cate, id)
    return render_to_response("zhiyuw/article.html", locals(), context_instance = RequestContext(req))

def login(req):
    logo_image = fun.get_site_logo(req)
    cate_name = '用户登录'
    if req.method=='GET':
        third_appid = qq_appid
        return render_to_response("zhiyuw/login.html", locals(), context_instance = RequestContext(req))
    elif req.method=='POST':
        data = fun.warp_data(req.POST)
        r = controller.auth(req, data)
        if r:
            # print r
            req.session['3rd_not_init'] = False
            req.session['isLogin'] = True
            req.session['info'] = r
            return HttpResponseRedirect("/members")
        else:
            msg = '用户或密码错误'
            return render_to_response("zhiyuw/msg.html", locals(), context_instance = RequestContext(req))

def logout(req):
    req.session['isLogin'] = False
    req.session['info'] = {}
    return HttpResponseRedirect("/zhiyuw")

def ydy(req):
    logo_image = fun.get_site_logo(req)
    cate_name = '用户注册'
    req.session['banner_list_ydy']  = global_settings['banner_list_ydy']
    req.session['settings'] = global_settings['settings']
    if req.method=='GET':
        express, express_id = controller.get_valid_code()
        fun.get_valid_code()
        third_appid = qq_appid
        return render_to_response("ydy.html", locals(), context_instance = RequestContext(req))

@request_login
def reg_yd(req):
    logo_image = fun.get_site_logo(req)
    if req.method=='GET':
        return render_to_response("zhiyuw/reg_yd.html", locals(), context_instance = RequestContext(req))

@valid_code
def register(req):
    logo_image = fun.get_site_logo(req)
    cate_name = '用户注册'
    if req.method=='GET':
        data = {}
        express, express_id = controller.get_valid_code()
        fun.get_valid_code()
        return render_to_response("zhiyuw/register.html", locals(), context_instance = RequestContext(req))
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
            # print r
            if r>0:
                info = controller.auth(req, data)
                req.session['isLogin'] = True
                req.session['info'] = info
                return render_to_response("zhiyuw/reg_yd.html", locals(), context_instance = RequestContext(req))
            else:
                msg = '该用户名或邮箱已注册,'
        express, express_id = controller.get_valid_code()
        fun.get_valid_code()
        return render_to_response("zhiyuw/register.html", locals(), context_instance = RequestContext(req))

def agreen(req):
    logo_image = fun.get_site_logo(req)
    cate_name = '用户注册'
    if req.method=='GET':
        agreen = controller.get_agreen()
        return render_to_response("zhiyuw/agreen.html", locals(), context_instance = RequestContext(req))

def search(req):
    logo_image = fun.get_site_logo(req)
    packagelist = None
    blog_list = controller.get_cate_list(req, 'bw', 10)
    kw = req.GET.get("kw")
    results = [{'url':'#', 'title':'搜索内容文章', 'username':'xwchen', 'update_date':'2015-06-13'},] *15
    results = controller.get_search_result(req, kw)
    return render_to_response("zhiyuw/search.html", locals(), context_instance = RequestContext(req))

def member(req):
    logo_image = fun.get_site_logo(req)
    data = fun.warp_data(req.GET)
    info = controller.get_user_info(data)
    article_list = controller.get_user_article(data, req)
    # add credits
    controller.add_count_history(req.session.get('info',{}).get('id','0'), 'hudie')
    return render_to_response("zhiyuw/member.html", locals(), context_instance = RequestContext(req))

@request_login
def comment(req):
    if req.method=='POST':
        data = fun.warp_data(req.POST)
        data['id'] = req.session.get('info',{}).get('id','0')
        if req.META.has_key('HTTP_X_FORWARDED_FOR'):
            data['ip'] =  req.META['HTTP_X_FORWARDED_FOR']
        else:
            data['ip'] = req.META['REMOTE_ADDR']
        # print data
        controller.add_comments(req, data)
        controller.add_count_history(req.session.get('info',{}).get('id','0'), 'comment')
        return HttpResponseRedirect(data.get('referer'))

def qiye_comment(req):
    if req.method=='GET':
        logo_image = fun.get_site_logo(req)
        data = fun.warp_data(req.GET)
        info = controller.get_user_info(data)
        controller.add_count(data['userid'], 'shuoshuo')
        controller.add_count_history(req.session.get('info',{}).get('id','0'), 'shuoshuo')
        return render_to_response("zhiyuw/qiye_comment.html", locals(), context_instance = RequestContext(req))
    elif req.method=='POST':
        data = fun.warp_data(req.POST)
        if req.META.has_key('HTTP_X_FORWARDED_FOR'):
            data['ip'] =  req.META['HTTP_X_FORWARDED_FOR']
        else:
            data['ip'] = req.META['REMOTE_ADDR']
        if controller.post_qiye_comment(req, data):
            msg = '提交说说成功'
        else:
            msg = '提交说说失败'
        return render_to_response("zhiyuw/msg.html", locals(), context_instance = RequestContext(req))

def guanzhu(req):
    result = {'errorCode':0, 'msg':''}
    if not req.session.get('isLogin'):
        result = {'errorCode':-1, 'msg':'你还未登录'}
        return HttpResponse(json.dumps(result),content_type="application/json")
    if req.method=='POST':
        data = fun.warp_data(req.POST)
        data['uid'] = req.session['info'].get('id', 0)
        # print data
        if not controller.has_complete_profile(data.get('uid')):
            result = {'errorCode':-2, 'msg':'请先完善个人资料中及履历表 '}
            return HttpResponse(json.dumps(result),content_type="application/json")
        r = controller.add_guanzhu(data)
        if r:
            controller.add_count(data['userid'], 'focus')
            controller.add_count_history(data['userid'], 'focus')
            return HttpResponse(json.dumps(result),content_type="application/json")
        else:
            result = {'errorCode':-3, 'msg':'已关注 '}
            return HttpResponse(json.dumps(result),content_type="application/json")

import datetime
def fgpassword(req):
    logo_image = fun.get_site_logo(req)
    if req.method=="GET":
        data = req.GET
        user_name = data.get('userName')
        sid = data.get('sid')
        if user_name and sid:
            r = controller.get_reset(user_name)
            d = datetime.datetime.now()
            if r.get('sid')==sid and r.get('ttl')>time.mktime(d.timetuple()):
                return render_to_response("zhiyuw/forgotpw3.html", locals(), context_instance = RequestContext(req))
            else:
                msg = "链接无效或已过期！"
                return render_to_response("zhiyuw/msg.html", locals(), context_instance = RequestContext(req))
        else:
            return render_to_response("zhiyuw/forgotpw.html", locals(), context_instance = RequestContext(req))
    if req.method=="POST":
        import uuid, hashlib
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
                    url = 'http://%s/zhiyuw/fgpassword?sid=%s&userName=%s' % (host, sid, email)
                    print url
                    send_reset_email(url, email)
                    email_pre = email.split('@')[0]
                    index = len(email_pre)/3
                    email_mix = email[:index]+'**'+email[index+2:]
                    return render_to_response("zhiyuw/forgotpw2.html", locals(), context_instance = RequestContext(req))
                else:
                    msg = '找回密码失败'
            else:
                msg = "无效的账户！"
            return render_to_response("zhiyuw/msg.html", locals(), context_instance = RequestContext(req))
        elif password:
            sid = data.get('sid')
            user_name = data.get('userName')
            r = controller.get_reset(user_name)
            d = datetime.datetime.now()
            if r.get('sid')==sid and r.get('ttl')>time.mktime(d.timetuple()):
                if controller.reset_passwd(password, user_name):
                    return render_to_response("zhiyuw/forgotpw4.html", locals(), context_instance = RequestContext(req))
                else:
                    msg = "密码更新失败"
            else:
                msg = "当前链接已过期！"
            return render_to_response("zhiyuw/msg.html", locals(), context_instance = RequestContext(req))
        else:
            msg = "访问无效！"
            return render_to_response("zhiyuw/msg.html", locals(), context_instance = RequestContext(req))

def baoming(req):
    data = req.POST
    login = data.get('login')
    if login=='true':
        uid = req.session['info'].get('id', 0)
        t = req.session['info'].get('utype', 0)
        if t=='ktq':
            result = {'errorCode':-2, 'msg':'开拓圈用户不可报名 '}
            return HttpResponse(json.dumps(result),content_type="application/json")
        data = {'t': t, 'userid':uid}
        info = controller.get_user_info(data)
        info['zhuanye'] = data.get('zhuanye')
        info['company'] = data.get('company')
        data = info
    if not data.get('name') or not data.get('phone'):
        result = {'errorCode':-1, 'msg':'参数不足'}
    else:
        r = controller.baoming(data)
        if r:
            result = {'errorCode':0, 'msg':'报名成功 '}
        else:
            result = {'errorCode':-1, 'msg':'报名失败 '}
    return HttpResponse(json.dumps(result),content_type="application/json")

def qq_login(req):
    if req.method=='GET':
        data = req.GET
        msg = '正在进行QQ登录操作，请稍后...'
        return render_to_response("zhiyuw/qq.html", locals(), context_instance = RequestContext(req))
    elif req.method=='POST':
        qq_info = req.POST
        print qq_info
        open_id = qq_info['openId']
        r = controller.is_3rd_exist(open_id)
        if r:
            if r.get('utype'):
                result = {'errorCode':0, 'msg':'成功 ', 'url':'/members'}
            else:
                result = {'errorCode':0, 'msg':'成功 ', 'url':'/zhiyuw/3rd_yd?uid=%s'%r.get('id')}
                req.session['3rd_not_init'] = True
        else:
            req.session['3rd_not_init'] = True
            uid = controller.add_3rd_user(req, qq_info ,'qq')
            result = {'errorCode':0, 'msg':'成功 ', 'url':'/zhiyuw/3rd_yd?uid=%s'% uid}
        info = controller.auth_3rd(req, open_id, 'qq')
        req.session['isLogin'] = True
        req.session['info'] = info
        return HttpResponse(json.dumps(result), content_type="application/json")

def weixin_login(req):
    from config import weixin_id, weixin_secret
    logo_image = fun.get_site_logo(req)
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
                page = '/members'
            else:
                page = '/zhiyuw/3rd_yd?uid=%s'%r.get('id')
                req.session['3rd_not_init'] = True
        else:
            req.session['3rd_not_init'] = True
            uid = controller.add_3rd_user(req, weixin_info ,'weixin')
            if uid:
                page = '/zhiyuw/3rd_yd?uid=%s'% uid
            else:
                msg = "绑定用户失败，该用户可能已经登录过，请联系管理员"
                return render_to_response("zhiyuw/msg.html", locals(), context_instance = RequestContext(req))
        info = controller.auth_3rd(req, unionid, 'weixin')
        if info:
            req.session['isLogin'] = True
            req.session['info'] = info
        return HttpResponseRedirect(page)

def third_yd(req):
    logo_image = fun.get_site_logo(req)
    if req.method=='GET':
        uid = req.GET.get('uid')
        return render_to_response("zhiyuw/3rd_yd.html", locals(), context_instance = RequestContext(req))
    elif req.method=='POST':
        data = req.POST
        print data
        if not data.get('uid') or data.get('uid')=='None':
            req.session['isLogin'] = False
            req.session['info'] = {}
            msg = '当前为非法提交'
            return render_to_response("zhiyuw/msg.html", locals(), context_instance = RequestContext(req))
        r = controller.bind_3rd_info(data)
        if r:
            req.session['3rd_not_init'] = False
            req.session['info']['utype'] = data.get('utype')
            print req.session['info']
            return render_to_response("zhiyuw/reg_yd.html", locals(), context_instance = RequestContext(req))
        else:
            msg = '手机或Email信息已绑定，添加信息失败。'
            url = '/zhiyuw/logout'
            return render_to_response("zhiyuw/msg.html", locals(), context_instance = RequestContext(req))
