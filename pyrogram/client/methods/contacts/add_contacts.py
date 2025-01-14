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
from pyrogram.api import functions
from ...ext import BaseClient


class AddContacts(BaseClient):
    def add_contacts(
        self,
        contacts: List["pyrogram.InputPhoneContact"]
    ):
        """Add contacts to your Telegram address book.

        Parameters:
            contacts (List of :obj:`InputPhoneContact`):
                The contact list to be added

        Returns:
            :obj:`types.contacts.ImportedContacts`

        Example:
            .. code-block:: python

                from pyrogram import InputPhoneContact

                app.add_contacts([
                    InputPhoneContact("39123456789", "Foo"),
                    InputPhoneContact("38987654321", "Bar"),
                    InputPhoneContact("01234567891", "Baz")])
        """
        imported_contacts = self.send(
            functions.contacts.ImportContacts(
                contacts=contacts
            )
        )

        return imported_contacts
