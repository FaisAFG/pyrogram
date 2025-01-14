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

from pyrogram.api import functions
from ...ext import BaseClient


class UpdateProfile(BaseClient):
    def update_profile(
        self,
        first_name: str = None,
        last_name: str = None,
        bio: str = None
    ) -> bool:
        """Update your profile details such as first name, last name and bio.
        
        You can omit the parameters you don't want to change.
        
        Parameters:
            first_name (``str``, *optional*):
                The new first name.
        
            last_name (``str``, *optional*):
                The new last name.
                Pass "" (empty string) to remove it.

            bio (``str``, *optional*):
                The new bio, also known as "about". Max 70 characters.
                Pass "" (empty string) to remove it.
                
        Returns:
            ``bool``: True on success.
        
        Example:
            .. code-block:: python
                
                # Update your first name only
                app.update_bio(first_name="Pyrogram")
                
                # Update first name and bio
                app.update_bio(first_name="Pyrogram", bio="https://docs.pyrogram.org/")
                
                # Remove the last name
                app.update_bio(last_name="")
        """

        return bool(
            self.send(
                functions.account.UpdateProfile(
                    first_name=first_name,
                    last_name=last_name,
                    about=bio
                )
            )
        )
