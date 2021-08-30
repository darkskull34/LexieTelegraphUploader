import os
import asyncio
import logging
import info

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import FloodWait, UserNotParticipant
from creds import Credentials
from telegraph import upload_file

logging.basicConfig(level=logging.WARNING)

async def ForceSub(bot: Client, event: Message):
    """
    Custom Pyrogram Based Telegram Bot's Force Subscribe Function by @viharasenindu.
    If User is not Joined Force Sub Channel Bot to Send a Message & ask him to Join First.
    
    :param bot: Pass Client.
    :param event: Pass Message.
    :return: It will return 200 if Successfully Got User in Force Sub Channel and 400 if Found that User Not Participant in Force Sub Channel or User is Kicked from Force Sub Channel it will return 400. Also it returns 200 if Unable to Find Channel.
    """
    
    try:
        invite_link = await bot.create_chat_invite_link(chat_id=(int(info.UPDATES_CHANNEL) if info.UPDATES_CHANNEL.startswith("-100") else info.UPDATES_CHANNEL))
    except FloodWait as e:
        await asyncio.sleep(e.x)
        fix_ = await ForceSub(bot, event)
        return fix_
    except Exception as err:
        print(f"Unable to do Force Subscribe to {info.UPDATES_CHANNEL}\n\nError: {err}\n\nContact Support Group: https://t.me/lexiesupport")
        return 200
    try:
        user = await bot.get_chat_member(chat_id=(int(info.UPDATES_CHANNEL) if info.UPDATES_CHANNEL.startswith("-100") else info.UPDATES_CHANNEL), user_id=event.from_user.id)
        if user.status == "kicked":
            await bot.send_message(
                chat_id=event.from_user.id,
                text="Sorry Dear, You are Banned to use me ☹️\nFeel free to say in our [Support Group](https://t.me/lexiesupport).",
                parse_mode="markdown",
                disable_web_page_preview=True,
                reply_to_message_id=event.message_id
            )
            return 400
        else:
            return 200
    except UserNotParticipant:
        await bot.send_message(
            chat_id=event.from_user.id,
            text="<b>Hello {} 👋</b>\n\n<b>You cant use me untill subscribe our updates channel ☹️</b>\n<b>So Please join our updates channel by the following button and restart our bot by ( /start ) command 😊</b>".format(event.from_user.mention),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Join Our Updates Channel 🗣", url=invite_link.invite_link)
                    ]
                ]
            ),
            disable_web_page_preview=True,
            reply_to_message_id=event.message_id
        )
        return 400
    except FloodWait as e:
        await asyncio.sleep(e.x)
        fix_ = await ForceSub(bot, event)
        return fix_
    except Exception as err:
        print(f"Something Went Wrong! Unable to do Force Subscribe.\nError: {err}\n\nContact Support Group: https://t.me/lexiesupport")
        return 200



tgraph = Client(
    "Telegraph Uploader bot",
    bot_token=Credentials.BOT_TOKEN,
    api_id=Credentials.API_ID,
    api_hash=Credentials.API_HASH
)


@tgraph.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        text=f"Hello {message.from_user.mention},\nI'm Telegraph Uploader Bot",
        disable_web_page_preview=True
    )


@tgraph.on_message(filters.photo)
async def getimage(client, message):
    dwn = await message.reply_text("Downloading...", True)
    img_path = await message.download()
    await dwn.edit_text("Uploading...")
    try:
        url_path = upload_file(img_path)[0]
    except Exception as error:
        await dwn.edit_text(f"Sorry Something Went Wrong😢\n{error}")
        return
    await dwn.edit_text(
        text=f"<b>Link :-</b> <code>https://telegra.ph{url_path}</code>",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                   InlineKeyboardButton(
                        text="Open Link", url=f"https://telegra.ph{url_path}")
            ]
                  
       ),
 
    os.remove(img_path)
tgraph.run()
