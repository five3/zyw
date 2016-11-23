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
            msg = '你需要登录才能发表评论'
            return render_to_response("mobile/msg.html", locals(), context_instance = RequestContext(req))
        if (args):
            return func(req, *args)
        else:
            return func(req)
    return __warp

def index(req):
    # print req.session['site_host']
    req.session['banner_list']  = global_settings['banner_list']
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

def second_cate(req, cate):
    logo_image = fun.get_site_logo(req)
    packagelist = None
    cate_name = cate_dict.get(cate, '无效分类')
    if cate:
        cate_list = controller.get_child_list(req, cate)
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
            # print r
            if r>0:
                msg = '注册用户成功，你现在可以登录了'
            else:
                msg = '该用户名或邮箱已注册,'
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

def xiangwang(req):
    logo_image = fun.get_site_logo(req)
    packagelist = None
    cate_name =  '我的书咖'
    blog_list = controller.get_cate_list(req, 'bw', 10)
    return render_to_response("mobile/xiangwang.html", locals(), context_instance = RequestContext(req))

@request_login
def navigate(req):
    uid = req.session['info']['id']
    utype = req.session['info']['utype']
    data = {'userid':uid, 't':utype}
    info = controller.get_user_info(data)
    if req.method=='GET':
        return render_to_response("mobile/navigate.html", locals(), context_instance = RequestContext(req))

def tianchi(req):
    logo_image = fun.get_site_logo(req)
    packagelist = None
    cate_name =  '我的财富'
    blog_list = controller.get_cate_list(req, 'bw', 10)
    return render_to_response("mobile/caifu.html", locals(), context_instance = RequestContext(req))

def pinpai(req):
    logo_image = fun.get_site_logo(req)
    packagelist = None
    cate_name =  '我的财富'
    blog_list = controller.get_cate_list(req, 'bw', 10)
    return render_to_response("mobile/caifu.html", locals(), context_instance = RequestContext(req))

def caifu(req):
    logo_image = fun.get_site_logo(req)
    packagelist = None
    cate_name =  '我的财富'
    blog_list = controller.get_cate_list(req, 'bw', 10)
    return render_to_response("mobile/caifu.html", locals(), context_instance = RequestContext(req))





