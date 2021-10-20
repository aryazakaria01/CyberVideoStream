import io
import sys
import traceback
import speedtest
from lib.helpers.decorators import authorized_users_only, sudo_users_only
from pyrogram.types import Message
from pyrogram import Client, filters
from pyrogram.errors import RPCError


def get_text(message: Message) -> [None, str]:
    text_to_return = message.text
    if message.text is None:
        return None
    if " " in text_to_return:
        try:
            return message.text.split(None, 1)[1]
        except IndexError:
            return None
    else:
        return None


@Client.on_message(filters.command("eval"))
@sudo_users_only
async def eval(client, message):
    kontolkecil = get_text(message)
    status_message = await message.reply_text("Processing ...")
    if not kontolkecil:
        await status_message.edit("Invalid Command Syntax!")
        return

    cmd = message.text.split(" ", maxsplit=1)[1]

    reply_to_ = message
    if message.reply_to_message:
        reply_to_ = message.reply_to_message

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"

    final_output = "<b>EVAL</b>: "
    final_output += f"<code>{cmd}</code>\n\n"
    final_output += "<b>OUTPUT</b>:\n"
    final_output += f"<code>{evaluation.strip()}</code> \n"

    if len(final_output) > 4096:
        with io.BytesIO(str.encode(final_output)) as out_file:
            out_file.name = "eval.text"
            await reply_to_.reply_document(
                document=out_file, caption=cmd, disable_notification=True
            )
    else:
        await reply_to_.reply_text(final_output)
    await status_message.delete()


async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {l_}" for l_ in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)


Client.on_message(filters.command("speedtest"))
@sudo_users_only
def speedtest_(_,message):
    speed = speedtest.Speedtest()
    speed.get_best_server()
    speed.download()
    speed.upload()
    speedtest_image = speed.results.share()

    message.reply_photo(speedtest_image)


@Client.on_message(filters.command("leave"))
@sudo_users_only
async def leave(client, message):
    if len(message.command) == 1:
        try:
            await client.leave_chat(message.chat.id)
        except RPCError as e:
            print(e)
    else:
        cmd = message.text.split(maxsplit=1)[1]
        try:
            await client.leave_chat(int(cmd))
        except RPCError as e:
            print(e)


@Client.on_message(filters.command("invitelink"))
@authorized_users_only
async def invitelink(client, message):
    chat_id = message.chat.id
    try:
        grouplink = await client.export_chat_invite_link(chat_id)
        await message.reply_text(f"{grouplink}")
    except Exception as e:
        pass
