def getUsernameFromEmail(email_address):
    strip_starting_index = email_address.index('@')
    return email_address[0:strip_starting_index]