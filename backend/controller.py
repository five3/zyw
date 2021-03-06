#encoding: utf-8
__author__ = 'macy'

from model import *
from zhiyuw import function as fun
import re

def get_cate_list():
    sql = '''select id, title
            from blog_blogcategory cate where parent_id is null'''
    catet = unio().fetchAll(sql)
    cate1 = []
    for i in catet:
        cate1.append(i)
        sql = '''select id, title from blog_blogcategory where parent_id=%s''' % i['id']
        # print sql
        catet2 = unio().fetchAll(sql)
        if catet2:
            items1 = [{'id': j['id'], 'title': '|----'+j['title']} for j in catet2]
            cate1.extend(items1)
    sql = '''select id, title, slug
            from ww_cate2'''
    cate2 = unio().fetchAll(sql)
    # print cate1
    return cate1, cate2

def get_post_info(id):
    sql = '''select post.id, post.title, post.featured_image, post.description, post.content, post.views, post.cate2, post.status, cate.id as cate
            from blog_blogpost post, blog_blogpost_categories blog_cate, blog_blogcategory cate
            where post.id=%s and post.id=blog_cate.blogpost_id and blog_cate.blogcategory_id=cate.id''' % id
    # print sql
    return unio().fetchOne(sql)

def get_post_list(req, page=1, num=10):
    index = (int(page)-1)*num
    sql = '''select post.id, post.title, post.short_url, post.status, post.content, post.views, post.cate2, post.status,
            post.created, cate.title as cate
            from blog_blogpost post, blog_blogpost_categories blog_cate, blog_blogcategory cate
            where post.site_id=%s and post.id=blog_cate.blogpost_id and blog_cate.blogcategory_id=cate.id
            order by post.created desc limit %s,%s''' % (fun.get_site_id(req), index, num)
    # print sql
    return unio().fetchAll(sql)

def save_post(req, data):
    id = data.get('id', 0)
    views = data.get('views')
    if not views:
        views = 0
    featured_image = data.get('featured_image')
    if not featured_image.strip():
        featured_image = '/static/zhiyuw/cy_images/images/infor.jpg'

    desc = data.get('description', '')
    if not desc:
        result, number  =  re .subn(r'<.*?>|</.*?>', '', data.get('editorValue'))
        desc = len(result)>20 and result[:20] or result
    if id:  ##update
        sql = '''update blog_blogpost set title='%s', featured_image='%s', description='%s', content='%s', status='%s', cate2='%s',
                created='%s', views='%s'
                where id=%s''' % (data.get('title'), featured_image, desc,
                                  data.get('editorValue'), data.get('status'), data.get('cate2'), fun.now(), views, id)
        # print sql
        r = unio().execute(sql)
        if r:
            sql = '''update blog_blogpost_categories set blogcategory_id=%s
                   where blogpost_id=%s''' % (data.get('cate'), id)
            unio().execute(sql)
            return r
    else:
        short_url = '/xx/xx'
        sql = '''insert into blog_blogpost (featured_image, description, comments_count, site_id, title, slug, created, status, publish_date,
                short_url, content, user_id, user_name, allow_comments, views, cate2)
                values ('%s', '%s', %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')''' % \
                  (featured_image, desc, 0, fun.get_site_id(req), data.get('title', 'no title'), data.get('title','no title'), fun.now(), data.get('status'),
                  fun.now(), short_url, data.get('editorValue'), 1, 'admin', 1, views, data.get('cate2'))
        # print sql
        lastid = unio().executeInsert(sql)
        if lastid:
            sql = '''insert blog_blogpost_categories (blogcategory_id, blogpost_id) values
                    ('%s', '%s')''' % (data.get('cate'), lastid)
            # print sql
            r = unio().executeInsert(sql)
        if r:
            sql = '''select slug from blog_blogcategory where id=%s''' % data.get('cate')
            r = unio().fetchOne(sql)
            slug = r.get('slug')
            short_url = '/zhiyuw/%s/show-%s.html' % (slug, lastid)
            mobile_url = '/mobile/%s/show-%s.html' % (slug, lastid)
            sql = '''update blog_blogpost set short_url='%s', mobile_url='%s' where id=%s''' %(short_url, mobile_url, lastid)
            return unio().execute(sql)


def del_post(id):
    sql = '''delete from blog_blogpost where id=%s''' % id
    r = unio().execute(sql)
    if not r:
        return None
    sql = '''delete from blog_blogpost_categories where blogpost_id=%s''' % id
    return unio().execute(sql)


def get_comment_list(req, page=1, num=10):
    index = (int(page)-1)*num
    sql = '''select id, comment, user_name, submit_date
            from django_comments
            where is_removed=0 and site_id=%s order by submit_date desc limit %s,%s''' % (fun.get_site_id(req), index, num)
    return unio().fetchAll(sql)


def get_comment_info(id):
    sql = '''select id, comment from django_comments where id=%s''' % id
    return unio().fetchOne(sql)


def save_comment(data):
    id = data.get('id')
    comment = data.get('comment', 'no content')
    if id:
        sql = '''update django_comments set comment='%s' where id=%s''' % (comment, id)
        return unio().execute(sql)
    else:
        sql = ''''''


def del_comment(id):
    sql = '''update django_comments set is_removed=1 where id=%s''' % id
    return unio().execute(sql)


def get_gbook_list(req, page, num=10):
    if page:
        page = int(page)
    else:
        page = 1
    index = (page-1)*num
    sql = '''select id, name, tel, created from ww_gbook where site_id=%s limit %s,%s''' % (fun.get_site_id(req), index, num)
    # print sql
    return unio().fetchAll(sql)

def get_baoming_list(req, page, num=10):
    if page:
        page = int(page)
    else:
        page = 1
    index = (page-1)*num
    sql = '''select * from ww_baoming where 1=1 order by id DESC limit %s,%s''' % (index, num)
    # print sql
    return unio().fetchAll(sql)

def del_gbook(id):
    sql = '''delete from ww_gbook where id=%s''' % id
    return unio().execute(sql)


def get_gbook_info(id):
    sql = '''select name, tel, content from ww_gbook where id=%s''' % id
    r = unio().fetchOne(sql)
    return '''<div class="Murphy fl">
             <div class="Murphy_list fl"><strong>用户名称</strong><p>%s</p></div>
             <div class="Murphy_list fl"><strong>联系方式</strong><p>%s人</p></div>
             <div class="Murphy_list fl"><strong>留言内容</strong><p>%s</p></div></div>''' % (
            r['name'], r['tel'], r['content'])

def warp_privileges(privileges):
    d = {}
    for i in privileges:
        if i.get('parent', 0):
            parent_id = i['parent']
            if parent_id in d:
                d[parent_id].get('child').append(i)
        else:
            i['child'] = []
            d[i['id']] = i
    return d

def auth(req, data):
    from django.contrib.auth import authenticate, login
    username = data.get('username')
    password = data.get('password')
    user = authenticate(username=username, password=password)
    if user and user.is_active:
        login(req, user)
        if user.is_superuser:
            privileges = get_privileges()
        else:
            privileges = get_user_privileges(user.id)
        req.session['privileges'] = warp_privileges(privileges)
        return True


def get_user_list(req, page, num=10, keys=None):
    if page:
        page = int(page)
    else:
        page = 1
    index = (page-1)*num

    if keys:
        where = ' and (username like "%%' + keys + '%%" or n.shoujihao="'+keys+'") '
        sql = '''select a.id, username, a.created, regip, a.status, a.utype
                from ww_member a, ww_member_normal n
                where (a.id=n.id) and a.site_id=%s %s order by a.created desc limit %s,%s''' % (
                 fun.get_site_id(req), where, index, num)
        # print sql
        r = unio().fetchAll(sql)
        if r and len(r)>0:
            return r

        where = ' and (username like "%%' + keys + '%%" or v.lianxifangshi="'+keys+'") '
        sql = '''select a.id, username, a.created, regip, a.status, a.utype
                from ww_member a, ww_member_vip v
                where (a.id=v.id) and a.site_id=%s %s order by a.created desc limit %s,%s''' % (
                 fun.get_site_id(req), where, index, num)
        # print sql
        return unio().fetchAll(sql)
    else:
        where = ' and 1=1 '
        sql = '''select a.id, username, a.created, regip, a.status, a.utype
                from ww_member a
                where a.site_id=%s %s order by a.created desc limit %s,%s''' % (
                 fun.get_site_id(req), where, index, num)
        # print sql
        return unio().fetchAll(sql)

def get_admin_list(req, page, num=10):
    if page:
        page = int(page)
    else:
        page = 1
    index = (page-1)*num
    sql = '''select id, username, date_joined, is_active, email from auth_user where is_staff=1 order by date_joined desc limit %s,%s''' % (
        index, num)
    # print sql
    return unio().fetchAll(sql)


def get_admin_pages(req, num=10):
    sql = '''select count(id) as pages from auth_user where is_staff=1'''
    # print sql
    pages = unio().fetchOne(sql)
    if pages:
        count = pages['pages']
        if count % num==0:
            return count/num
        else:
            return count/num+1
    else:
        return 1


def get_user_pages(req, num=10):
    sql = '''select count(id) as pages from ww_member where site_id=%s''' % fun.get_site_id(req)
    print sql
    pages = unio().fetchOne(sql)
    if pages:
        count = pages['pages']
        if count % num==0:
            return count/num
        else:
            return count/num+1
    else:
        return 1


def audit_user(id, action):
    if action=='pass':
        status = 1
    else:
        status = 0
    sql = '''update ww_member set status=%s where id=%s''' % (status, id)
    # print sql
    return unio().execute(sql)


def audit_admin(id, action):
    if action=='pass':
        status = 1
    else:
        status = 0
    sql = '''update auth_user set is_active=%s where id=%s''' % (status, id)
    # print sql
    return unio().execute(sql)


def reset_user_passwd(id):
    md5 = fun.mk_md5('000000')
    sql = '''update ww_member set password='%s' where id=%s''' % (md5, id)
    # print sql
    return unio().execute(sql)


def reset_admin_passwd(id):
    md5 = fun.mk_md5('000000')
    sql = '''update auth_user set password='%s' where id=%s''' % (md5, id)
    # print sql
    return unio().execute(sql)

def update_admin_passwd(id, username, old, new):
    from django.contrib.auth import authenticate
    user = authenticate(username=username, password=old)
    print user
    if user and user.is_active:
        user.set_password(new)
        user.save()
        return user
        # sql = '''update auth_user set password='%s' where id=%s and password='%s';''' % (new, id, old)
        # print sql
        # return unio().execute(sql)


def audit_post(data):
    sql = '''update blog_blogpost set status='%s' where id=%s''' % (data.get('status',1),data.get('id',0))
    # print sql
    if unio().execute(sql):
        return {'msg': 'success', 'errorCode' : 0}
    else:
        return {'msg': 'fail', 'errorCode' : -1}

def get_user_privileges(uid):
    sql = '''select a.id, a.parent, a.name, a.value, a.icon from ww_privilege a, ww_user_privilege b
            where b.user_id=%s and b.privilege_id=a.id ''' % uid
    # print sql
    return unio().fetchAll(sql)

def get_privileges():
    sql = '''select a.id, a.parent, a.name, a.value, a.icon from ww_privilege a'''
    # print sql
    return unio().fetchAll(sql)

def delete_user_privileges(id):
    sql = '''delete from ww_user_privilege where user_id=%s''' % id
    # print sql
    return unio().execute(sql)

def add_user_privileges(id, privileges):
    sql = '''insert into ww_user_privilege (user_id, privilege_id, created) values '''
    for i in privileges:
        sql += '(%s, %s, now()),' % (id, i)
    print sql
    return unio().execute(sql[:-1])

def get_user_info(data):
    t = data.get('t')
    if t=='ktq':
        sql = '''select username, email, nickname, logo, utype,
                qiyeming, qiyewangzhi, lianxifangshi, qiyejianjie, zhuanye, zhuti
                from ww_member, ww_member_vip
                where ww_member.id=%s and ww_member.id=ww_member_vip.id''' % data.get('userid')
    else:
        sql = '''select username, email, nickname, logo, utype,
                xingming, shoujihao, qq, weixin, linkedin, zuoyouming, gerenjianjie, zhiwei, sex
                from ww_member, ww_member_normal
                where ww_member.id=%s and ww_member.id=ww_member_normal.id''' % data.get('userid')
    # print sql
    return unio().fetchOne(sql)


def add_admin(post):
    name = post.get('name')
    password = post.get('password')
    email = post.get('email')
    sql = '''insert into auth_user (first_name, last_name, username, password, date_joined, last_login, is_active, is_staff, is_superuser, email) VALUES ('', '', '%s', '%s', now(), now(), 0, 1, 0, '%s');''' % (name, fun.mk_md5(password), email)
    # print sql
    try:
        if unio().execute(sql):
            return True
    except:
        pass


def get_settings():
    sql = '''SELECT * FROM ww_setting where 1=1'''
    # print sql
    try:
        return unio().fetchOne(sql)
    except:
        pass


def update_setting(post):
    title = post.get('title')
    keywords = post.get('keywords')
    desc = post.get('desc')
    copyright = post.get('copyright')
    friend_link = post.get('friend_link')
    sql = '''UPDATE ww_setting SET title='%s', keywords='%s', `desc`='%s', copyright='%s', friend_link='%s' where 1=1''' % (title, keywords, desc, copyright, friend_link)
    # print sql
    try:
        if unio().execute(sql):
            return True
    except:
        pass

def get_banners():
    sql = '''SELECT * FROM ww_banner where 1=1'''
    # print sql
    try:
        return unio().fetchAll(sql)
    except:
        pass


def del_banner(id):
    sql = '''DELETE FROM ww_banner where id=%s''' % id
    # print sql
    try:
        return unio().execute(sql)
    except:
        pass


def add_banner(url, file_path, t):
    src = '/static' + file_path.split('static')[1].replace('\\', '/')
    sql ='''INSERT INTO ww_banner (src, url, t) VALUES ('%s', '%s', '%s')''' % (src, url, t)
    # print sql
    try:
        return unio().execute(sql)
    except:
        pass

def save_banner(id, url, file_path, t):
    src = '/static' + file_path.split('static')[1].replace('\\', '/')
    sql ='''UPDATE ww_banner SET src='%s', url='%s', t='%s' WHERE id='%s';''' % (src, url, t, id)
    print sql
    try:
        return unio().execute(sql)
    except:
        pass

def save_content(data):
    short_url = '/xx/xx'
    sql = '''insert into blog_blogpost (featured_image, description, comments_count, site_id, title, slug, created, status, publish_date,
            short_url, content, user_id, user_name, allow_comments, views, cate2, reference)
            values ('%s', '%s', %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')''' % \
              (data.get('featured_image', '/static/zhiyuw/cy_images/images/infor.jpg'), data.get('description'),
               0, 1, data.get('title'), data.get('title'), fun.now(), 2,
              fun.now(), short_url, data.get('content', '').replace("'", "\\'"), 0, 'auto', 1, 0, '', data.get('reference', ''))
    # print sql
    try:
        lastid = unio().executeInsert(sql)
    except Exception, e:
        print e, e.message
        return
    print lastid
    if lastid:
        sql = '''insert blog_blogpost_categories (blogcategory_id, blogpost_id) values
                ('%s', '%s')''' % (data.get('cate'), lastid)
        # print sql
        try:
            r = unio().executeInsert(sql)
        except Exception, e:
            print e.message
            return
    if r:
        sql = '''select slug from blog_blogcategory where id=%s''' % data.get('cate')
        # print sql
        r = unio().fetchOne(sql)
        slug = r.get('slug')
        short_url = '/zhiyuw/%s/show-%s.html' % (slug, lastid)
        mobile_url = '/mobile/%s/show-%s.html' % (slug, lastid)
        sql = '''update blog_blogpost set short_url='%s', mobile_url='%s' where id=%s''' %(short_url, mobile_url, lastid)
        return unio().execute(sql)

def get_agreen():
    sql = '''SELECT content FROM ww_agreen where 1=1'''
    # print sql
    return unio().fetchOne(sql)

def update_agreen(content):
    sql = '''UPDATE ww_agreen SET content='%s' where 1=1''' % content
    # print sql
    return unio().execute(sql)

def get_fav(limit=6):
    sql = '''SELECT id, name, url FROM ww_navigate_admin where 1=1 limit %s''' % limit
    # print sql
    return unio().fetchAll(sql)

def update_fav(data):
    sql = '''UPDATE ww_navigate_admin SET name='%s', url='%s' where id=%s''' % (data.get('name'), data.get('url'), data.get('id'))
    # print sql
    return unio().execute(sql)

def add_fav(data):
    sql = '''INSERT INTO ww_navigate_admin (name, url, created) VALUES ('%s', '%s', now())''' % (data.get('name'), data.get('url'))
    # print sql
    return unio().execute(sql)

def del_fav(id):
    sql = '''DELETE FROM ww_navigate_admin where id=%s''' % id
    # print sql
    return unio().execute(sql)

def get_user_data(account):
    sql = '''SELECT ww_count.* FROM ww_count,ww_member
            WHERE ww_member.email='%s' AND ww_member.id=ww_count.uid''' % account
    print sql
    return unio().fetchOne(sql)

def update_user_data(data):
    sql = '''UPDATE ww_count
            SET article=%s, comment=%s, shuoshuo=%s, money=%s, focus=%s
            WHERE uid=%s''' % (data['article'], data['comment'], data['shuoshuo'], data['money'],  data['focus'], data['uid'])
    print sql
    return unio().execute(sql)

