# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2020 Dan <https://github.com/delivrance>
#
# This file is part of Pyrogram.
#
# Pyrogram is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pyrogram is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from typing import Union

import pyrogram
from pyrogram.api import functions, types
from ...ext import BaseClient


class KickChatMember(BaseClient):
    def kick_chat_member(
        self,
        chat_id: Union[int, str],
        user_id: Union[int, str],
        until_date: int = 0
    ) -> Union["pyrogram.Message", bool]:
        """Kick a user from a group, a supergroup or a channel.
        In the case of supergroups and channels, the user will not be able to return to the group on their own using
        invite links, etc., unless unbanned first. You must be an administrator in the chat for this to work and must
        have the appropriate admin rights.

        Note:
            In regular groups (non-supergroups), this method will only work if the "All Members Are Admins" setting is
            off in the target group. Otherwise members may only be removed by the group's creator or by the member
            that added them.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target user.
                For a contact that exists in your Telegram address book you can use his phone number (str).

            until_date (``int``, *optional*):
                Date when the user will be unbanned, unix time.
                If user is banned for more than 366 days or less than 30 seconds from the current time they are
                considered to be banned forever. Defaults to 0 (ban forever).

        Returns:
            :obj:`Message` | ``bool``: On success, a service message will be returned (when applicable), otherwise, in
            case a message object couldn't be returned, True is returned.

        Example:
            .. code-block:: python

                from time import time

                # Ban chat member forever
                app.kick_chat_member(chat_id, user_id)

                # Kick chat member and automatically unban after 24h
                app.kick_chat_member(chat_id, user_id, int(time.time() + 86400))
        """
        chat_peer = self.resolve_peer(chat_id)
        user_peer = self.resolve_peer(user_id)

        if isinstance(chat_peer, types.InputPeerChannel):
            r = self.send(
                functions.channels.EditBanned(
                    channel=chat_peer,
                    user_id=user_peer,
                    banned_rights=types.ChatBannedRights(
                        until_date=until_date,
                        view_messages=True,
                        send_messages=True,
                        send_media=True,
                        send_stickers=True,
                        send_gifs=True,
                        send_games=True,
                        send_inline=True,
                        embed_links=True
                    )
                )
            )
        else:
            r = self.send(
                functions.messages.DeleteChatUser(
                    chat_id=abs(chat_id),
                    user_id=user_peer
                )
            )

        for i in r.updates:
            if isinstance(i, (types.UpdateNewMessage, types.UpdateNewChannelMessage)):
                return pyrogram.Message._parse(
                    self, i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats}
                )
        else:
            return True
