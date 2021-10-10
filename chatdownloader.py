from chat_downloader import ChatDownloader

import re
from collections import namedtuple

Badge = namedtuple('Badge', ['name', 'title'])
SubBadgeInfo = namedtuple('SubBadge', ['num', 'timescale'])
subscriber_duration_count = re.compile(r"([0-9][.]?[0-9]?[0-9]?-[Y|M])", re.IGNORECASE)


def load_metadata(url: str) -> dict:
    try:
        chat = ChatDownloader().get_chat(url)
        return [x for x in chat]
    except:
        print(f"VOD does not exist.")
        raise Exception("VOD does not exist")


def parse(metadata: dict) -> list:
    parsed_metadata = []
    for elem in metadata:
        parsed_elem = {
            "message": elem["message"],
            "author": elem["author"]["display_name"],
            "timestamp": elem["timestamp"],
            "time_stamp_in_vod": elem["time_text"],
            "time_in_seconds": elem["time_in_seconds"],
            "is_emote": check_if_emote(elem),
            "subscriber": check_if_subscribed(elem),
            "subscription_duration": check_sub_duration(elem),
        }
        parsed_metadata.append(parsed_elem)
    return parsed_metadata


def check_if_emote(elem: dict) -> bool:
    if "emotes" in elem.keys(): return True
    return False


def check_if_subscribed(elem: dict) -> None:
    if "badges" in elem["author"].keys():
        badges = [Badge(name=x["name"], title=x["title"]) for x in elem["author"]["badges"]]
        if "subscriber" in [x.name for x in badges]: return True
    return False


def check_sub_duration(elem: dict) -> int:
    if "badges" in elem["author"].keys():
        badges = [Badge(name=x["name"], title=x["title"]) for x in elem["author"]["badges"]]
        if "subscriber" not in [x.name for x in badges]: return 0
        else:    
            for badge in badges:
                if badge.name == "subscriber": return duration_conversion(badge.title)
    return 0


def duration_conversion(dur_str: str) -> int:
    if dur_str.lower() == "subscriber":
        return 1
    if badge := subscriber_duration_count.match(dur_str):
        parsed_badge = badge[0].split('-')
        badge_info = SubBadgeInfo(num=float(parsed_badge[0]), timescale=parsed_badge[1])
        if badge_info.timescale.upper() == 'Y':
            return int(badge_info.num * 12)
        return badge_info.num
    else:
        print(f"Error parsing subscriber duration: {dur_str}")
    
    
def get_chat(url: str) -> list:
    vod_msg_metadata = load_metadata(url)
    try:
        chat = parse(vod_msg_metadata)
        print("Finished getting the chat")
        return chat
    except Exception as err:
        print(f"Failed to fetch chat from vod: {err}")
        return {"err", f"Failed to fetch vod: {err}"}
