import time
while True:
    ## set the query up to find emails that haven't been send and that have a send date that has past
    query = db.email.sent_on==None&(db.email.email_send_date < request.now)
    ## grab the next email to send
    next_email = db(query).select().first()
    ## check if there is an email to send
    if next_email:
        ## send the email
        ret = mail.send(to=next_email.email_to,
                   subject=next_email.email_subject,
                   message=next_email.email_message)
        ## update the database
        next_email.update_record(sent_on=request.now,
                                    failed = not ret)
        db.commit()
    ## else sleep
    else:
        time.sleep(60) #that's 60 second sleep
