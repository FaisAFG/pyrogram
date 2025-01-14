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

import inspect
import sqlite3
import time
from pathlib import Path
from threading import Lock
from typing import List, Tuple, Any

from pyrogram.api import types
from pyrogram.client.ext import utils
from .storage import Storage


def get_input_peer(peer_id: int, access_hash: int, peer_type: str):
    if peer_type in ["user", "bot"]:
        return types.InputPeerUser(
            user_id=peer_id,
            access_hash=access_hash
        )

    if peer_type == "group":
        return types.InputPeerChat(
            chat_id=-peer_id
        )

    if peer_type in ["channel", "supergroup"]:
        return types.InputPeerChannel(
            channel_id=utils.get_channel_id(peer_id),
            access_hash=access_hash
        )

    raise ValueError("Invalid peer type: {}".format(peer_type))


class SQLiteStorage(Storage):
    VERSION = 2
    USERNAME_TTL = 8 * 60 * 60

    def __init__(self, name: str):
        super().__init__(name)

        self.conn = None  # type: sqlite3.Connection
        self.lock = Lock()

    def create(self):
        with self.lock, self.conn:
            with open(str(Path(__file__).parent / "schema.sql"), "r") as schema:
                self.conn.executescript(schema.read())

            self.conn.execute(
                "INSERT INTO version VALUES (?)",
                (self.VERSION,)
            )

            self.conn.execute(
                "INSERT INTO sessions VALUES (?, ?, ?, ?, ?, ?)",
                (2, None, None, 0, None, None)
            )

    def open(self):
        raise NotImplementedError

    def save(self):
        self.date(int(time.time()))

        with self.lock:
            self.conn.commit()

    def close(self):
        with self.lock:
            self.conn.close()

    def delete(self):
        raise NotImplementedError

    def update_peers(self, peers: List[Tuple[int, int, str, str, str]]):
        with self.lock:
            self.conn.executemany(
                "REPLACE INTO peers (id, access_hash, type, username, phone_number)"
                "VALUES (?, ?, ?, ?, ?)",
                peers
            )

    def get_peer_by_id(self, peer_id: int):
        r = self.conn.execute(
            "SELECT id, access_hash, type FROM peers WHERE id = ?",
            (peer_id,)
        ).fetchone()

        if r is None:
            raise KeyError("ID not found: {}".format(peer_id))

        return get_input_peer(*r)

    def get_peer_by_username(self, username: str):
        r = self.conn.execute(
            "SELECT id, access_hash, type, last_update_on FROM peers WHERE username = ?",
            (username,)
        ).fetchone()

        if r is None:
            raise KeyError("Username not found: {}".format(username))

        if abs(time.time() - r[3]) > self.USERNAME_TTL:
            raise KeyError("Username expired: {}".format(username))

        return get_input_peer(*r[:3])

    def get_peer_by_phone_number(self, phone_number: str):
        r = self.conn.execute(
            "SELECT id, access_hash, type FROM peers WHERE phone_number = ?",
            (phone_number,)
        ).fetchone()

        if r is None:
            raise KeyError("Phone number not found: {}".format(phone_number))

        return get_input_peer(*r)

    def _get(self):
        attr = inspect.stack()[2].function

        return self.conn.execute(
            "SELECT {} FROM sessions".format(attr)
        ).fetchone()[0]

    def _set(self, value: Any):
        attr = inspect.stack()[2].function

        with self.lock, self.conn:
            self.conn.execute(
                "UPDATE sessions SET {} = ?".format(attr),
                (value,)
            )

    def _accessor(self, value: Any = object):
        return self._get() if value == object else self._set(value)

    def dc_id(self, value: int = object):
        return self._accessor(value)

    def test_mode(self, value: bool = object):
        return self._accessor(value)

    def auth_key(self, value: bytes = object):
        return self._accessor(value)

    def date(self, value: int = object):
        return self._accessor(value)

    def user_id(self, value: int = object):
        return self._accessor(value)

    def is_bot(self, value: bool = object):
        return self._accessor(value)

    def version(self, value: int = object):
        if value == object:
            return self.conn.execute(
                "SELECT number FROM version"
            ).fetchone()[0]
        else:
            with self.lock, self.conn:
                self.conn.execute(
                    "UPDATE version SET number = ?",
                    (value,)
                )
