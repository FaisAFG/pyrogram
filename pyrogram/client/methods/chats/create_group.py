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

from typing import Union, List

import pyrogram
from pyrogram.api import functions
from ...ext import BaseClient


class CreateGroup(BaseClient):
    def create_group(
        self,
        title: str,
        users: Union[Union[int, str], List[Union[int, str]]]
    ) -> "pyrogram.Chat":
        """Create a new basic group.

        .. note::

            If you want to create a new supergroup, use :meth:`~pyrogram.Client.create_supergroup` instead.

        Parameters:
            title (``str``):
                The group title.

            users (``int`` | ``str`` | List of ``int`` or ``str``):
                Users to create a chat with.
                You must pass at least one user using their IDs (int), usernames (str) or phone numbers (str).
                Multiple users can be invited by passing a list of IDs, usernames or phone numbers.

        Returns:
            :obj:`Chat`: On success, a chat object is returned.

        Example:
            .. code-block:: python

                app.create_group("Group Title", user_id)
        """
        if not isinstance(users, list):
            users = [users]

        r = self.send(
            functions.messages.CreateChat(
                title=title,
                users=[self.resolve_peer(u) for u in users]
            )
        )

        return pyrogram.Chat._parse_chat(self, r.chats[0])
