from mmgmail.gmail import GMail


def send_mail(to: str, subject: str, message_text: str) -> None:
    gmail = GMail()
    gmail.send_mail(to, subject, message_text)


def list_messages_matching_query(query: str) -> None:
    gmail = GMail()
    messages = gmail.list_messages_matching_query(query)
    for message in messages:
        print("id=" + message["id"])


def get_message(msg_id: str) -> None:
    gmail = GMail()
    message = gmail.get_message(msg_id)
    subject = gmail.get_subject(message)
    date = gmail.get_date(message)
    body = gmail.get_body(message)
    print("subject = " + subject)
    print("date    = " + date)
    print("body    = " + body)
