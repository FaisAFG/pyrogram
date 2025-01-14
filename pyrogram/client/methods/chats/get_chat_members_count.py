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

from pyrogram.api import functions, types
from ...ext import BaseClient


class GetChatMembersCount(BaseClient):
    def get_chat_members_count(
        self,
        chat_id: Union[int, str]
    ) -> int:
        """Get the number of members in a chat.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

        Returns:
            ``int``: On success, the chat members count is returned.

        Raises:
            ValueError: In case a chat id belongs to user.

        Example:
            .. code-block:: python

                count = app.get_chat_members_count("pyrogramchat")
                print(count)
        """
        peer = self.resolve_peer(chat_id)

        if isinstance(peer, types.InputPeerChat):
            return self.send(
                functions.messages.GetChats(
                    id=[peer.chat_id]
                )
            ).chats[0].participants_count
        elif isinstance(peer, types.InputPeerChannel):
            return self.send(
                functions.channels.GetFullChannel(
                    channel=peer
                )
            ).full_chat.participants_count
        else:
            raise ValueError("The chat_id \"{}\" belongs to a user".format(chat_id))
