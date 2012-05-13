# coding: utf8
#define table for emails
db.define_table(
            'email',
            Field('email_send_date', 'datetime', default=request.now),
            Field('sent_on', 'datetime', default=None),
            Field('failed_on', 'datetime', default=None),
            Field('failed', 'boolean', default=False),
            Field('email_to'),
            Field('email_subject'),
            Field('email_message'),
            auth.signature)
