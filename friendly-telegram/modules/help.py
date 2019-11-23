# -*- coding: future_fstrings -*-

#    Friendly Telegram (telegram userbot)
#    Copyright (C) 2018-2019 The Authors

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging
import inspect

from telethon.tl.functions.channels import JoinChannelRequest

from .. import loader, utils

logger = logging.getLogger(__name__)


def register(cb):
    cb(HelpMod())


class HelpMod(loader.Module):
    """Provides this help message"""
    def __init__(self):
        super().__init__()
        self.name = _("Help")
        self.allmodules = None
        self.client = None

    async def helpcmd(self, message):
        """.help [module]"""
        args = utils.get_args_raw(message)
        if args:
            module = None
            for mod in self.allmodules.modules:
                if mod.name.lower() == args.lower():
                    module = mod
            if module is None:
                await message.edit("<code>" + _("Invalid module name specified") + "</code>")
                return
            # Translate the format specification and the module seperately
            reply = "<b>" + _("Help for</b> <code>{}</code>:").format(utils.escape_html(_(module.name))) + "\n  "
            if module.__doc__:
                reply += utils.escape_html(inspect.cleandoc(module.__doc__))
            else:
                logger.warning("Module %s is missing docstring!", module)
            for name, fun in module.commands.items():
                reply += f"\n  <code>{name}</code>\n"
                if fun.__doc__:
                    reply += utils.escape_html("\n".join(["    " + x for x in
                                                          _(inspect.cleandoc(fun.__doc__)).splitlines()]))
                else:
                    reply += _("There is no documentation for this command")
        else:
            reply = "<b>" + _("Available Modules:") + "</b>"
            for mod in self.allmodules.modules:
                reply += _("\n• <b>{}</b> ({})").format(mod.name, len(mod.commands))
                first = True
                for cmd in mod.commands:
                    if first:
                        reply += f"\n  <code>{cmd}"
                        first = False
                    else:
                        reply += f", {cmd}"
                reply += "</code>"
        await utils.answer(message, reply)

    async def supportcmd(self, message):
        """Joins the support chat"""
        await self.client(JoinChannelRequest("https://t.me/friendlytgbot"))
        await message.edit(_("<code>Joined to</code> <a href='https://t.me/friendlytgbot'>support chat</a>"))

    async def client_ready(self, client, db):
        self.client = client
