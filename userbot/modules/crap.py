# Copyright (C) 2020 Azrim.

import ffmpy
import time
import asyncio
from userbot.events import register
import os
from userbot import TEMP_DOWNLOAD_DIRECTORY ,bot
from userbot import CMD_HELP
from userbot.util import admin_cmd, humanbytes, progress, time_formatter

@register(outgoing=True, pattern=r"^.togif(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    if not event.is_reply:
        await event.edit("Reply to a video to convert it.")
        return
    mone = await event.edit("Processing ...")
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        try:
            c_time = time.time()
            downloaded_file_name = await bot.download_media(
                reply_message,
                TEMP_DOWNLOAD_DIRECTORY,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, mone, c_time, "trying to download")
                )
            )
            directory_name = TEMP_DOWNLOAD_DIRECTORY + "/clip.gif"
            await event.edit("`Converting your media....`")
            ff = ffmpy.FFmpeg(
                inputs = {downloaded_file_name : None},
                outputs = {directory_name : None})
            ff.run()

        except Exception as e:  # pylint:disable=C0103,W0703
            await mone.edit(str(e))

        except ValueError as e:
            await mone.edit(str(e))

        await asyncio.sleep(7)
        await bot.send_file(
            event.chat_id,
            directory_name,
            caption="Enjoy your gif",
            force_document=True,
            allow_cache=False,
            reply_to=event.message.id,
        )
        os.remove(directory_name)
        os.remove(downloaded_file_name)
        await event.delete()
