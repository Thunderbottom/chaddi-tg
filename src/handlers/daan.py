from loguru import logger
from util import util
from db import dao
from telegram import ParseMode

def handle(update, context):

    util.log_chat("daan", update)

    # Extract query...
    query = update.message.text
    query = query.split(" ")

    if len(query) < 2:
        update.message.reply_text(
            text="Haat chutiya! Syntax is `/daan @username 786`",
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    sender = dao.get_bakchod_by_id(update.message.from_user["id"])
    if sender is None:
        sender = Bakchod.fromUpdate(update)
        dao.insert_bakchod(sender)

    receiver_username = query[1]
    if receiver_username.startswith("@"):
        receiver_username = receiver_username[1:]
    receiver = dao.get_bakchod_by_username(receiver_username)
    if receiver is None:
        update.message.reply_text(receiver_username + "??? Who dat???")
        return

    try:
        daan = int("".join(query[2:]))
    except Exception as e:
        update.message.reply_text("Kitna rokda be???")
        return

    logger.info(
        "[daan] sender={} receiver={} daan={}",
        sender.username,
        receiver.username,
        daan,
    )

    sender.rokda = sender.rokda - daan
    dao.insert_bakchod(sender)

    receiver.rokda = receiver.rokda + daan
    dao.insert_bakchod(receiver)

    update.message.reply_text(
        "@{} gave @{}🤲 a daan of {} ₹okda! 🎉".format(
            sender.username, receiver.username, daan
        )
    )
    return