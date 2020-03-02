import argparse
import logging
from mmgmail.core import send_mail, list_messages_matching_query, get_message


def main():
    parser = argparse.ArgumentParser(
        description="""
    GMail の情報を取得します。
    """
    )

    parser.add_argument("-g", "--message", help="送信メールの本文")
    parser.add_argument("-s", "--subject", help="送信メールのタイトル")
    parser.add_argument("-t", "--to", help="送信メールの宛先")
    parser.add_argument("-q", "--query", help="このクエリに一致するメールメッセージを全て取得します")
    parser.add_argument("-i", "--id", help="取得するメールメッセージのID")
    parser.add_argument("-m", "--mode", help="モードを指定します", choices=["send", "list", "get"])
    parser.add_argument("-d", "--debug", help="デバッグログ出力をONにします", action="store_true")

    args = parser.parse_args()

    # log設定
    formatter = "%(asctime)s : %(levelname)s : %(message)s"
    if args.debug:
        # ログレベルを DEBUG に変更
        logging.basicConfig(level=logging.DEBUG, format=formatter)
    else:
        logging.basicConfig(format=formatter)

    if args.mode == "send":
        send_mail(to=args.to, subject=args.subject, message_text=args.message)
    elif args.mode == "list":
        list_messages_matching_query(args.query)
    elif args.mode == "get":
        get_message(args.id)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
