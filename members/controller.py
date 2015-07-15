#encoding: utf-8
__author__ = 'macy'

from model import *
from zhiyuw import function as fun

def get_cate_list():
    sql = '''select id, title
            from blog_blogcategory cate'''
    cate1 = unio().fetchAll(sql)
    sql = '''select id, title, slug
            from ww_cate2'''
    cate2 = unio().fetchAll(sql)
    return cate1, cate2

def get_post_info(id):
    sql = '''select post.id, post.title, post.content, post.views, post.cate2, post.status, cate.id as cate
            from blog_blogpost post, blog_blogpost_categories blog_cate, blog_blogcategory cate
            where post.id=%s and post.id=blog_cate.blogpost_id and blog_cate.blogcategory_id=cate.id''' % id
    # print sql
    return unio().fetchOne(sql)

def get_post_list(req, uid, cate=None, page=1, num=10):
    if page<1:
        return []
    if cate:
        condition = ' post.cate2="%s" and ' % cate
    else:
        condition = ''
    index = (int(page)-1)*num
    sql = '''select post.id, post.title, short_url, post.content, post.views, post.cate2, post.status,
            post.created, cate.title as cate
            from blog_blogpost post, blog_blogpost_categories blog_cate, blog_blogcategory cate
            where %s post.user_id=%s and post.site_id=%s and post.id=blog_cate.blogpost_id and blog_cate.blogcategory_id=cate.id
            order by post.created desc limit %s,%s''' % (condition, uid, fun.get_site_id(req), index, num)
    # print sql
    return unio().fetchAll(sql)

def save_post(req, data, uid, uname):
    id = data.get('id', 0)
    views = data.get('views')
    if not views:
        views = 0
    if id:  ##update
        sql = '''update blog_blogpost set title='%s', content='%s', status='%s', cate2='%s',
                updated='%s', views='%s'
                where id=%s''' % (data.get('title'), data.get('editorValue'),
                                  data.get('status'), data.get('cate2'), fun.now(), views, id)
        # print sql
        r = unio().execute(sql)
        if r:
            sql = '''update blog_blogpost_categories set blogcategory_id=%s
                   where blogpost_id=%s''' % (data.get('cate'), id)
            unio().execute(sql)
        return r
    else:
        short_url = '/zhiyuw/%s/show-%s.html' % ('xxx',0)
        sql = '''insert into blog_blogpost (comments_count, site_id, title, slug, created, status, publish_date,
                short_url, content, user_id, user_name, allow_comments, views, cate2)
                values (%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')''' % \
                  (0, fun.get_site_id(req), data.get('title', 'no title'), data.get('title','no title'), fun.now(), data.get('status'),
                  fun.now(), short_url, data.get('editorValue'), uid, uname, 1, views, data.get('cate2'))
        # print sql
        lastid = unio().executeInsert(sql)
        if lastid:
            sql = '''insert blog_blogpost_categories (blogcategory_id, blogpost_id) values
                    ('%s', '%s')''' % (data.get('cate'), lastid)
            # print sql
            r =unio().executeInsert(sql)
        if r:
            sql = '''select slug from blog_blogcategory where id=%s''' % data.get('cate')
            r = unio().fetchOne(sql)
            slug = r.get('slug')
            short_url = '/zhiyuw/%s/show-%s.html' % (slug, lastid)
            sql = '''update blog_blogpost set short_url='%s' where id=%s''' %(short_url, lastid)
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

def set_bg_music(src, uid):
    sql = '''update ww_member set bgmusic='%s' where id=%s;''' % (src, uid)
    # print sql
    return unio().execute(sql)

def set_password(data, uid):
    old = data.get('old')
    new = data.get('new')
    sql = '''select password from ww_member where id=%s''' % uid
    r = unio().fetchOne(sql)
    if r:
        if r.get('password')==fun.mk_md5(old):
            sql = '''update ww_member set password='%s' where id=%s''' % (fun.mk_md5(new), uid)
            return unio().execute(sql)

def update_profile(data, utype, uid):
    if utype=='ktq':
        sql = '''update ww_member_vip set logo='%s', qiyeming='%s', lianxifangshi='%s', qiyewangzhi='%s',
                qiyejianjie='%s', zhuanye='%s', zhuti='%s'
                where id=%s''' % (data.get('photo_img'), data.get('qiyeming'), data.get('lianxifangshi'),
                                  data.get('qiyewangzhi'), data.get('qiyejianjie'), data.get('zhuanye','qt'),
                                  data.get('zhuti'), uid)
        # print sql
        return unio().execute(sql)>-1
    elif utype=='gyq':
        sql = '''update ww_member set nickname='%s', avatar='%s' where id=%s''' % \
              (data.get('nickname'), data.get('photo_img'), uid)
        # print sql
        unio().execute(sql)
        sql = '''update ww_member_normal set xingming='%s', shoujihao='%s', zuoyouming='%s', qq='%s',
               gerenjianjie='%s', zhiwei='%s', sex='%s' where id=%s''' % (data.get('xingming'), data.get('shoujihao'),
                 data.get('zuoyouming'), data.get('qq'), data.get('gerenjianjie'), data.get('zhiwei'),
                 data.get('sex'), uid)
        # print sql
        return unio().execute(sql)>-1

def get_profile(uid, utype):
    if utype=='ktq':
        sql = '''select logo as photo_img, qiyeming, qiyewangzhi, lianxifangshi, qiyejianjie, zhuanye, zhuti
                from ww_member_vip where id=%s''' % uid
        # print sql
        return unio().fetchOne(sql)
    elif utype=='gyq':
        sql = '''select m.nickname, m.avatar as photo_img, n.xingming, n.shoujihao, n.zuoyouming, n.qq, n.gerenjianjie,
                n.zhiwei, n.sex from ww_member m, ww_member_normal n
                where m.id=%s and m.id=n.id''' % uid
        # print sql
        return unio().fetchOne(sql)

def get_zhuanye_list():
    sql = '''select name, `desc` from ww_zhuanye where `desc` is not null'''
    # print sql
    return unio().fetchAll(sql)

def get_zhiwei_list():
    sql = '''select name, `desc` from ww_zhiwei where `desc` is not null'''
    # print sql
    return unio().fetchAll(sql)

def update_photo_img(url, utype, uid):
    if utype=='ktq':
        sql = '''update ww_member_vip set logo='%s' where id=%s''' % (url, uid)
        # print sql
        return unio().execute(sql)
    elif utype=='gyq':
        sql = '''update ww_member set avatar='%s' where id=%s''' % (url, uid)
        # print sql
        return unio().execute(sql)

def post_zhaopin(data, uid, uname):
    data['cate'] = 15
    data['cate2'] = '*'
    data['status'] = 2
    companyname = data.pop('companyname')
    zhaopingangwei = data.pop('zhaopingangwei')
    zhaopinrenshu = data.pop('zhaopinrenshu')
    lianxifangshi = data.pop('lianxifangshi')
    gangweiyaoqiu = data.pop('gangweiyaoqiu').replace('\r\n', '<br/>')
    relatelink = data.pop('relatelink')
    # print `gangweiyaoqiu`
    data['editorValue'] = '''<div class="Murphy fl"><div class="Murphy_list fl"><strong>公司名称</strong><p>%s</p></div>
    <div class="Murphy_list fl"><strong>招聘岗位</strong><p>%s</p></div><div class="Murphy_list fl">
    <strong>招聘人数</strong><p>%s人</p></div>
    <div class="Murphy_list fl"><strong>岗位要求</strong><p>%s</p></div>
    <div class="Murphy_list fl"><strong>联系方式</strong><p>%s</p></div>
    <div class="Murphy_list fl"><strong>相关链接</strong><p><a href="%s" target="_blank">%s</a></p></div>
    </div>''' % (
        companyname, zhaopingangwei, zhaopinrenshu, gangweiyaoqiu, lianxifangshi, relatelink, relatelink)
    return save_post(data, uid, uname)

def get_shuoshuo_list(uid, page, num=10):
    if page:
        page = int(page)
    else:
        page = 1
    index = (page-1)*num
    sql = '''select id, user_name, user_type, lianxi, created
            from ww_qiye_comment where qiye_id=%s and is_show>-1 limit %s,%s''' % (uid, index, num)
    # print sql
    return unio().fetchAll(sql)

def get_qiye_comment(id):
    sql = '''select id, user_name, user_type, lianxi, qianbao, shuoshuo, created
            from ww_qiye_comment where id=%s''' % id
    # print sql
    r = unio().fetchOne(sql)
    return '''<div class="Murphy fl">
             <div class="Murphy_list fl"><strong>用户名称</strong><p>%s</p></div>
             <div class="Murphy_list fl"><strong>用户类型</strong><p>%s</p></div>
             <div class="Murphy_list fl"><strong>联系方式</strong><p>%s人</p></div>
             <div class="Murphy_list fl"><strong>微信钱包</strong><p>%s</p></div>
             <div class="Murphy_list fl"><strong>说说内容</strong><p>%s</p></div></div>''' %  (r['user_name'], r['user_type'],
                                    r['lianxi'], r['qianbao'], r['shuoshuo'])

def del_qiye_comment(id):
    sql = '''update ww_qiye_comment set is_show=-1 where id=%s''' % id
    return unio().execute(sql)