#encoding: utf-8
__author__ = 'macy'

from model import *
import function as fun
from datetime import date
# def get_site_id():
#     return SITE_ID
def get_nxt_list(req, n):
    sql = '''select post.title, short_url as url, mobile_url, user_name, created, description, featured_image
            from blog_blogpost post, blog_blogpost_categories cate, blog_blogcategory blog_category
            where post.status=2 and post.site_id=%s and blog_category.slug in ('zjmk','zxmk', 'rlzx', 'nxt') and cate.blogcategory_id=blog_category.id
            and cate.blogpost_id=post.id order by updated desc limit 0,%s;''' % (fun.get_site_id(req),n)
    # print sql
    return unio().fetchAll(sql)

def get_fsb_list(req, n):
    sql = '''select post.title, short_url as url, mobile_url, user_name, created, description, featured_image
            from blog_blogpost post, blog_blogpost_categories cate, blog_blogcategory blog_category
            where post.status=2 and post.site_id=%s and blog_category.slug in ('bjys','wxjl', 'ylxw', 'sh', 'sy', 'fsb') and cate.blogcategory_id=blog_category.id
            and cate.blogpost_id=post.id order by updated desc limit 0,%s;''' % (fun.get_site_id(req),n)
    # print sql
    return unio().fetchAll(sql)

def get_alh_list(req, n):
    sql = '''select post.title, short_url as url, mobile_url, user_name, created, description, featured_image
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
    sql = '''select post.title, short_url as url, mobile_url, user_name, created, description, featured_image
            from blog_blogpost post, blog_blogpost_categories cate, blog_blogcategory blog_category
            where post.status=2 and post.site_id=%s and blog_category.slug='%s' and cate.blogcategory_id=blog_category.id
            and cate.blogpost_id=post.id order by created desc limit %s,%s;''' % (fun.get_site_id(req), cate, index, n)
    # print sql
    return unio().fetchAll(sql)

def get_cate_total(req, cate):
    sql = '''select count(post.title) as total
            from blog_blogpost post, blog_blogpost_categories cate, blog_blogcategory blog_category
            where post.status=2 and post.site_id=%s and blog_category.slug='%s' and cate.blogcategory_id=blog_category.id
            and cate.blogpost_id=post.id''' % (fun.get_site_id(req), cate)
    # print sql
    rt = unio().fetchOne(sql)
    if rt:
        return rt['total']
    else:
        return 1


def get_article(id):
    sql = '''select id, title, content, user_id, user_name, created, allow_comments,views
            from blog_blogpost post
            where id=%s and status=2''' % id
    # print sql
    r = unio().fetchOne(sql)
    if r:
        sql = '''update ww_member set credits=credits+1 where id=%s''' % r['user_id']
        unio().execute(sql)

        sql = '''update blog_blogpost set views=views+1 where id=%s''' % id
        unio().execute(sql)

        sql = '''INSERT INTO ww_count_history (uid, hudie, created) VALUES (%s, 1, '%s')
                ON DUPLICATE KEY UPDATE hudie=hudie+1;''' % (r['user_id'], date.today())
        unio().execute(sql)

    return r

def get_context_page(req, cate, id):
    sql = '''select post.title, short_url, mobile_url
            from blog_blogpost post, blog_blogpost_categories cate, blog_blogcategory
            where blog_blogcategory.slug='%s' and blog_blogcategory.id=cate.blogcategory_id
            and cate.blogpost_id=post.id and post.site_id=%s and post.id<%s order by post.id desc limit 0,1''' % \
          (cate, fun.get_site_id(req), id)
    # print sql
    pre_page = unio().fetchOne(sql)
    sql = '''select post.title, short_url, mobile_url
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

def get_ktq_total(req, zhuanye=None):
    if zhuanye:
        sql = '''select count(vip.id) as total
            from ww_member_vip vip, ww_member, ww_zhuanye
            where ww_member.status=1 and ww_member.site_id=%s and vip.zhuanye='%s' and vip.id=ww_member.id and ww_zhuanye.name=vip.zhuanye
            ''' % (fun.get_site_id(req), zhuanye)
    else:
        sql = '''select count(vip.id) as total
            from ww_member_vip vip, ww_member, ww_zhuanye
            where ww_member.status=1 and ww_member.site_id=%s and vip.id=ww_member.id and ww_zhuanye.name=vip.zhuanye
             ''' % (fun.get_site_id(req))
    # print sql
    rt = unio().fetchOne(sql)
    if rt:
        return rt['total']
    else:
        return 1


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

def get_gyq_total(req, zhiwei=None):
    if zhiwei:
        sql = '''select count(ww_member.id) as total
                from ww_member_normal normal,ww_member,ww_zhiwei
                where ww_member.status=1 and ww_member.site_id=%s and normal.zhiwei='%s' and ww_member.id=normal.id and ww_zhiwei.name=normal.zhiwei
                ''' % (fun.get_site_id(req), zhiwei)
    else:
        sql = '''select count(ww_member.id) as total
                from ww_member_normal normal,ww_member,ww_zhiwei
                where ww_member.status=1 and ww_member.site_id=%s and ww_member.id=normal.id and ww_zhiwei.name=normal.zhiwei
                ''' % (fun.get_site_id(req))
    # print sql
    rt = unio().fetchOne(sql)
    if rt:
        return rt['total']
    else:
        return 1

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
        sql = '''select d.short_url as url, d.mobile_url, d.title, d.description, d.user_name, d.updated, d.featured_image
                from blog_blogpost_categories c, blog_blogpost d
                where d.status=2 and d.site_id=%s and c.blogcategory_id=%s and c.blogpost_id=d.id
                order by d.updated desc limit 0,10''' % (fun.get_site_id(req), i['id'])
        d.append({'title':i['title'], 'more':i['slug'], 'cate_list':unio().fetchAll(sql)})
    return d

def auth_3rd(req, openid, utype):
    sql = '''select password,id,nickname,username,utype,email,bgmusic,credits,logo
            from ww_member
            where site_id=%s and 3rd_id='%s' and 3rd_type='%s';''' % (fun.get_site_id(req), openid, utype)
    print sql
    r = unio().fetchOne(sql)
    if r:
        sql = '''update ww_member set credits=credits+1 where id=%s''' % r['id']
        unio().execute(sql)
        return fun.convert_dengji_list(r)[0]

def auth(req, data):
    username = data.get('username')
    password = data.get('password')
    sql = '''select password,id,nickname,username,utype,email,bgmusic,credits,logo
            from ww_member
            where site_id=%s and (username='%s' or email='%s')
        ''' % (fun.get_site_id(req), username, username)
    # print sql
    r = unio().fetchOne(sql)
    # print r
    if not r:
        sql = '''select password,ww_member.id,nickname,username,utype,email,bgmusic,credits,logo
                from ww_member, ww_member_normal
                where site_id=%s and ww_member.id=ww_member_normal.id and ww_member_normal.shoujihao='%s'
            ''' % (fun.get_site_id(req), username)
        # print sql
        r = unio().fetchOne(sql)
    if r and r.pop('password')==fun.mk_md5(password):
        sql = '''update ww_member set credits=credits+1 where id=%s''' % r['id']
        unio().execute(sql)
        return fun.convert_dengji_list(r)[0]

def add_3rd_user(req, info, third_type):
    if third_type=='qq':
        openid = info['openId']
        logo = info['figureurl_qq_2']
        username = openid
        password = info['nickname']
    elif third_type=='weixin':
        openid = info['unionid']
        logo = info['headimgurl']
        username = openid
        password = info['nickname']
    print username
    utype = ''
    email = openid + '@qq.com'
    if req.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip =  req.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = req.META['REMOTE_ADDR']
    site_id = fun.get_site_id(req)
    bg_music = '/static/members/cy_images/music/gohome.mp3'
    sql = '''insert into ww_member (3rd_id, 3rd_type, username, nickname, password, email, logo,
                                    created, regip, status, utype, site_id, bgmusic, credits)
            values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', 0, '%s', %s, '%s', 1)
            ''' % (openid, third_type, username, username, password, email, logo,
                   fun.now(), ip, utype, site_id, bg_music)
    # print sql
    try:
        return unio().executeInsert(sql)
    except Exception, e:
        print e
        return None

def reg_user(req, data):
    if data['utype']=='gyq':
        logo = '/static/zhiyuw/cy_images/images/gengyunqun.png'
    else:
        logo = '/static/zhiyuw/cy_images/images/kaituoquan.png'
    sql = '''insert into ww_member (username, nickname, password, email, logo, created, regip, status, utype, site_id, bgmusic, credits)
            values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', 0, '%s', %s, '%s', 1)
            ''' % (data['username'], data['username'], fun.mk_md5(data['password']), data['email'], logo, fun.now(), data['ip'], data['utype'], fun.get_site_id(req), '/static/members/cy_images/music/gohome.mp3')
    # print sql
    try:
        r = unio().executeInsert(sql)
        if not r:
            return -1
        if data['utype']=='gyq':
            sql = '''insert into ww_member_normal (id, shoujihao) values (%s, '%s')''' % (r, data['phone'])
            r2 = unio().execute(sql)
        elif data['utype']=='ktq':
            sql = '''insert into ww_member_vip (id, lianxifangshi) values (%s, '%s')''' % (r, data['phone'])
            r2 = unio().execute(sql)
        if r2:
            sql = '''INSERT INTO ww_count (uid) VALUES (%s)''' % r
            return unio().execute(sql)

    except Exception, e:
        print e
        return -2

def add_comments(req, data):
    sql = '''update blog_blogpost set comments_count=comments_count+1 where id=%s''' % data.get('object_pk')
    if unio().execute(sql)<0:
        return False
    sql = '''insert into django_comments (content_type_id, object_pk, site_id, user_id, user_name,
            user_email, user_url, comment, submit_date, ip_address, is_public, is_removed) values
            (14, '%s', %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', 1, 0)''' % (data['object_pk'], fun.get_site_id(req), data['id'], data['name'], data['email'], data.get('url',''), data['comment'], fun.now(), data['ip'])
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
        sql = '''select ww_member.id, qq, weixin, linkedin,username, utype, nickname,email,credits,ww_member.logo,ww_member_normal.xingming as name,shoujihao as phone,zhiwei as zhuanye,sex
		        from ww_member, ww_member_normal
		        where ww_member.id=%s and ww_member.id=ww_member_normal.id''' % uid
    elif t=='ktq':
        sql = '''select ww_member.id, username, qiyewangzhi, utype, nickname,email,credits,vip.qiyejianjie,ww_member.logo, vip.qiyeming as name
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

def get_valid_code():
    exp, val = fun.get_valid_code()
    sql = '''INSERT INTO ww_valid_code (express, value) VALUES ('%s', '%s')''' % (exp, val)
    # print sql
    rt = unio().executeInsert(sql)
    if rt:
        return exp, rt
    else:
        return '8*8', 1

def validation_code(code_id):
    if not code_id.strip():
        return
    sql = '''SELECT value FROM ww_valid_code WHERE id=%s''' % code_id
    print sql
    rt = unio().fetchOne(sql)
    if rt:
        return rt.get('value')

def get_agreen():
    sql = '''SELECT content FROM ww_agreen WHERE 1=1'''
    # print sql
    rt = unio().fetchOne(sql)
    if rt:
        return rt.get('content')
    else:
        ''

def add_count(uid, label, num=1):
    sql = '''INSERT INTO ww_count (uid, %s) VALUES (%s, 1)
            ON DUPLICATE KEY UPDATE %s=%s+(%s);''' % (label, uid, label, label, num)
    print sql
    return unio().execute(sql)

def add_count_history(uid, label, num=1):
    sql = '''INSERT INTO ww_count_history (uid, %s, created) VALUES (%s, 1, '%s')
            ON DUPLICATE KEY UPDATE %s=%s+%s;''' % (label, uid, date.today(), label, label, num)
    return unio().execute(sql)

def add_guanzhu(data):
    sql = '''INSERT INTO ww_guanzhu (cid, pid) VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE pid=%s;''' % (data.get('userid'), data.get('uid'), data.get('uid'))
    # print sql
    return unio().execute(sql)

def get_email_by_account(account):
    account = account.replace(' ', '')
    sql = '''SELECT email FROM ww_member WHERE (username='%s' or email='%s') and status=1;''' % (account, account)
    # print sql
    r = unio().fetchOne(sql)
    if r:
        return r['email']

def add_reset(email, sid, ttl):
    sql = '''UPDATE ww_reset SET status=0 where email='%s';''' % email
    unio().execute(sql)
    sql = '''INSERT INTO ww_reset (email, sid, ttl, status) VALUES ('%s', '%s', '%s', '1')''' % (email, sid, ttl)
    # print sql
    return unio().executeInsert(sql)

def get_reset(email):
    sql = '''SELECT sid, ttl FROM ww_reset WHERE email='%s' and status=1''' % email
    # print sql
    return unio().fetchOne(sql)

def reset_passwd(passwd, user_name):
    sql = '''UPDATE ww_member SET password='%s' WHERE email='%s' AND status=1''' % (fun.mk_md5(passwd), user_name)
    # print sql
    return unio().execute(sql)

def baoming(data):
    sql = '''INSERT INTO ww_baoming (name, sex, phone, zhuanye, zhiwei, company, created) VALUES
            ('%s','%s','%s','%s','%s','%s',now())''' % (data.get('name'), data.get('sex'),
                        data.get('phone'), data.get('zhuanye'), data.get('zhiwei'), data.get('company'))
    # print sql
    return unio().executeInsert(sql)

def is_3rd_exist(uid):
    sql = '''SELECT id,utype FROM ww_member WHERE 3rd_id='%s';''' % uid
    print sql
    return unio().fetchOne(sql)

def bind_3rd_info(data):
    utype = data.get('utype')
    phone = data.get('phone')
    email = data.get('email')
    uid = data.get('uid')
    sql = '''UPDATE ww_member SET utype='%s',email='%s',status=1 WHERE id='%s';''' % (utype, email, uid)
    try:
        r = unio().execute(sql)
        # print r
        if utype=='gyq':
            sql = '''insert into ww_member_normal (id, shoujihao) values (%s, '%s')''' % (uid, phone)
        elif utype=='ktq':
            sql = '''insert into ww_member_vip (id, lianxifangshi) values (%s, '%s')''' % (uid, phone)
        print sql
        r2 = unio().execute(sql)
        # print r2
        if r2:
            sql = '''INSERT INTO ww_count (uid) VALUES (%s)''' % uid
            print sql
            return unio().executeInsert(sql)
    except Exception,e:
        print e
        return None
