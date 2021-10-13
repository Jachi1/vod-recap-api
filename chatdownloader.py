import re

from chat_downloader import ChatDownloader
from collections import namedtuple


class TwitchVodDownloader:
    Badge = namedtuple('Badge', ['name', 'title'])
    SubBadgeInfo = namedtuple('SubBadge', ['num', 'timescale'])
    subscriber_duration_count = re.compile(r"([0-9][.]?[0-9]?[0-9]?-[Y|M])", re.IGNORECASE)


    def load_metadata(self, url: str) -> dict:
        try:
            chat = ChatDownloader().get_chat(url)
            return [x for x in chat]
        except:
            print(f"VOD does not exist.")
            raise Exception("VOD does not exist")


    def parse(self, metadata: dict) -> list:
        parsed_metadata = []
        for elem in metadata:
            parsed_elem = {
                "message": elem["message"],
                "author": elem["author"]["display_name"],
                "timestamp": elem["timestamp"],
                "time_stamp_in_vod": elem["time_text"],
                "time_in_seconds": elem["time_in_seconds"],
                "is_emote": self.check_if_emote(elem),
                "emotes": self.get_emotes(elem),
                "subscriber": self.check_if_subscribed(elem),
                "subscription_duration": self.check_sub_duration(elem),
            }
            parsed_metadata.append(parsed_elem)
        return parsed_metadata


    def check_if_emote(self, elem: dict) -> bool:
        if "emotes" in elem.keys(): return True
        return False

    def get_emotes(self, elem: dict) -> list:
        if "emotes" in elem.keys(): return [x["name"] for x in elem["emotes"]]
        return []
        

    def check_if_subscribed(self, elem: dict) -> None:
        if "badges" in elem["author"].keys():
            badges = [self.Badge(name=x["name"], title=x["title"]) for x in elem["author"]["badges"]]
            if "subscriber" in [x.name for x in badges]: return True
        return False


    def check_sub_duration(self, elem: dict) -> int:
        if "badges" in elem["author"].keys():
            badges = [self.Badge(name=x["name"], title=x["title"]) for x in elem["author"]["badges"]]
            if "subscriber" not in [x.name for x in badges]: return 0
            else:    
                for badge in badges:
                    if badge.name == "subscriber": return self.duration_conversion(badge.title)
        return 0


    def duration_conversion(self, dur_str: str) -> int:
        if dur_str.lower() == "subscriber":
            return 1
        if badge := self.subscriber_duration_count.match(dur_str):
            parsed_badge = badge[0].split('-')
            badge_info = self.SubBadgeInfo(num=float(parsed_badge[0]), timescale=parsed_badge[1])
            if badge_info.timescale.upper() == 'Y':
                return int(badge_info.num * 12)
            return badge_info.num
        else:
            print(f"Error parsing subscriber duration: {dur_str}")
        
        
    def get_chat(self, url: str) -> list:
        vod_msg_metadata = self.load_metadata(url)
        try:
            chat = self.parse(vod_msg_metadata)
            print("Finished getting the chat")
            return chat
        except Exception as err:
            print(f"Failed to fetch chat from vod: {err}")
            return {"err", f"Failed to fetch vod: {err}"}


class YoutubeVodDownloader:
    Badge = namedtuple('Badge', ['title'])
    SubBadgeInfo = namedtuple('SubBadge', ['num', 'timescale'])
    member_check = re.compile(r"(new member|member)", re.IGNORECASE)
    member_duration_count = re.compile(r"([0-9][.]?[0-9]?[0-9]? [y|m])", re.IGNORECASE)


    def load_metadata(self, url: str) -> dict:
        try:
            chat = ChatDownloader().get_chat(url)
            return [x for x in chat]
        except:
            print(f"VOD does not exist.")
            raise Exception("VOD does not exist")


    def parse(self, metadata: dict) -> list:
        parsed_metadata = []
        for elem in metadata:
            parsed_elem = {
                "message": elem["message"],
                "author": elem["author"]["name"],
                "timestamp": elem["timestamp"],
                "time_stamp_in_vod": elem["time_text"],
                "time_in_seconds": elem["time_in_seconds"],
                "is_emote": self.check_if_emote(elem),
                "emotes": self.get_emotes(elem),
                "subscriber": self.check_if_subscribed(elem),
                "subscription_duration": self.check_sub_duration(elem),
            }
            parsed_metadata.append(parsed_elem)
        return parsed_metadata


    def check_if_emote(self, elem: dict) -> bool:
        if "emotes" in elem.keys(): return True
        return False

    def get_emotes(self, elem: dict) -> list:
        if "emotes" in elem.keys(): return [x["name"] for x in elem["emotes"]]
        return []
        

    def check_if_subscribed(self, elem: dict) -> None:
        if "badges" in elem["author"].keys():
            badges = [self.Badge(title=x["title"].lower()) for x in elem["author"]["badges"]]
            for badge in badges:
                if self.member_check.match(badge.title): return True
        return False


    def check_sub_duration(self, elem: dict) -> int:
        if "badges" in elem["author"].keys():
            badges = [self.Badge(title=x["title"].lower()) for x in elem["author"]["badges"]]
            for badge in badges:
                if self.member_check.match(badge.title): return self.duration_conversion(badge.title)
        return 0


    def duration_conversion(self, dur_str: str) -> int:
        if dur_str == "new member":
            return 1

        if badge := self.member_duration_count.search(dur_str):
            parsed_badge = badge[0].split(' ')
            badge_info = self.SubBadgeInfo(num=float(parsed_badge[0]), timescale=parsed_badge[1])
            if badge_info.timescale == 'y':
                return int(badge_info.num * 12)
            return badge_info.num
        else:
            print(f"Error parsing subscriber duration: {dur_str}")
        
        
    def get_chat(self, url: str) -> list:
        vod_msg_metadata = self.load_metadata(url)
        try:
            chat = self.parse(vod_msg_metadata)
            print("Finished getting the chat")
            return chat
        except Exception as err:
            print(f"Failed to fetch chat from vod: {err}")
            return {"err", f"Failed to fetch vod: {err}"}
