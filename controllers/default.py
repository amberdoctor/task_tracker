# -*- coding: utf-8 -*-

#########################################################################
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################
import datetime

def index():
    """
    Defines main landing page.
    """
    return locals()
    
def error():
    """
    Defines an error page.
    """
    return locals()
    
#FILE SHARING SECTION
        
@auth.requires_login()
def upload():
    """
    Allows authenticated user to upload a file.
    Uploaded files generate a link that enables the user to share the file.
    """
    db.file_share.access_permitted_to_tasks.readable=False
    db.file_share.access_permitted_to_tasks.writable=False
    form = SQLFORM(db.file_share).process()
    if form.accepted:
        response.flash = "Your file was uploaded"
        uploaded_file_id = form.vars.id
        uploaded_file_url = URL('file', host='host_defined', scheme='https', args=uploaded_file_id)
        uploaded_file_link = A(uploaded_file_url, _href=uploaded_file_url)
        my_files_url = A('my files', _href=URL('my_files'))
        message = DIV('Use this URL to share your file with users that you assigned permissions to:',BR(),uploaded_file_link,BR(),BR(),'You can view and manage all files that you have uploaded at ', my_files_url,'.')
    return locals()
    
@auth.requires_login()
def upload_to_task():
    """
    Allows authenticated user to upload a file to a specified task.
    Uploaded files generate a link that enables the user to share the file.
    """
    allowed_access = False
    task_id = request.args(0)
    task = db.task(id=task_id) or redirect(URL('error'))
    db.file_share.access_permitted_to_tasks.readable=False
    db.file_share.access_permitted_to_tasks.writable=False
    db.file_share.access_permitted_to_tasks.default=task.id
    if (task.created_by==auth.user.id or task.assigned_to==auth.user.email):
        form = SQLFORM(db.file_share).process()
        allowed_access = True
        if form.accepted:
            session.flash = "Your file was uploaded"
            redirect(URL('task',args=task_id))
    return locals()

@auth.requires_login()
def my_files():
    """
    Allows viewing all files posted by the current authenticated user.
    """
    my_uploads = db(db.file_share.posted_by==auth.user.id).select(db.file_share.ALL, orderby=~db.file_share.posted_on)
    shared_uploads = db(db.file_share.access_permitted_to.contains(auth.user.email)).select(db.file_share.ALL, orderby=~db.file_share.posted_on)
    return locals()

@auth.requires_login()
def file():
    """
    Allows viewing file details and allows downloading an uploaded file.
    URL must include the id of the file as an arg
    """
    allowed_access = False
    file_id = request.args(0)
    file = db.file_share(id=file_id) or redirect(URL('error_file'))
    if (file.posted_by==auth.user.id):
        rows = db(db.file_share.id==file.id).select()
        comments = db(db.comment.response_to==file_id).select()
        allowed_access = True
    elif file.access_permitted_to:
        if (auth.user.email in file.access_permitted_to):
            rows = db(db.file_share.id==file.id).select()
            comments = db(db.comment.response_to==file_id).select()
            allowed_access = True
    else:
        message = "You do not have access to this file."
    return locals()

@auth.requires_login()
def comment():
    """
    Allows user to comment on an uploaded file.  
    URL must include the id of the file as an arg.
    """
    allowed_access = False
    file_id = request.args(0)
    file = db.file_share(id=file_id) or redirect(URL('error'))
    if (file.posted_by==auth.user.id):
        rows = db(db.file_share.id==file.id).select()
        db.comment.response_to.default = file_id
        form = SQLFORM(db.comment).process()
        allowed_access = True
        if form.accepted:
            session.flash = "Your comment was posted"
            redirect(URL('file',args=file_id))
    elif file.access_permitted_to:
        if (auth.user.email in file.access_permitted_to):
            rows = db(db.file_share.id==file.id).select()
            db.comment.response_to.default = file_id
            form = SQLFORM(db.comment).process()
            allowed_access = True
            if form.accepted:
                session.flash = "Your comment was posted"
                redirect(URL('file',args=file_id))
    return locals()










# TASK SECTION

@auth.requires_login()
def my_tasks():
    """
    creates two tables
    created_by_me are tasks that the logged in user created
    assigned_to_me are tasks that the logged in user was assigned by another user or by themself
    """
    created_by_me = db(db.task.created_by==auth.user.id).select(orderby=~db.task.due_date)
    assigned_to_me = db(db.task.assigned_to==auth.user.email).select(orderby=~db.task.due_date)
    return locals()
    
    
@auth.requires_login()
def add_task():
    """
    Allows the adding of a task by authenticated users
    """
    form = SQLFORM(db.task).process()
    if form.accepted:
        response.flash = "Task Added"
        my_tasks_url = A('my tasks', _href=URL('my_tasks'))
        message = DIV('Task was added.  You may review your task at ', my_tasks_url,'.')
        """
        To notify the person listed in the assigned_to category
        """
        email_task_url = URL('my_tasks', host=host_defined, scheme='https')
        assigned_to_message = 'A new task was assigned to you.  You may review your tasks at: ' + str(email_task_url) + '.'
        created_by_message = 'A new task was created by you.  You may review your tasks at: ' + str(email_task_url) + '.'
        reminder_message = 'Task Reminder Notification.  You have a task that is due soon.  You may review your tasks at: ' + str(email_task_url) + '.'
        ## email notification of task creation to the assignee
        db.email.insert(email_to=form.vars.assigned_to, 
                        email_subject='A new task was assigned to you.', 
                        email_message=assigned_to_message)
        ## email reminder of task to the assignee
        db.email.insert(email_to=form.vars.assigned_to, 
                        email_subject='Task Reminder', 
                        email_message=reminder_message,
                        email_send_date=form.vars.due_date - datetime.timedelta(days=1))
        ## email notification of task creation to the creator
        db.email.insert(email_to=form.vars.created_by, 
                        email_subject='You created a new task.', 
                        email_message=created_by_message)
        ## email reminder of task to the creator          
        db.email.insert(email_to=form.vars.created_by, 
                        email_subject='Task Reminder', 
                        email_message=reminder_message,
                        email_send_date=form.vars.due_date - datetime.timedelta(days=1))
    return locals()

@auth.requires_login()
def task():
    """
    Allows viewing task details and allows downloading a task.
    URL must include the id of the file as an arg
    """
    allowed_access = False
    task_id = request.args(0)
    task = db.task(id=task_id) or redirect(URL('error'))
    if (task.created_by==auth.user.id or task.assigned_to==auth.user.email):
        tasks = db(db.task.id==task_id).select()
        comments = db(db.task_comment.tc_response_to==task_id).select()
        my_uploads = db(db.file_share.access_permitted_to_tasks.contains(task_id)).select(db.file_share.ALL,    
                    orderby=~db.file_share.posted_on)
        allowed_access = True      
    else:
        message = "You do not have access to this task."
    return locals()

@auth.requires_login()
def update_task():
    """
    Allows a user to update a task they have permissions for.
    """

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
    task_url = URL('update_task', host='host_defined', scheme='https', args=task_id)
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
        
        
    if (task.created_by==auth.user.id or (task.assigned_to==auth.user.email)):
        form = SQLFORM(db.task, task).process()
        previous_assigned_to = task.assigned_to 
        if form.accepted:
            response.flash = 'Task was Updated.'
            updated_message = 'The following task was updated: ' + str(task_url) + '.'
            #email notice that a task has been updated
            db.email.insert(email_to=form.vars.assigned_to,
                             email_subject='A task assigned to you was updated.', 
                             email_message=updated_message)
            #email notice that a task has been updated
            db.email.insert(email_to=task.created_by.email,
                             email_subject='A task you created was updated.', 
                             email_message=updated_message)
            if (form.vars.assigned_to!=previous_assigned_to):
                reassigned_message = 'The following task is no longer assigned to you: ' + task.short_description + '  Full Description: ' + task.full_description + '  If you were not the creator of this task, you will no longer be able to view it.'
                #email notice that a task has been updated
                db.email.insert(email_to=previous_assigned_to, 
                                email_subject='A task assigned to you was reassigned.', 
                                email_message=reassigned_message)
            redirect(URL('my_tasks'))           
    return locals()
    

@auth.requires_login()
def task_comment():
    """
    Allows user to comment on an task.  
    URL must include the id of the file as an arg.
    """
    allowed_access = False
    task_id = request.args(0)
    task = db.task(id=task_id) or redirect(URL('error'))
    if (task.created_by==auth.user.id or task.assigned_to==auth.user.email):
        tasks = db(db.task.id==task.id).select()
        db.task_comment.tc_response_to.default = task_id
        form = SQLFORM(db.task_comment).process()
        allowed_access = True
        if form.accepted:
            session.flash = "Your comment was posted"
            redirect(URL('task',args=task_id))
    return locals()


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
