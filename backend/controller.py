#encoding: utf-8
__author__ = 'macy'

from model import *
from zhiyuw import function as fun
from local_settings import SITE_ID

def get_site_id():
    return SITE_ID

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

def get_post_list(page=1, num=10):
    index = (int(page)-1)*num
    sql = '''select post.id, post.title, post.content, post.views, post.cate2, post.status,
            post.created, cate.title as cate
            from blog_blogpost post, blog_blogpost_categories blog_cate, blog_blogcategory cate
            where post.site_id=%s and post.id=blog_cate.blogpost_id and blog_cate.blogcategory_id=cate.id
            order by post.created desc limit %s,%s''' % (get_site_id(), index, num)
    # print sql
    return unio().fetchAll(sql)

def save_post(data):
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
        short_url = '/xx/xx'
        sql = '''insert into blog_blogpost (comments_count, site_id, title, slug, created, status, publish_date,
                short_url, content, user_id, user_name, allow_comments, views, cate2)
                values (%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')''' % \
                  (0, get_site_id(), data.get('title', 'no title'), data.get('title','no title'), fun.now(), data.get('status'),
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
            sql = '''update blog_blogpost set short_url='%s' where id=%s''' %(short_url, lastid)
            return unio().execute(sql)


def del_post(id):
    sql = '''delete from blog_blogpost where id=%s''' % id
    r = unio().execute(sql)
    if not r:
        return None
    sql = '''delete from blog_blogpost_categories where blogpost_id=%s''' % id
    return unio().execute(sql)

def get_comment_list(page=1, num=10):
    index = (int(page)-1)*num
    sql = '''select id, comment, user_name, submit_date
            from django_comments
            where is_removed=0 and site_id=%s order by submit_date desc limit %s,%s''' % (get_site_id(), index, num)
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