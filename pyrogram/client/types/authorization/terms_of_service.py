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

from pyrogram.api import types
from ..messages_and_media import MessageEntity
from ..object import Object


class TermsOfService(Object):
    """Telegram's Terms of Service returned by :meth:`~Client.sign_in`.

    Parameters:
        id (``str``):
            Terms of Service identifier.

        text (``str``):
            Terms of Service text.

        entities (List of :obj:`MessageEntity`):
            Special entities like URLs that appear in the text.
    """

    def __init__(self, *, id: str, text: str, entities: List[MessageEntity]):
        super().__init__()

        self.id = id
        self.text = text
        self.entities = entities

    @staticmethod
    def _parse(terms_of_service: types.help.TermsOfService) -> "TermsOfService":
        return TermsOfService(
            id=terms_of_service.id.data,
            text=terms_of_service.text,
            entities=[
                MessageEntity._parse(None, entity, {})
                for entity in terms_of_service.entities
            ]
        )
