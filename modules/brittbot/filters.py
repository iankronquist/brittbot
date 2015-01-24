#!/usr/bin/env python
'''
brittbot/filters.py - jenni Spam filters

More info:
 * jenni: https://github.com/myano/jenni/
'''

import re
from functools import wraps

ignored_nicks = [
    ".*bot",
]

limited_channels = {
}


def check_ignore(msg):
    ignore = False
    if not msg.sender.startswith("#"):
        ignore = True
    for ignored_nick in ignored_nicks:
        if re.search(re.compile(ignored_nick, re.IGNORECASE), msg.nick):
            ignore = True
            print "%s is ignored by rule %s" % (
                msg.nick,
                ignored_nick
            )
    if msg.admin:
        ignore = False
    return ignore


def is_allowed(function_name, jenni, msg):
    irc_room = msg.sender
    filters = jenni.config.channel_filters
    allowed = True
    if irc_room in filters:
        if 'blocked' in filters[irc_room]:
            if function_name in filters[irc_room]['blocked']:
                allowed = False
        if 'allowed' in filters[irc_room]:
            allowed = function_name in filters[irc_room]['allowed']
    return allowed


def smart_ignore(fn):
    @wraps(fn)
    def callable(jenni, msg):
        function_name = fn.__name__
        default_fn = lambda jenni, msg: None
        if not is_allowed(function_name, jenni, msg):
            return default_fn
        return fn(jenni, msg)
    return callable