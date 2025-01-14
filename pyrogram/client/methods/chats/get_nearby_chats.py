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

from typing import List

import pyrogram
from pyrogram.api import functions, types
from ...ext import BaseClient, utils


class GetNearbyChats(BaseClient):
    def get_nearby_chats(
        self,
        latitude: float,
        longitude: float
    ) -> List["pyrogram.Chat"]:
        """Get nearby chats.

        Parameters:
            latitude (``float``):
                Latitude of the location.

            longitude (``float``):
                Longitude of the location.

        Returns:
            List of :obj:`Chat`: On success, a list of nearby chats is returned.

        Example:
            .. code-block:: python

                chats = app.get_nearby_chats(51.500729, -0.124583)
                print(chats)
        """

        r = self.send(
            functions.contacts.GetLocated(
                geo_point=types.InputGeoPoint(
                    lat=latitude,
                    long=longitude
                )
            )
        )

        if not r.updates:
            return []

        chats = pyrogram.List([pyrogram.Chat._parse_chat(self, chat) for chat in r.chats])
        peers = r.updates[0].peers

        for peer in peers:
            chat_id = utils.get_channel_id(peer.peer.channel_id)

            for chat in chats:
                if chat.id == chat_id:
                    chat.distance = peer.distance
                    break

        return chats
