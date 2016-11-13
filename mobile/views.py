#！encoding: utf-8

from django.shortcuts import render_to_response
from zhiyuw.config import global_settings, reset_setting
from zhiyuw import controller
import zhiyuw.function as fun
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render

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
        if req.method=='POST':
            if not req.session.get('isLogin'):
                msg = '你需要登录才能发表评论'
                return render_to_response("zhiyuw/msg.html", locals(), context_instance = RequestContext(req))
            ret = func(req)
            return ret
        else:
            msg = '请求方法不支持'
            return render_to_response("zhiyuw/msg.html", locals(), context_instance = RequestContext(req))

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
    return render_to_response("mobile/index.html", locals(), context_instance = RequestContext(req))

def article(req):
    logo_image = fun.get_site_logo(req)
    packagelist = None
    cate_name =  '我的文章'
    blog_list = controller.get_cate_list(req, 'bw', 10)
    return render_to_response("mobile/article.html", locals(), context_instance = RequestContext(req))

def caifu(req):
    logo_image = fun.get_site_logo(req)
    packagelist = None
    cate_name =  '我的财富'
    blog_list = controller.get_cate_list(req, 'bw', 10)
    return render_to_response("mobile/caifu.html", locals(), context_instance = RequestContext(req))

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
    blog_list = controller.get_cate_list(req, 'bw', 10)
    total = controller.get_cate_total(req, cate)
    total_page = fun.get_total_page(total, 20)
    return render_to_response("mobile/list.html", locals(), context_instance = RequestContext(req))

def navigate(req):
    logo_image = fun.get_site_logo(req)
    packagelist = None
    cate_name =  '我的导航'
    blog_list = controller.get_cate_list(req, 'bw', 10)
    return render_to_response("mobile/navigate.html", locals(), context_instance = RequestContext(req))

def post(req):
    logo_image = fun.get_site_logo(req)
    packagelist = None
    cate_name =  '发布文章'
    blog_list = controller.get_cate_list(req, 'bw', 10)
    return render_to_response("mobile/post.html", locals(), context_instance = RequestContext(req))

def shuka(req):
    logo_image = fun.get_site_logo(req)
    packagelist = None
    cate_name =  '我的书咖'
    blog_list = controller.get_cate_list(req, 'bw', 10)
    return render_to_response("mobile/shuka.html", locals(), context_instance = RequestContext(req))

def register(req):
    logo_image = fun.get_site_logo(req)
    packagelist = None
    cate_name =  '我的书咖'
    blog_list = controller.get_cate_list(req, 'bw', 10)
    return render_to_response("mobile/register.html", locals(), context_instance = RequestContext(req))

def login(req):
    logo_image = fun.get_site_logo(req)
    packagelist = None
    cate_name =  '我的书咖'
    blog_list = controller.get_cate_list(req, 'bw', 10)
    return render_to_response("mobile/signin.html", locals(), context_instance = RequestContext(req))


