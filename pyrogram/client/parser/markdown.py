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

import html
import re
from typing import Union

import pyrogram
from . import utils
from .html import HTML

BOLD_DELIM = "**"
ITALIC_DELIM = "__"
UNDERLINE_DELIM = "--"
STRIKE_DELIM = "~~"
CODE_DELIM = "`"
PRE_DELIM = "```"

MARKDOWN_RE = re.compile(r"({d})|\[(.+?)\]\((.+?)\)".format(
    d="|".join(
        ["".join(i) for i in [
            [r"\{}".format(j) for j in i]
            for i in [
                PRE_DELIM,
                CODE_DELIM,
                STRIKE_DELIM,
                UNDERLINE_DELIM,
                ITALIC_DELIM,
                BOLD_DELIM
            ]
        ]]
    )))

OPENING_TAG = "<{}>"
CLOSING_TAG = "</{}>"
URL_MARKUP = '<a href="{}">{}</a>'
FIXED_WIDTH_DELIMS = [CODE_DELIM, PRE_DELIM]


class Markdown:
    def __init__(self, client: Union["pyrogram.BaseClient", None]):
        self.html = HTML(client)

    def parse(self, text: str, strict: bool = False):
        if strict:
            text = html.escape(text)

        delims = set()
        is_fixed_width = False

        for i, match in enumerate(re.finditer(MARKDOWN_RE, text)):
            start, _ = match.span()
            delim, text_url, url = match.groups()
            full = match.group(0)

            if delim in FIXED_WIDTH_DELIMS:
                is_fixed_width = not is_fixed_width

            if is_fixed_width and delim not in FIXED_WIDTH_DELIMS:
                continue

            if text_url:
                text = utils.replace_once(text, full, URL_MARKUP.format(url, text_url), start)
                continue

            if delim == BOLD_DELIM:
                tag = "b"
            elif delim == ITALIC_DELIM:
                tag = "i"
            elif delim == UNDERLINE_DELIM:
                tag = "u"
            elif delim == STRIKE_DELIM:
                tag = "s"
            elif delim == CODE_DELIM:
                tag = "code"
            elif delim == PRE_DELIM:
                tag = "pre"
            else:
                continue

            if delim not in delims:
                delims.add(delim)
                tag = OPENING_TAG.format(tag)
            else:
                delims.remove(delim)
                tag = CLOSING_TAG.format(tag)

            text = utils.replace_once(text, delim, tag, start)

        return self.html.parse(text)

    @staticmethod
    def unparse(text: str, entities: list):
        text = utils.add_surrogates(text)

        entities_offsets = []

        for entity in entities:
            entity_type = entity.type
            start = entity.offset
            end = start + entity.length

            if entity_type == "bold":
                start_tag = end_tag = BOLD_DELIM
            elif entity_type == "italic":
                start_tag = end_tag = ITALIC_DELIM
            elif entity_type == "underline":
                start_tag = end_tag = UNDERLINE_DELIM
            elif entity_type == "strike":
                start_tag = end_tag = STRIKE_DELIM
            elif entity_type == "code":
                start_tag = end_tag = CODE_DELIM
            elif entity_type in ("pre", "blockquote"):
                start_tag = end_tag = PRE_DELIM
            elif entity_type == "text_link":
                url = entity.url
                start_tag = "["
                end_tag = "]({})".format(url)
            elif entity_type == "text_mention":
                user = entity.user
                start_tag = "["
                end_tag = "](tg://user?id={})".format(user.id)
            else:
                continue

            entities_offsets.append((start_tag, start,))
            entities_offsets.append((end_tag, end,))

        # sorting by offset (desc)
        entities_offsets.sort(key=lambda x: -x[1])

        for entity, offset in entities_offsets:
            text = text[:offset] + entity + text[offset:]

        return utils.remove_surrogates(text)
