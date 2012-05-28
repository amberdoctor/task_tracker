# coding: utf8
## Define a server variable
host_defined = '127.0.0.1:8000' ##'mdp.cti.depaul.edu:8000'

## Define a table for tasks
db.define_table(
        'task',
        Field('short_description', 'string', notnull=True),
        Field('full_description', 'text', notnull=True),
        Field('created_by', db.auth_user, default=auth.user_id, readable=False, writable=False),
        Field('assigned_to', 'string', notnull=True),
        Field('status', requires=IS_IN_SET(['Accepted', 'Rejected', 'Not Reviewed']), default='Not Reviewed'),
        Field('progress', requires=IS_IN_SET(['In Progress', 'Not Started', 'Completed']), default='Not Started'),
        Field('date_created', 'datetime', default=request.now, readable=False, writable=False),
        Field('due_date', 'datetime'),
        format='%(short_description)s')
		
## Define a table for events
db.define_table(
		'event',
		Field('title'),
		Field('start_datetime','datetime'),
		Field('stop_datetime','datetime')
		)
    
## Define a table for comments about tasks
db.define_table(
        'task_comment',
        Field('tc_response_to','reference task'),
        Field('task_comment_text','text',requires=IS_NOT_EMPTY()),
        Field('tc_posted_on','datetime',default=request.now),
        Field('tc_posted_by',db.auth_user,default=auth.user_id)
        )
        

##Set requires permissions
db.task.assigned_to.requires=IS_IN_DB(db, 'auth_user.email', '%(first_name)s %(last_name)s', multiple=False)


## Set Read/Write Permissions for table fields
db.task_comment.tc_response_to.writable=False
db.task_comment.tc_response_to.readable=False

db.task_comment.tc_posted_on.writable=False
db.task_comment.tc_posted_on.readable=False

db.task_comment.tc_posted_by.writable=False
db.task_comment.tc_posted_by.readable=False
