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
from ...ext import BaseClient, utils


class GetChat(BaseClient):
    def get_chat(
        self,
        chat_id: Union[int, str]
    ) -> Union["pyrogram.Chat", "pyrogram.ChatPreview"]:
        """Get up to date information about a chat.

        Information include current name of the user for one-on-one conversations, current username of a user, group or
        channel, etc.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                Unique identifier for the target chat in form of a *t.me/joinchat/* link, identifier (int) or username
                of the target channel/supergroup (in the format @username).

        Returns:
            :obj:`Chat` | :obj:`ChatPreview`: On success, if you've already joined the chat, a chat object is returned,
            otherwise, a chat preview object is returned.

        Raises:
            ValueError: In case the chat invite link points to a chat you haven't joined yet.

        Example:
            .. code-block:: python

                chat = app.get_chat("pyrogram")
                print(chat)
        """
        match = self.INVITE_LINK_RE.match(str(chat_id))

        if match:
            r = self.send(
                functions.messages.CheckChatInvite(
                    hash=match.group(1)
                )
            )

            if isinstance(r, types.ChatInvite):
                return pyrogram.ChatPreview._parse(self, r)

            self.fetch_peers([r.chat])

            if isinstance(r.chat, types.Chat):
                chat_id = -r.chat.id

            if isinstance(r.chat, types.Channel):
                chat_id = utils.get_channel_id(r.chat.id)

        peer = self.resolve_peer(chat_id)

        if isinstance(peer, types.InputPeerChannel):
            r = self.send(functions.channels.GetFullChannel(channel=peer))
        elif isinstance(peer, (types.InputPeerUser, types.InputPeerSelf)):
            r = self.send(functions.users.GetFullUser(id=peer))
        else:
            r = self.send(functions.messages.GetFullChat(chat_id=peer.chat_id))

        return pyrogram.Chat._parse_full(self, r)
