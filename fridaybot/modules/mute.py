#   Copyright 2019 - 2020-2021 DarkPrinc3

#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at

#       http://www.apache.org/licenses/LICENSE-2.0

#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import asyncio

from fridaybot import CMD_HELP
from fridaybot.modules.sql_helper.mute_sql import is_muted, mute, unmute


@friday.on(friday_on_cmd(pattern=r"mute ?(\d+)?"))
async def startmute(event):
    private = False
    if event.fwd_from:
        return
    elif event.is_private:
        await event.edit("Unexpected issues or ugly errors may occur!")
        await asyncio.sleep(3)
        private = True
    if any(x in event.raw_text for x in ("/mute", "!mute")):
        await asyncio.sleep(0.5)
    else:
        reply = await event.get_reply_message()
        if event.pattern_match.group(1) is not None:
            userid = event.pattern_match.group(1)
        elif reply is not None:
            userid = reply.sender_id
        elif private:
            userid = event.chat_id
        else:
            return await event.edit(
                "Please reply to a user or add their userid into the command to mute them."
            )
        chat_id = event.chat_id
        chat = await event.get_chat()
        if "admin_rights" in vars(chat) and vars(chat)["admin_rights"] is not None:
            if chat.admin_rights.delete_messages is not True:
                return await event.edit(
                    "`You can't mute a person if you dont have delete messages permission. ಥ﹏ಥ`"
                )
        elif "creator" in vars(chat):
            pass
        elif not private:
            return await event.edit(
                "`You can't mute a person without admin rights niqq.` ಥ﹏ಥ  "
            )
        if is_muted(userid, chat_id):
            return await event.edit(
                "This user is already muted in this chat ~~lmfao sed rip~~"
            )
        try:
            mute(userid, chat_id)
        except Exception as e:
            await event.edit("Error occured!\nError is " + str(e))
        else:
            await event.edit("Successfully muted that person.\n**｀-´)⊃━☆ﾟ.*･｡ﾟ **")


@friday.on(friday_on_cmd(pattern=r"unmute ?(\d+)?"))
async def endmute(event):
    private = False
    if event.fwd_from:
        return
    elif event.is_private:
        await event.edit("Unexpected issues or ugly errors may occur!")
        await asyncio.sleep(3)
        private = True
    if any(x in event.raw_text for x in ("/unmute", "!unmute")):
        await asyncio.sleep(0.5)
    else:
        reply = await event.get_reply_message()
        if event.pattern_match.group(1) is not None:
            userid = event.pattern_match.group(1)
        elif reply is not None:
            userid = reply.sender_id
        elif private:
            userid = event.chat_id
        else:
            return await event.edit(
                "Please reply to a user or add their userid into the command to unmute them."
            )
        chat_id = event.chat_id
        if not is_muted(userid, chat_id):
            return await event.edit(
                "__This user is not muted in this chat__\n（ ^_^）o自自o（^_^ ）"
            )
        try:
            unmute(userid, chat_id)
        except Exception as e:
            await event.edit("Error occured!\nError is " + str(e))
        else:
            await event.edit("Successfully unmuted that person\n乁( ◔ ౪◔)「    ┑(￣Д ￣)┍")

@command(incoming=True)
async def watcher(event):
    if is_muted(event.sender_id, event.chat_id):
        await event.delete()



CMD_HELP.update(
    {
        "mute": "**Mute**\
\n\n**Syntax : **`.mute <reply to a user/ mention username>`\
\n**Usage :** Mutes the user in a chat.\
\n\n**Syntax : **`.unmute <reply to a user/ mention username>`\
\n**Usage :** unmutes user in that chat."
    }
)
