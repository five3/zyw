#encoding: utf-8
__author__ = 'macy'

from model import *
import function as fun

# def get_site_id():
#     return SITE_ID

def get_fsb_list(req, n):
    sql = '''select post.title, short_url as url, user_name, created
            from blog_blogpost post, blog_blogpost_categories cate, blog_blogcategory blog_category
            where post.status=2 and post.site_id=%s and blog_category.slug in ('bjys','wxjl', 'ylxw', 'sh', 'sy', 'fsb') and cate.blogcategory_id=blog_category.id
            and cate.blogpost_id=post.id order by updated desc limit 0,%s;''' % (fun.get_site_id(req),n)
    # print sql
    return unio().fetchAll(sql)

def get_alh_list(req, n):
    sql = '''select post.title, short_url as url, user_name, created
            from blog_blogpost post, blog_blogpost_categories cate, blog_blogcategory blog_category
            where post.status=2 and post.site_id=%s and blog_category.slug in ('zuzhi','geren', 'qtalh', 'alh') and cate.blogcategory_id=blog_category.id
            and cate.blogpost_id=post.id order by updated desc limit 0,%s;''' % (fun.get_site_id(req),n)
    # print sql
    return unio().fetchAll(sql)
	
def get_cate_list(req, cate, n, page=1):
    if not page:
        page = 1
    else:
        page = int(page)
    if page<1:
        return []
    index = (page-1)*n
    sql = '''select post.title, short_url as url, user_name, created
            from blog_blogpost post, blog_blogpost_categories cate, blog_blogcategory blog_category
            where post.status=2 and post.site_id=%s and blog_category.slug='%s' and cate.blogcategory_id=blog_category.id
            and cate.blogpost_id=post.id order by updated desc limit %s,%s;''' % (fun.get_site_id(req), cate, index, n)
    # print sql
    return unio().fetchAll(sql)

def get_article(id):
    sql = '''update blog_blogpost set views=views+1 where id=%s''' % id
    unio().execute(sql)

    sql = '''select id, title, content, user_id, user_name, created, allow_comments,views
            from blog_blogpost post
            where id=%s''' % id
    # print sql
    r = unio().fetchOne(sql)
    if r:
        sql = '''update ww_member set credits=credits+1 where id=%s''' % r['user_id']
        unio().execute(sql)

    return r

def get_context_page(req, cate, id):
    sql = '''select post.title, short_url
            from blog_blogpost post, blog_blogpost_categories cate, blog_blogcategory
            where blog_blogcategory.slug='%s' and blog_blogcategory.id=cate.blogcategory_id
            and cate.blogpost_id=post.id and post.site_id=%s and post.id<%s order by post.id desc limit 0,1''' % \
          (cate, fun.get_site_id(req), id)
    # print sql
    pre_page = unio().fetchOne(sql)
    sql = '''select post.title, short_url
            from blog_blogpost post, blog_blogpost_categories cate, blog_blogcategory
            where blog_blogcategory.slug='%s' and blog_blogcategory.id=cate.blogcategory_id
            and cate.blogpost_id=post.id and post.site_id=%s and post.id>%s limit 0,1''' % \
          (cate, fun.get_site_id(req), id)
    # print sql
    next_page = unio().fetchOne(sql)
    return pre_page, next_page

def get_ktq_list(req, n, zhuanye=None, page=1):
    index = (page-1)*n
    if zhuanye:
        sql = '''select vip.id, ww_member.logo, utype, zhuti, qiyeming, qiyewangzhi as url,qiyejianjie,ww_zhuanye.desc as zhuanye,
                ww_member.credits, vip.qiyejianjie
            from ww_member_vip vip, ww_member, ww_zhuanye
            where ww_member.status=1 and ww_member.site_id=%s and vip.zhuanye='%s' and vip.id=ww_member.id and ww_zhuanye.name=vip.zhuanye
             order by id desc limit %s,%s''' % (fun.get_site_id(req), zhuanye, index, n)
    else:
        sql = '''select vip.id, ww_member.logo, utype, zhuti, qiyeming, qiyewangzhi as url,qiyejianjie,ww_zhuanye.desc as zhuanye,
                ww_member.credits, vip.qiyejianjie
            from ww_member_vip vip, ww_member, ww_zhuanye
            where ww_member.status=1 and ww_member.site_id=%s and vip.id=ww_member.id and ww_zhuanye.name=vip.zhuanye
             order by vip.id desc limit %s,%s''' % (fun.get_site_id(req), index, n)
    # print sql
    rs = unio().fetchAll(sql)
    return fun.convert_dengji_list(*rs)

def get_gyq_list(req, n, zhiwei=None, page=1):
    index = (page-1)*n
    if zhiwei:
        sql = '''select ww_member.id, utype,ww_zhiwei.desc as zhiwei,ww_member.logo,ww_member.nickname,
                ww_member.credits, normal.zuoyouming
                from ww_member_normal normal,ww_member,ww_zhiwei
                where ww_member.status=1 and ww_member.site_id=%s and normal.zhiwei='%s' and ww_member.id=normal.id and ww_zhiwei.name=normal.zhiwei
                    order by normal.id desc limit %s,%s''' % (fun.get_site_id(req), zhiwei, index, n)
    else:
        sql = '''select ww_member.id, utype,ww_zhiwei.desc as zhiwei,ww_member.logo,ww_member.nickname,
                ww_member.credits, normal.zuoyouming
                from ww_member_normal normal,ww_member,ww_zhiwei
                where ww_member.status=1 and ww_member.site_id=%s and ww_member.id=normal.id and ww_zhiwei.name=normal.zhiwei
                    order by normal.id desc limit %s,%s''' % (fun.get_site_id(req), index, n)
    # print sql
    rs = unio().fetchAll(sql)
    return fun.convert_dengji_list(*rs)

def get_search_result(req, kw):
    sql = '''select short_url as url, title, user_name, updated
            from blog_blogpost
            where post.status=2 and site_id='''+ str(fun.get_site_id(req)) +''' and title like '%%'''+kw+"%%'"
    # print sql
    return unio().fetchAll(sql)

def post_gbook(req, data):
    sql = '''insert into ww_gbook (name, tel, content, created, status, site_id)
            values ('%s', '%s', '%s', '%s', 1, %s)''' % \
          (data['name'],data['tel'],data['content'].replace('\r\n', '<br>'), fun.now(), fun.get_site_id(req))
    # print sql
    return unio().execute(sql)

def get_child_list(req, cate):
    sql = '''select b.id, b.title, b.slug
            from blog_blogcategory a, blog_blogcategory b
            where a.slug='%s' and a.id=b.parent_id order by b.ord''' % cate
    cate_list = unio().fetchAll(sql)
    d = []
    for i in cate_list:
        sql = '''select d.short_url as url,d.title, d.user_name, d.updated
                from blog_blogpost_categories c, blog_blogpost d
                where d.status=2 and d.site_id=%s and c.blogcategory_id=%s and c.blogpost_id=d.id
                order by d.updated desc limit 0,10''' % (fun.get_site_id(req), i['id'])
        d.append({'title':i['title'], 'more':i['slug'], 'cate_list':unio().fetchAll(sql)})
    return d

def auth(req, data):
    username = data.get('username')
    password = data.get('password')
    sql = '''select password,id,nickname,username,utype,email,bgmusic,credits,logo from ww_member where site_id=%s and username='%s'
        ''' % (fun.get_site_id(req), username)
    # print sql
    r = unio().fetchOne(sql)
    if not r:
        return None
    if r.pop('password')==fun.mk_md5(password):
        sql = '''update ww_member set credits=credits+1 where id=%s''' % r['id']
        unio().execute(sql)
        return fun.convert_dengji_list(r)[0]

def reg_user(req, data):
    if data['utype']=='gyq':
        logo = '/static/zhiyuw/cy_images/images/gengyunqun.png'
    else:
        logo = '/static/zhiyuw/cy_images/images/kaituoquan.png'
    sql = '''insert into ww_member (username, nickname, password, email, logo, created, regip, status, utype, site_id, bgmusic, credits)
            values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', 0, '%s', %s, '%s', 1)
            ''' % (data['username'], data['username'], fun.mk_md5(data['password']), data['email'], logo, fun.now(), data['ip'], data['utype'], fun.get_site_id(req), '/static/members/cy_images/music/gohome.mp3')
    try:
        r = unio().executeInsert(sql)
        if not r:
            return -2
        if data['utype']=='gyq':
            sql = '''insert into ww_member_normal (id) values (%s)''' % r
            return unio().execute(sql)
        elif data['utype']=='ktq':
            sql = '''insert into ww_member_vip (id) values (%s)''' % r
            return unio().execute(sql)
    except:
        return -2

def add_comments(req, data):
    sql = '''update blog_blogpost set comments_count=comments_count+1 where id=%s''' % data.get('object_pk')
    if unio().execute(sql)<0:
        return False
    sql = '''insert into django_comments (content_type_id, object_pk, site_id, user_id, user_name,
            user_email, user_url, comment, submit_date, ip_address, is_public, is_removed) values
            (14, '%s', %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', 1, 0)''' % (data['object_pk'], fun.get_site_id(req), data['id'], data['name'], data['email'], data['url'], data['comment'], fun.now(), data['ip'])
    # print sql
    if unio().execute(sql)<0:
        return False
    return True

utype = {'ktq':'开拓圈', 'gyq':'耕耘群'}
def get_user_info(data):
    uid = data.get('userid')
    t = data.get('t')
    if not uid or not t:
        return {}
   # print t
    if t=='gyq':	
		sql = '''select ww_member.id, username, utype, nickname,email,credits,ww_member.logo,ww_member_normal.xingming as name
		        from ww_member, ww_member_normal
		        where ww_member.id=%s and ww_member.id=ww_member_normal.id''' % uid
    elif t=='ktq':
		sql = '''select ww_member.id, username, utype, nickname,email,credits,vip.qiyejianjie,ww_member.logo, vip.qiyeming as name
				from ww_member,ww_member_vip vip 
				where ww_member.id=%s and ww_member.id=vip.id''' % uid

    # print sql
    r = unio().fetchOne(sql)
    # print r
    if r:
        return fun.convert_dengji_list(r)[0]
    else:
        return {}

def get_user_article(data, req):
    sql = '''select post.title, short_url as url, user_name, created
            from blog_blogpost post
            where post.site_id=%s and post.status=2 and post.user_id=%s order by updated desc limit 0,%s;''' % (fun.get_site_id(req), data.get('userid',0), 10)
    # print sql
    return unio().fetchAll(sql)

def get_comments(id):
    sql = '''select user_url,user_name,submit_date,comment
            from django_comments
            where object_pk=%s and is_removed=0''' % (id,)
    # print sql
    return unio().fetchAll(sql)

def get_cate_dict():
    sql = '''select slug, title from blog_blogcategory'''
    l = unio().fetchAll(sql)
    d = {}
    for i in l:
        d[i['slug']] = i['title']
    return d

def post_qiye_comment(req, data):
    sql = '''insert into ww_qiye_comment (qiye_id, user_name, user_type, lianxi, qianbao, shuoshuo, created, ip, site_id) values
            ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')''' % (data['qiye_id'], data['user_name'], data['user_type'], data['lianxi'], data['qianbao'],
                                               data['shuoshuo'].replace('\r\n', '<br>'), fun.now(), data['ip'], fun.get_site_id(req))
    # print sql
    return unio().execute(sql)
