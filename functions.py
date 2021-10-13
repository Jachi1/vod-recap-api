# Compress messages_per_second, emote_messages_per_second, and subscriber_messages_per_second to one command

def messages_per_second(chat: list, interval: int) -> dict:
    if interval < 1:
        return # Interval must be 1 sec. or more, make formal fix later
    else:
        current_pos = 0
        mps = {}
        for message in chat:
            position = int(message["time_in_seconds"] / interval)
            while current_pos <= position:
                mps.update({current_pos: 0})
                current_pos += 1
            mps[position] = mps[position] + 1
        return mps


def emote_messages_per_second(chat: list, interval: int) -> dict:
    if interval < 1:
        return # Interval must be 1 sec. or more, make formal fix later
    else:
        current_pos = 0
        mps = {}
        for message in chat:
            if message["is_emote"]:
                position = int(message["time_in_seconds"] / interval)
                while current_pos <= position:
                    mps.update({current_pos: 0})
                    current_pos += 1
                mps[position] = mps[position] + 1
        return mps


def subscriber_messages_per_second(chat: list, interval: int) -> dict:
    if interval < 1:
        return # Interval must be 1 sec. or more, make formal fix later
    else:
        current_pos = 0
        mps = {}
        for message in chat:
            if message["subscriber"]:
                position = int(message["time_in_seconds"] / interval)
                while current_pos <= position:
                    mps.update({current_pos: 0})
                    current_pos += 1
                mps[position] = mps[position] + 1
        return mps


def messages_per_user(chat: list) -> dict:
    mpc = {}
    for message in chat:
        author = str(message["author"])
        if author in mpc:
            mpc[author] += 1
        else:
            mpc.update({author: 1})
    return mpc


def emote_messages_per_user(chat: list) -> dict:
    mpc = {}
    for message in chat:
        if message["is_emote"]:
            author = str(message["author"])
            if author in mpc:
                mpc[author] += 1
            else:
                mpc.update({author: 1})
    return mpc


def emotes_by_usage(chat: list) -> dict:
    emote = {}
    for message in chat:
        if len(message["emotes"]) > 0:
            emotes = message["emotes"]
            for e in emotes:
                if e in emote:
                    emote[e] += 1
                else:
                    emote.update({e: 1})
    return emote
