# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html
    """
    response.flash = "Welcome to web2py!"
    return dict(message=T('Hello World'))

@auth.requires_login()
def my_tasks():
    """
    defines two tables
    created_by_me are tasks that the logged in user created
    assigned_to_me are tasks that the logged in user was assigned by another user or by themself
    """
    created_by_me = db(db.task.created_by==auth.user.id).select(orderby=~db.task.due_date)
    assigned_to_me = db(db.task.assigned_to==auth.user.email).select(orderby=~db.task.due_date)
    return locals()
    
    
@auth.requires_login()
def add_task():
    """
    """
    form = SQLFORM(db.task).process()
    if form.accepted:
        response.flash = "Task Added"
        my_tasks_url = A('my tasks', _href=URL('my_tasks'))
        message = DIV('Task was added.  You may review your task at ', my_tasks_url,'.')
    return locals()
    
def update_task():
    """
    First grab the task id from the args
    Then check if the task exists in the database
    Then check if the task belongs to the authenticated user
    If it was created by the authenticated user - allow them to edit certain fields
    If it was assigned to the authenticated user - allow them to edit progress and status fields
    Otherwise inform the user that do not have permission to see this task.
    Create the update form
   
    """
    
    task_id = request.args(0)
    task = db.task(id=task_id) or redirect(URL('task_not_found'))
    
    


    """
    Set permissions based on user authentication
    """
    if (task.created_by==auth.user.id and task.assigned_to==auth.user.email):
        message = 'Please update your task.'
        db.task.id.readable=False
        db.task.short_description.writable=False
        db.task.full_description.writable=False
        db.task.created_by.readable=True
        db.task.assigned_to.writable=True
        db.task.status.writable=True
        db.task.progress.writable=True
        db.task.date_created.readable=True
        db.task.due_date.writable=True
    elif (task.created_by==auth.user.id):
        message = 'Please update your task.'
        db.task.id.readable=False
        db.task.short_description.writable=False
        db.task.full_description.writable=False
        db.task.created_by.readable=True
        db.task.assigned_to.writable=True
        db.task.status.writable=False
        db.task.progress.writable=False
        db.task.date_created.readable=True
        db.task.due_date.writable=True
    elif (task.assigned_to==auth.user.email):
        message = 'Please update the status or the progress indicators of the task.'
        db.task.id.readable=False
        db.task.short_description.writable=False
        db.task.full_description.writable=False
        db.task.created_by.readable=True
        db.task.assigned_to.writable=False
        db.task.status.writable=True
        db.task.progress.writable=True
        db.task.date_created.readable=True
        db.task.due_date.writable=False
    else :
        message = 'You do not have permission to see this task.'
        
        
    if (task.created_by==auth.user.id):
        form = SQLFORM(db.task, task, deletable=True).process()
        
    elif (task.assigned_to==auth.user.email):
        form = SQLFORM(db.task, task).process()

    if form.accepted:
        response.flash = 'Task was Updated.'
        redirect(URL('my_tasks'))   

    return locals()
    
    


    
"""
What do I need?
Need a page for people to track their tasks - two parts - ones they create - ones assigned to them
So I need a controller that pulls items that they wrote
And a controller that pulls items that they were assigned
Maybe make these two separate pages and then also have the main page with both

Need a page to add a new task
The page for people to track their tasks should have a button to add a new task 
Maybe put that new task button in a defined side bar

"""




def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
