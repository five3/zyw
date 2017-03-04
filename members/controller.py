#encoding: utf-8
__author__ = 'macy'

from model import *
from zhiyuw import function as fun
from zhiyuw import controller as controller2
from datetime import date

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
    sql = '''select post.id, post.title, post.content, post.views, post.cate2, cate3, post.status, cate.id as cate
            from blog_blogpost post, blog_blogpost_categories blog_cate, blog_blogcategory cate
            where post.id=%s and post.id=blog_cate.blogpost_id and blog_cate.blogcategory_id=cate.id''' % id
    # print sql
    return unio().fetchOne(sql)

def get_post_total(req, uid, cate=None):
    if cate:
        condition = ' post.cate2="%s" and ' % cate
    else:
        condition = ''
    sql = '''select count(post.title) as total
            from blog_blogpost post, blog_blogpost_categories cate, blog_blogcategory blog_category
            where %s post.status>0 and post.site_id=%s and post.user_id=%s and cate.blogcategory_id=blog_category.id
            and cate.blogpost_id=post.id''' % (condition, fun.get_site_id(req), uid)
    # print sql
    rt = unio().fetchOne(sql)
    if rt:
        return rt['total']
    else:
        return 1

def get_post_list(req, uid, cate=None, page=1, num=10):
    if page<1:
        return []
    if cate:
        condition = ' post.cate2="%s" and ' % cate
    else:
        condition = ''
    index = (int(page)-1)*num
    sql = '''select post.id, post.title, post.status, short_url, mobile_url, post.content, post.views,
            post.cate2, description, featured_image, post.created, cate.title as cate
            from blog_blogpost post, blog_blogpost_categories blog_cate, blog_blogcategory cate
            where %s post.user_id=%s and post.site_id=%s and post.id=blog_cate.blogpost_id and blog_cate.blogcategory_id=cate.id
            order by post.created desc limit %s,%s''' % (condition, uid, fun.get_site_id(req), index, num)
    # print sql
    return unio().fetchAll(sql)

def get_cate3_list(req, uid, cate, page=1, num=10):
    if page<1:
        return []
    if cate:
        condition = ' post.cate3="%s" and ' % cate
    else:
        condition = ''
    index = (int(page)-1)*num
    sql = '''select post.id, post.title, post.status, short_url, mobile_url, post.content, post.views,
            post.cate2, description, featured_image, post.created, cate.title as cate
            from blog_blogpost post, blog_blogpost_categories blog_cate, blog_blogcategory cate
            where %s post.user_id=%s and post.site_id=%s and post.id=blog_cate.blogpost_id and blog_cate.blogcategory_id=cate.id
            order by post.created desc limit %s,%s''' % (condition, uid, fun.get_site_id(req), index, num)
    # print sql
    return unio().fetchAll(sql)

def save_post(req, data, uid, uname):
    # print data
    id = data.get('id', 0)
    views = data.get('views')
    if not views:
        views = 0
    featured_image = data.get('featured_image', '')
    if not featured_image.strip():
        featured_image = '/static/zhiyuw/cy_images/images/infor.jpg'

    if id:  ##update
        sql = '''update blog_blogpost set title='%s', content='%s', cate2='%s', featured_image='%s',
                description='%s',created='%s', views='%s', cate3='%s'
                where id=%s''' % (data.get('title'), data.get('editorValue'), data.get('cate2'),
                                  featured_image, data.get('description', ''), fun.now(), views, data.get('cate3', ''), id)
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
                short_url, content, user_id, user_name, allow_comments, views, cate2, cate3, featured_image, description)
                values (%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')''' % \
                  (0, fun.get_site_id(req), data.get('title', 'no title'), data.get('title','no title'), fun.now(), 1,
                  fun.now(), short_url, data.get('editorValue'), uid, uname, 1, views, data.get('cate2'),data.get('cate3', ''),
                  featured_image, data.get('description'))
        # print sql
        lastid = unio().executeInsert(sql)
        if lastid:
            sql = '''insert blog_blogpost_categories (blogcategory_id, blogpost_id) values
                    ('%s', '%s')''' % (data.get('cate'), lastid)
            # print sql
            r =unio().executeInsert(sql)
        if r:
            sql = '''update ww_member set credits=credits+10 where id=%s''' % uid
            unio().execute(sql)

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
        sql = '''update ww_member_vip set qiyeming='%s', lianxifangshi='%s', qiyewangzhi='%s',
                qiyejianjie='%s', zhuanye='%s', zhuti='%s'
                where id=%s''' % (data.get('qiyeming'), data.get('lianxifangshi'),
                                  data.get('qiyewangzhi'), data.get('qiyejianjie'), data.get('zhuanye','qt'),
                                  data.get('zhuti'), uid)
        # print sql
        unio().execute(sql)
        sql = '''update ww_member set logo='%s' where id=%s''' % (data.get('photo_img'), uid)
        return unio().execute(sql)>-1
    elif utype=='gyq':
        sql = '''update ww_member set nickname='%s', logo='%s' where id=%s''' % \
              (data.get('nickname'), data.get('photo_img'), uid)
        # print sql
        unio().execute(sql)
        sql = '''update ww_member_normal set xingming='%s', shoujihao='%s', zuoyouming='%s', qq='%s',
               gerenjianjie='%s', zhiwei='%s', sex='%s', weixin='%s', linkedin='%s', guanzhuhan='%s'
               where id=%s''' % (data.get('xingming'), data.get('shoujihao'),
                 data.get('zuoyouming'), data.get('qq'), data.get('gerenjianjie'), data.get('zhiwei'),
                 data.get('sex'), data.get('weixin'), data.get('linkedin'), data.get('guanzhuhan'), uid)
        # print sql
        return unio().execute(sql)>-1

def get_profile(uid, utype):
    if utype=='ktq':
        sql = '''select ww_member.logo as photo_img, vip.qiyeming, qiyewangzhi, lianxifangshi, qiyejianjie, vip.zhuanye, vip.zhuti
                from ww_member, ww_member_vip vip
                where ww_member.id=%s and ww_member.id=vip.id''' % uid
        # print sql
        return unio().fetchOne(sql)
    elif utype=='gyq':
        sql = '''select m.nickname, m.logo as photo_img, n.xingming, n.shoujihao, n.zuoyouming, n.qq, n.gerenjianjie,
                n.zhiwei, n.sex, n.weixin, n.linkedin, n.guanzhuhan
                from ww_member m, ww_member_normal n
                where m.id=%s and m.id=n.id''' % uid
        # print sql
        return unio().fetchOne(sql)

def get_zhuanye_list():
    sql = '''select name, `desc` from ww_zhuanye where `desc` is not null and status=1'''
    # print sql
    return unio().fetchAll(sql)

def get_zhiwei_list():
    sql = '''select name, `desc` from ww_zhiwei where `desc` is not null and status=1'''
    # print sql
    return unio().fetchAll(sql)

def update_photo_img(url, utype, uid):
    if utype=='ktq':
        sql = '''update ww_member set logo='%s' where id=%s''' % (url, uid)
        # print sql
        return unio().execute(sql)
    elif utype=='gyq':
        sql = '''update ww_member set logo='%s' where id=%s''' % (url, uid)
        # print sql
        return unio().execute(sql)

def post_zhaopin(req, data, uid, uname):
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
    return save_post(req, data, uid, uname)

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
             <div class="Murphy_list fl"><strong>联系方式</strong><p>%s</p></div>
             <div class="Murphy_list fl"><strong>微信钱包</strong><p>%s</p></div>
             <div class="Murphy_list fl"><strong>说说内容</strong><p>%s</p></div></div>''' %  (r['user_name'], r['user_type'],
                                    r['lianxi'], r['qianbao'], r['shuoshuo'])

def del_qiye_comment(id):
    sql = '''update ww_qiye_comment set is_show=-1 where id=%s''' % id
    return unio().execute(sql)

def get_user_urls(uid):
    sql = '''SELECT * FROM ww_navigate WHERE uid=%s''' % uid
    # print sql
    return unio().fetchAll(sql)

def save_url(uid, nid, name, url):
    if nid: ##update
        sql = '''UPDATE ww_navigate SET name='%s', url='%s' WHERE uid=%s AND id=%s''' % (name, url, uid, nid)
    else:   ##insert
        sql = '''INSERT INTO ww_navigate (uid, name, url) VALUE (%s, '%s', '%s')''' % (uid, name, url)
    # print sql
    return unio().execute(sql)

def del_url(uid, nid):
    sql = '''DELETE FROM ww_navigate WHERE uid=%s AND id=%s''' % (uid, nid)
    # print sql
    return unio().execute(sql)

def get_xiangwang_count(uid, num=10):
    sql = '''SELECT count(id) as count
            FROM ww_guanzhu
            WHERE ww_guanzhu.pid=%s''' % uid
    # print sql
    r = unio().fetchOne(sql)
    if r:
        total =  r.get('count', 1)
        if total==0:
            return 1
        elif total%num==0:
            return total/num
        else:
            return total/num + 1
    else:
        return 1

def get_xiangwang(uid, page=1, num=10):
    index = (page-1)*num
    sql = '''SELECT ww_member.id, ww_member.logo,ww_member_vip.qiyewangzhi as url,ww_member_vip.qiyeming,
            ww_zhuanye.desc as hangye, ww_member.utype, ww_member.credits
            FROM ww_guanzhu, ww_member, ww_member_vip, ww_zhuanye
            WHERE ww_guanzhu.pid=%s AND ww_guanzhu.cid=ww_member.id AND ww_member.id=ww_member_vip.id
            AND ww_member_vip.zhuanye=ww_zhuanye.name
            order by ww_guanzhu.id desc limit %s,%s''' % (uid, index, num)
    # print sql
    r = unio().fetchAll(sql)
    if r:
        return fun.convert_dengji_list(*r)
    else:
        return {}

def get_tianchi_count(uid, gread=None, num=10):
    condi = ''
    if gread:
        condi = ''' AND ww_member_normal.zhiwei='%s' ''' % gread
    sql = '''SELECT count(ww_guanzhu.id) as count
            FROM ww_guanzhu, ww_member_normal
            WHERE ww_guanzhu.cid=%s AND ww_guanzhu.pid=ww_member_normal.id %s''' % (uid, condi)
    # print sql
    r = unio().fetchOne(sql)
    if r:
        total =  r.get('count', 1)
        if total==0:
            return 1
        elif total%num==0:
            return total/num
        else:
            return total/num + 1
    else:
        return 1

def get_tianchi(uid, gread=None, page=1, num=10):
    condi = ''
    if gread:
        condi = ''' AND ww_member_normal.zhiwei='%s' ''' % gread
    index = (page-1)*num
    sql = '''SELECT ww_member.id, ww_member.utype, ww_member.logo, ww_member.username, ww_member_normal.qq,
            ww_member_normal.shoujihao, ww_member_normal.weixin, ww_member_normal.linkedin, ww_member_normal.gerenjianjie,
            ww_member_normal.guanzhuhan
            FROM ww_guanzhu, ww_member, ww_member_normal
            WHERE ww_guanzhu.cid=%s AND ww_guanzhu.pid=ww_member.id AND ww_guanzhu.pid=ww_member_normal.id
            AND ww_member_normal.gerenjianjie is not null %s
            order by ww_guanzhu.id desc limit %s,%s''' % (uid, condi, index, num)
    # print sql
    return unio().fetchAll(sql)


def get_count(uid):
    d = {}
    sql = '''SELECT credits FROM ww_member where id=%s''' % uid
    # print sql
    member_totle = unio().fetchOne(sql)['credits']
    sql = '''SELECT count(views) as n, count(comments_count) as m FROM blog_blogpost where user_id=%s''' % uid
    # print sql
    r = unio().fetchOne(sql)
    article_totle = r['n']
    comment = r['m']

    sql = '''SELECT shuoshuo, money FROM ww_count WHERE uid=%s''' % uid
    # print sql
    r = unio().fetchOne(sql)
    sql = '''SELECT hudie as hudie_today, comment as comment_today,
            shuoshuo as shuoshuo_today, money_in, money_out
            FROM ww_count_history WHERE uid=%s AND created='%s';''' % (uid, date.today())
    # print sql
    r2 = unio().fetchOne(sql)
    if r:
        d = r
    if not r2:
        r2 = {'hudie_today': 0, 'comment_today': 0, 'shuoshuo_today': 0, 'money_in': 0, 'money_out': 0}
    d.update(r2)
    sql = '''SELECT article, comment FROM ww_count WHERE uid=%s''' % uid
    print sql
    r3 = unio().fetchOne(sql)
    d['hudie'] = member_totle + article_totle + r3.get('article')
    d['comment'] = comment + r3.get('comment')
    # print d
    return d

def log_money(uid, account, num):
    if num < 0:
        return
    email = account.strip().split()[0]
    sql = '''SELECT id FROM ww_member WHERE email='%s' AND 1=1''' % email
    r = unio().fetchOne(sql)
    if r:
        tid = r.get('id')
    else:
        return
    sql = '''SELECT money FROM ww_count WHERE uid=%s AND money>%s''' % (uid, num)
    r = unio().fetchOne(sql)
    if not r:  ##money not enougth
        return
    sql = '''INSERT INTO ww_money (sender_id, recev_id, num, created) VALUES (%s, %s, %s, now())''' % (uid, tid, num)
    r = unio().executeInsert(sql)
    if r:
        sql = '''INSERT INTO ww_money (sender_id, recev_id, num, created) VALUES (%s, %s, %s, now())''' % (tid, uid, 0-num)
        r = unio().executeInsert(sql)
        if r:
            r1 = controller2.add_count(tid, 'money', num)
            r2 = controller2.add_count(uid, 'money', 0-num)
            r3 = controller2.add_count_history(tid, 'money_in', num)
            r4 = controller2.add_count_history(uid, 'money_out', num)
            if r1 and r2 and r3 and r4:
                return True

def get_money_history(uid):
    sql = '''SELECT ww_money.num, ww_money.created, ww_member.username, ww_member.email
            FROM ww_money,ww_member WHERE recev_id=%s AND ww_money.sender_id=ww_member.id
            order by created desc''' % (uid)
    # print sql
    r = unio().fetchAll(sql)
    if r:
        return r
    else:
        []

def get_focus_count(uid):
    d = {}
    sql = '''SELECT focus FROM ww_count WHERE uid=%s''' % uid
    r = unio().fetchOne(sql)
    sql = '''SELECT focus as focus_today FROM ww_count_history WHERE uid=%s AND created='%s';''' % (uid, date.today())
    r2 = unio().fetchOne(sql)
    if r:
        d = r
    else:
        return d
    if r2:
        d.update(r2)
    return d

def get_user_profile(uid, label):
    sql = '''SELECT %s FROM ww_member_normal WHERE id=%s''' % (label, uid)
    # print sql
    return unio().fetchOne(sql)

def get_user_cates(uid):
    sql = '''SELECT distinct cate3 as name FROM blog_blogpost WHERE user_id=%s AND cate3 is not NULL;''' % uid
    # print sql
    return unio().fetchAll(sql)
