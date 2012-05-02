# coding: utf8

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
    
db.task.assigned_to.requires=IS_IN_DB(db, 'auth_user.email', '%(first_name)s %(last_name)s', multiple=False)
