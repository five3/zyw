#！encoding: utf-8

from django.shortcuts import render_to_response
from config import position_imgs as pimg,settings as st
import controller
import function as fun
from django.http import HttpResponseRedirect
from django.template import RequestContext

def index(req):
    # print req.session['site_host']
    position_imgs = pimg
    settings = st
    logo_image = fun.get_site_logo(req)
    xxc_list = controller.get_cate_list(req, 'xxc', 12)
    tzl_list = controller.get_cate_list(req, 'tzl', 12)
    ktq_list = controller.get_ktq_list(req, 10)
    alh_list = controller.get_alh_list(req, 12)
    fsb_list = controller.get_fsb_list(req, 12)
    bw_list = controller.get_cate_list(req, 'bw', 12)
    gyq_list = controller.get_gyq_list(req, 10)
    return render_to_response("zhiyuw/index.html", locals(), context_instance = RequestContext(req))

def kaituoqquan(req):
    position_imgs = pimg
    settings = st
    logo_image = fun.get_site_logo(req)
    packagelist = None
    ktq_list = [{'id': 1, 'zhuti': '主题名1', 'logo':'/static/uploadfiles/image/20150525/thumb_287a08c4865fda9bd348cfac4bf0b090.jpg', 'qiyeming':'企业名称', 'qiye_url':"#", 'credits':'新兵蛋', 'hangye':'财务', 'desc':'企业简介描述，不超过200字'},
                {'id': 2, 'zhuti': '百度一下，你就', 'logo':'/static/uploadfiles/image/20150526/bd_logo1.png', 'qiyeming':'百度', 'qiye_url':"http://www.baidu.com", 'credits':'老鸟单', 'hangye':'财务', 'desc':'企业简介描述，不超过200字'}] * 5
    name = req.GET.get('name')
    page = req.GET.get('page', 1)
    if page:
        page = int(page)
    else:
        page = 1
    if page<1:
        ktq_list = []
    elif name:
        prepage = 'name=%s&page=%s' % (name, page-1)
        nextpage = 'name=%s&page=%s' % (name, page+1)
        ktq_list = controller.get_ktq_list(req, 20, name, page)
    else:
        prepage = 'page=%s' % (page-1,)
        nextpage = 'page=%s' % (page+1,)
        ktq_list = controller.get_ktq_list(req, 20, name, page)
    return render_to_response("zhiyuw/ktq.html", locals(), context_instance = RequestContext(req))

def gengyunqun(req):
    position_imgs = pimg
    settings = st
    logo_image = fun.get_site_logo(req)
    packagelist = None
    name = req.GET.get('name')
    page = req.GET.get('page', 1)
    if page:
        page = int(page)
    else:
        page = 1
    if page<1:
        gyq_list = []
    elif name:
        prepage = 'name=%s&page=%s' % (name, page-1)
        nextpage = 'name=%s&page=%s' % (name, page+1)
        gyq_list = controller.get_gyq_list(req, 20, name, page)
    else:
        prepage = 'page=%s' % (page-1,)
        nextpage = 'page=%s' % (page+1,)
        gyq_list = controller.get_gyq_list(req, 20, name, page)
    return render_to_response("zhiyuw/gyq.html", locals(), context_instance = RequestContext(req))

cate_dict = {'alh':'案例汇','xxc':'信息窗','zyk':'资源库','bw':'博文', 'fsb':'放松吧','nxt':'纳贤台',
             'lxwm':'联系我们','lyl':'留言栏', 'tzl':'通知栏', 'sh':'书画', 'sy':'摄影', 'bjys':'保健养生',
             'wxjl':'文学交流', 'ylxw':'娱乐新闻', 'zxmk':'招贤模块', 'zjmk':'自荐模块', 'rlzx':'人力资讯'}
cate_dict = controller.get_cate_dict()

def category(req, cate):
    page = req.GET.get('page', 1)
    position_imgs = pimg
    settings = st
    logo_image = fun.get_site_logo(req)
    packagelist = None
    cate_name = cate_dict.get(cate, '无效分类')
    cate_list = controller.get_cate_list(req, cate, 15, page)
    blog_list = controller.get_cate_list(req, 'bw', 10)
    return render_to_response("zhiyuw/category.html", locals(), context_instance = RequestContext(req))

def second_cate(req, cate):
    position_imgs = pimg
    settings = st
    logo_image = fun.get_site_logo(req)
    packagelist = None
    cate_name = cate_dict.get(cate, '无效分类')
    blog_list = controller.get_cate_list(req, 'bw', 10)
    if cate:
        cate_list = controller.get_child_list(req, cate)
    return render_to_response("zhiyuw/second_cate.html", locals(), context_instance = RequestContext(req))

def gbook(req):
    position_imgs = pimg
    settings = st
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
    position_imgs = pimg
    settings = st
    logo_image = fun.get_site_logo(req)
    packagelist = None
    cate_name =  '联系我们'
    blog_list = controller.get_cate_list(req, 'bw', 10)
    return render_to_response("zhiyuw/contact_us.html", locals(), context_instance = RequestContext(req))

import time
def article(req, cate, id):
    position_imgs = pimg
    settings = st
    logo_image = fun.get_site_logo(req)
    packagelist = None
    cate_name = cate_dict.get(cate, '无效分类')
    blog_list = controller.get_cate_list(req, 'bw', 10)
    art = controller.get_article(id)
    refer = req.path
    timestamp = int(time.time())
    comments = controller.get_comments(id)
    pre_page, next_page = controller.get_context_page(req, cate, id)
    return render_to_response("zhiyuw/article.html", locals(), context_instance = RequestContext(req))

def login(req):
    position_imgs = pimg
    settings = st
    logo_image = fun.get_site_logo(req)
    cate_name = '用户登录'
    if req.method=='GET':
        return render_to_response("zhiyuw/login.html", locals(), context_instance = RequestContext(req))
    elif req.method=='POST':
        data = fun.warp_data(req.POST)
        r = controller.auth(req, data)
        if r:
            print r
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

def register(req):
    position_imgs = pimg
    settings = st
    logo_image = fun.get_site_logo(req)
    cate_name = '用户注册'
    if req.method=='GET':
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
                msg = '注册用户成功，你现在可以登录了'
            else:
                msg = '该用户名或邮箱已注册,'
        return render_to_response("zhiyuw/msg.html", locals(), context_instance = RequestContext(req))

def search(req):
    position_imgs = pimg
    settings = st
    logo_image = fun.get_site_logo(req)
    packagelist = None
    blog_list = controller.get_cate_list(req, 'bw', 10)
    kw = req.GET.get("kw")
    results = [{'url':'#', 'title':'搜索内容文章', 'username':'xwchen', 'update_date':'2015-06-13'},] *15
    results = controller.get_search_result(req, kw)
    return render_to_response("zhiyuw/search.html", locals(), context_instance = RequestContext(req))

def member(req):
    position_imgs = pimg
    settings = st
    logo_image = fun.get_site_logo(req)
    data = fun.warp_data(req.GET)
    info = controller.get_user_info(data)
    article_list = controller.get_user_article(data)
    return render_to_response("zhiyuw/member.html", locals(), context_instance = RequestContext(req))

def comment(req):
    data = fun.warp_data(req.POST)
    data['id'] = req.session.get('info',{}).get('id','0')
    if req.META.has_key('HTTP_X_FORWARDED_FOR'):
        data['ip'] =  req.META['HTTP_X_FORWARDED_FOR']
    else:
        data['ip'] = req.META['REMOTE_ADDR']
    # print data
    controller.add_comments(req, data)
    return HttpResponseRedirect(data.get('referrer'))

def qiye_comment(req):
    if req.method=='GET':
        position_imgs = pimg
        settings = st
        logo_image = fun.get_site_logo(req)
        data = fun.warp_data(req.GET)
        info = controller.get_user_info(data)
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