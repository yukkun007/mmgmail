import os
import base64
import pickle
import email
import logging
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
from typing import Dict, List
from apiclient import errors
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Gmail API リファレンス
# https://developers.google.com/gmail/api/v1/reference


class GMail:
    SCOPES = [
        "https://www.googleapis.com/auth/gmail.send",
        "https://www.googleapis.com/auth/gmail.readonly",
    ]
    GMAIL_CLIENT_SECRET = "/tmp/mmgmail_client_secret.json"
    GMAIL_TOKEN_PICKLE = "/tmp/mmgmail_token.pickle"
    SENDER = "kato.yutaka@gmail.com"

    def __init__(self):
        self._service = self._login()

    def _save_client_secret(self):
        secret = Path(GMail.GMAIL_CLIENT_SECRET)
        if not secret.exists():
            load_dotenv(dotenv_path="", verbose=True)
            contents = os.environ.get("mmgmail_client_secret_contents", "dummy")
            secret.write_text(contents)

    def _login(self):
        credentials = None
        if os.path.exists(GMail.GMAIL_TOKEN_PICKLE):
            with open(GMail.GMAIL_TOKEN_PICKLE, "rb") as token:
                credentials = pickle.load(token)

        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                self._save_client_secret()
                flow = InstalledAppFlow.from_client_secrets_file(
                    GMail.GMAIL_CLIENT_SECRET, GMail.SCOPES
                )
                credentials = flow.run_local_server()
            with open(GMail.GMAIL_TOKEN_PICKLE, "wb") as token:
                pickle.dump(credentials, token)
        service = build("gmail", "v1", credentials=credentials)
        return service

    def send_mail(self, to: str, subject: str, message_text: str) -> None:
        message = MIMEText(message_text)
        message["to"] = to
        message["from"] = GMail.SENDER
        message["subject"] = subject
        encode_message = base64.urlsafe_b64encode(message.as_bytes())
        # 送信
        self._send_mail_sub({"raw": encode_message.decode()}, user_id="me")

    def _send_mail_sub(self, message_raw: Dict, user_id: str = "me") -> None:
        try:
            message = (
                self._service.users().messages().send(userId=user_id, body=message_raw).execute()
            )
            logging.info("message Id: {}".format(message["id"]))
        except errors.HttpError as error:
            logging.error("an error occurred: {}".format(error))

    def get_message(self, msg_id: str, user_id: str = "me"):
        message = (
            self._service.users().messages().get(userId=user_id, id=msg_id, format="raw").execute()
        )
        msg_str = base64.urlsafe_b64decode(message["raw"]).decode("utf-8")
        mime_msg = email.message_from_string(msg_str)
        return mime_msg

    def get_subject(self, message):
        subjects = email.header.decode_header(message.get("Subject"))
        for subject in subjects:
            if isinstance(subject[0], bytes) and subject[1] is not None:
                return subject[0].decode(subject[1])
            else:
                return subject[0].decode()

    def get_date(self, message):
        date = message.get("Date")
        return self._get_formatted_date(date)

    def get_body(self, message):
        if message.is_multipart():
            for payload in message.get_payload():
                if payload.get_content_type() == "text/plain":
                    charset = message.get_param("charset")
                    if charset is None:
                        return payload.get_payload(decode=True).decode("iso-2022-jp")
                    else:
                        return payload.get_payload(decode=True).decode(charset)
        else:
            charset = message.get_param("charset")
            return message.get_payload(decode=True).decode(charset)

    def list_messages_matching_query(self, query: str = "", user_id: str = "me"):
        try:
            response = self._service.users().messages().list(userId=user_id, q=query).execute()
            messages: List[Dict] = []
            if "messages" in response:
                messages.extend(response["messages"])

            while "nextPageToken" in response:
                page_token = response["nextPageToken"]
                response = (
                    self._service.users()
                    .messages()
                    .list(userId=user_id, q=query, pageToken=page_token)
                    .execute()
                )
                messages.extend(response["messages"])

            return messages
        except errors.HttpError as error:
            logging.error("an error occurred: {}".format(error))

    def _get_formatted_date(self, date: str) -> str:
        split_date = date.split()

        # 日時情報を生成（タイムゾーン情報なし）
        ts = ""
        for s in split_date[1:5]:
            ts += s
        # 取得した日付情報から naive な datetime オブジェクトを生成
        d = datetime.strptime(ts, "%d%b%Y%H:%M:%S")

        # タイムゾーン情報を文字列から取得
        tzs = split_date[5]
        if tzs[0] == "+":
            sign = 1
        else:
            sign = -1
        h = int(tzs[1:3])
        m = int(tzs[3:])

        # タイムゾーン情報を生成
        TZ = timezone(timedelta(hours=(sign * h), minutes=(sign * m)))
        # 生成済みの naive な datetime とタイムゾーン情報から aware な datetime オブジェクトを生成
        dt = datetime(d.year, d.month, d.day, d.hour, d.minute, d.second, 0, tzinfo=TZ)

        return dt.strftime("%Y/%m/%d %H:%M:%S")
