#encoding: utf-8
__author__ = 'macy'

from model import *
import function as fun

def get_site_id():
    return 1

def get_fsb_list(n):
    sql = '''select post.title, short_url as url, user_name, created
            from blog_blogpost post, blog_blogpost_categories cate, blog_blogcategory blog_category
            where post.site_id=%s and blog_category.slug in ('bjys','wxjl', 'ylxw', 'sh', 'sy') and cate.blogcategory_id=blog_category.id
            and cate.blogpost_id=post.id order by updated desc limit 0,%s;''' % (get_site_id(),n)
    # print sql
    return unio().fetchAll(sql)

def get_alh_list(n):
    sql = '''select post.title, short_url as url, user_name, created
            from blog_blogpost post, blog_blogpost_categories cate, blog_blogcategory blog_category
            where post.site_id=%s and blog_category.slug in ('zuzhi','geren', 'qtalh') and cate.blogcategory_id=blog_category.id
            and cate.blogpost_id=post.id order by updated desc limit 0,%s;''' % (get_site_id(),n)
    # print sql
    return unio().fetchAll(sql)
	
def get_cate_list(cate, n, page=1):
    if not page:
        page = 1
    else:
        page = int(page)
    if page<1:
        return []
    index = (page-1)*n
    sql = '''select post.title, short_url as url, user_name, created
            from blog_blogpost post, blog_blogpost_categories cate, blog_blogcategory blog_category
            where post.site_id=%s and blog_category.slug='%s' and cate.blogcategory_id=blog_category.id
            and cate.blogpost_id=post.id order by updated desc limit %s,%s;''' % (get_site_id(), cate, index, n)
    # print sql
    return unio().fetchAll(sql)

def get_article(id):
    sql = '''select id, title, content, user_name, created, allow_comments,views
            from blog_blogpost post
            where id=%s''' % id
    # print sql
    return unio().fetchOne(sql)

def get_context_page(cate, id):
    sql = '''select post.title, short_url
            from blog_blogpost post, blog_blogpost_categories cate, blog_blogcategory
            where blog_blogcategory.slug='%s' and blog_blogcategory.id=cate.blogcategory_id
            and cate.blogpost_id=post.id and post.site_id=%s and post.id<%s order by post.id desc limit 0,1''' % \
          (cate, get_site_id(), id)
    # print sql
    pre_page = unio().fetchOne(sql)
    sql = '''select post.title, short_url
            from blog_blogpost post, blog_blogpost_categories cate, blog_blogcategory
            where blog_blogcategory.slug='%s' and blog_blogcategory.id=cate.blogcategory_id
            and cate.blogpost_id=post.id and post.site_id=%s and post.id>%s limit 0,1''' % \
          (cate, get_site_id(), id)
    # print sql
    next_page = unio().fetchOne(sql)
    return pre_page, next_page

def get_ktq_list(n, zhuanye=None):
    if zhuanye:
        sql = '''select vip.id, logo, zhuti, qiyeming, qiyewangzhi as url,qiyejianjie,ww_zhuanye.desc as zhuanye,
                ww_member.credits, vip.qiyejianjie
            from ww_member_vip vip, ww_member, ww_zhuanye
            where ww_member.site_id=%s and vip.zhuanye='%s' and vip.id=ww_member.id and ww_zhuanye.name=vip.zhuanye
             order by id desc limit 0,%s''' % (get_site_id(), zhuanye, n)
    else:
        sql = '''select vip.id, logo, zhuti, qiyeming, qiyewangzhi as url,qiyejianjie,ww_zhuanye.desc as zhuanye,
                ww_member.credits, vip.qiyejianjie
            from ww_member_vip vip, ww_member, ww_zhuanye
            where ww_member.site_id=%s and vip.id=ww_member.id and ww_zhuanye.name=vip.zhuanye
             order by id desc limit 0,%s''' % (get_site_id(), n,)
    # print sql
    return unio().fetchAll(sql)

def get_gyq_list(n, zhiwei=None):
    if zhiwei:
        sql = '''select ww_member.id,ww_zhiwei.desc as zhiwei,ww_member.avatar as logo,ww_member.nickname,
                ww_member.credits, normal.zuoyouming
                from ww_member_normal normal,ww_member,ww_zhiwei
                where ww_member.site_id=%s and normal.zhiwei='%s' and ww_member.id=normal.id and ww_zhiwei.name=normal.zhiwei
                    order by normal.id desc limit 0,%s''' % (get_site_id(), zhiwei, n)
    else:
        sql = '''select ww_member.id,ww_zhiwei.desc as zhiwei,ww_member.avatar as logo,ww_member.nickname,
                ww_member.credits, normal.zuoyouming
                from ww_member_normal normal,ww_member,ww_zhiwei
                where ww_member.site_id=%s and ww_member.id=normal.id and ww_zhiwei.name=normal.zhiwei
                    order by normal.id desc limit 0,%s''' % (get_site_id(), n)
    # print sql
    return unio().fetchAll(sql)

def get_search_result(kw):
    sql = '''select short_url as url, title, user_name, updated
            from blog_blogpost
            where site_id='''+ get_site_id() +''' and title like '%%'''+kw+"%%'"
    # print sql
    return unio().fetchAll(sql)

def post_gbook(data):
    data['addtime'] = int(time.time())
    sql = '''insert into ww_gbook (name, tel, content, addtime, status, site_id)
            values ('%s', '%s', '%s', '%s', 1, %s)''' % \
          (data['name'],data['tel'],data['content'],data['addtime'], get_site_id())
    # print sql
    return unio().execute(sql)

def get_child_list(cate):
    sql = '''select b.id, b.title, b.slug
            from blog_blogcategory a, blog_blogcategory b
            where a.slug='%s' and a.id=b.parent_id order by b.ord''' % cate
    cate_list = unio().fetchAll(sql)
    d = []
    for i in cate_list:
        sql = '''select d.short_url as url,d.title, d.user_name, d.updated
                from blog_blogpost_categories c, blog_blogpost d
                where d.site_id=%s and c.blogcategory_id=%s and c.blogpost_id=d.id
                order by d.updated desc limit 0,10''' % (get_site_id(), i['id'])
        d.append({'title':i['title'], 'more':i['slug'], 'cate_list':unio().fetchAll(sql)})
    return d


def auth(data):
    username = data.get('username')
    password = data.get('password')
    sql = '''select password,id,nickname,username,utype,email,bgmusic from ww_member where site_id=%s and username='%s'
        ''' % (get_site_id(), username)
    # print sql
    r = unio().fetchOne(sql)
    if not r:
        return None
    if r.pop('password')==fun.mk_md5(password):
        sql = '''update ww_member set credits=credits+1 where id=%s''' % r['id']
        unio().execute(sql)
        return r

from django.db.utils import IntegrityError
def reg_user(data):
    sql = '''insert into ww_member (username, nickname, password, email, avatar, regdate, regip, status, utype, site_id, bgmusic)
            values ('%s', '%s', '%s', '%s', '/static/zhiyuw/cy_images/images/gengyunqun.png', '%s', '', 1, '%s', %s, '%s')
            ''' % (data['username'], data['username'], fun.mk_md5(data['password']), data['email'], int(time.time()), data['utype'], get_site_id(), '/static/members/cy_images/music/gohome.mp3')
    try:
        r = unio().executeInsert(sql)
        if not r:
            return -2
        if data['utype']=='gyq':
            sql = '''insert into ww_member_normal (id) values (%s)''' % r
            return unio().executeInsert(sql)
        elif data['utype']=='ktq':
            sql = '''insert into ww_member_vip (id, logo) values (%s, '%s')''' % (r, '/static/zhiyuw/cy_images/images/kaituoquan.png')
            return unio().executeInsert(sql)
    except:
        return -2

def add_comments(data):
    sql = '''update blog_blogpost set comments_count=comments_count+1 where id=%s''' % data.get('object_pk')
    if unio().execute(sql)<0:
        return False
    sql = '''insert into django_comments (content_type_id, object_pk, site_id, user_id, user_name,
            user_email, user_url, comment, submit_date, ip_address, is_public, is_removed) values
            (14, '%s', %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', 1, 0)''' % (data['object_pk'], get_site_id(), data['id'], data['name'], data['email'], data['url'], data['comment'], fun.now(), data['ip'])
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
#    print t	
    if t=='gyq':	
		sql = '''select id,nickname,email,credits,avatar as logo from ww_member where id=%s''' % uid
    elif t=='ktq':
		sql = '''select ww_member.id,nickname,email,credits,vip.qiyejianjie,vip.logo
				from ww_member,ww_member_vip vip 
				where ww_member.id=%s and ww_member.id=vip.id''' % uid

    # print sql
    r = unio().fetchOne(sql)
#    print r		
    if r:
        r['utype'] = utype[t]
    return r

def get_user_article(data):
    sql = '''select post.title, short_url as url, user_name, created
            from blog_blogpost post
            where post.user_id=%s order by updated desc limit 0,%s;''' % (data.get('userid',0), 10)
    # print sql
    return unio().fetchAll(sql)

def get_comments(id):
    sql = '''select user_url,user_name,submit_date,comment
            from django_comments
            where object_pk=%s;''' % (id,)
    # print sql
    return unio().fetchAll(sql)

def get_cate_dict():
    sql = '''select slug, title from blog_blogcategory'''
    l = unio().fetchAll(sql)
    d = {}
    for i in l:
        d[i['slug']] = i['title']
    return d

def post_qiye_comment(data):
    sql = '''insert into ww_qiye_comment (qiye_id, user_name, user_type, lianxi, qianbao, shuoshuo, created) values
            ('%s', '%s', '%s', '%s', '%s', '%s', '%s')''' % (data['qiye_id'], data['user_name'], data['user_type'], data['lianxi'], data['qianbao'],
                                               data['shuoshuo'].replace('\r\n', '<br>'), fun.now())
    # print sql
    return unio().execute(sql)
