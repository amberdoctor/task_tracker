# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.title = T('Amber Doctor Task Tracker')
response.subtitle = T('DePaul University CSC 438 Assignment 3')

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Amber Doctor <amberdoctor@gmail.com>'
response.meta.description = 'task tracking application'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'
response.meta.copyright = 'Copyright 2012'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [(T('Home'), False, URL('default','index'), []),
    (T('My Tasks'), False, URL('default','my_tasks'), []),
    (T('Add Task'), False, URL('default','add_task'), []),
    (T('My Files'), False, URL('default','my_files'), []),
    (T('Add File'), False, URL('default','upload'), [])
    ]
