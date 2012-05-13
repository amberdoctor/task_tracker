# coding: utf8
## Define table for the file that has been uploaded
db.define_table('file_share',
            Field('file_name',requires=IS_NOT_EMPTY()),
            Field('description',requires=IS_NOT_EMPTY()),
            Field('posted_on','datetime',default=request.now),
            Field('posted_by',db.auth_user,default=auth.user_id),
            Field('access_permitted_to', 'list:string', requires=IS_IN_DB(db, 'auth_user.email', '%(first_name)s %(last_name)s', multiple=True)),
            Field('file','upload',requires=IS_NOT_EMPTY()),
            Field('access_permitted_to_tasks', 'list:reference task', requires=IS_IN_DB(db, 'task.id', '%(short_description)s', multiple=True))
            )

## Define table for the comments about files
db.define_table('comment',
            Field('response_to','reference file_share'),
            Field('comment_text','text',requires=IS_NOT_EMPTY()),
            Field('posted_on','datetime',default=request.now),
            Field('posted_by',db.auth_user,default=auth.user_id)
            )
            

## Set Read/Write Permissions for table fields
db.file_share.posted_on.writable=False
db.file_share.posted_on.readable=False

db.file_share.posted_by.writable=False
db.file_share.posted_by.readable=False

db.comment.response_to.writable=False
db.comment.response_to.readable=False

db.comment.posted_on.writable=False
db.comment.posted_on.readable=False

db.comment.posted_by.writable=False
db.comment.posted_by.readable=False
