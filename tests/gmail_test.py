import pytest
from mmgmail.gmail import GMail


class TestGMail:
    @pytest.fixture()
    def gmail1(self) -> GMail:
        return GMail()

    def test_send_mail(self, gmail1: GMail):
        to = "kato.yutaka@gmail.com"
        subject = "メール送信自動化テスト"
        message_text = "メール送信の自動化テストをしています。"
        gmail1.send_mail(to, subject, message_text)

    def test_list_messages_matching_query(self, gmail1: GMail):
        query = "from:info@keishicho.metro.tokyo.jp"
        # query = "from:info@keishicho.metro.tokyo.jp is:unread"
        messages = gmail1.list_messages_matching_query(query)
        print(messages)

    def test_list_and_get(self, gmail1: GMail):
        query = "from:info@keishicho.metro.tokyo.jp"
        messages = gmail1.list_messages_matching_query(query)
        # idとthreadIdしか入っていないので、もう一度getする必要がある
        for message in messages:
            message = gmail1.get_message(message["id"])
            subject = gmail1.get_subject(message)
            print("subject=" + subject)
            # 取り敢えず1件で良い
            break

    def test_get_message(self, gmail1: GMail):
        message = gmail1.get_message("16642b1b92620a2d")

        subject = gmail1.get_subject(message)
        date = gmail1.get_date(message)
        body = gmail1.get_body(message)
        print("subject=" + subject)
        print("date=" + date)
        print("body=" + body)
