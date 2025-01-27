import tls_client
import requests
from logger import *
import random
from fingerprints import fps
from datetime import datetime, timedelta
import base64
import json
import yaml

with open('config.yml') as c:
  config = yaml.safe_load(c)

def encode_to_base64(json_object):
    json_str = json.dumps(json_object)
    json_bytes = json_str.encode("utf-8")
    base64_bytes = base64.b64encode(json_bytes)
    base64_str = base64_bytes.decode("utf-8")
    return base64_str


def get_cookies() -> dict:
    try:
        response = requests.get("https://discord.com").cookies
        cookies = {
            "__dcfduid": response.get("__dcfduid"),
            "__sdcfduid": response.get("__sdcfduid"),
            "_cfuvid": response.get("_cfuvid"),
            "__cfruid": response.get("__cfruid"),
        }
        return cookies
    except Exception as e:
        return {}


invite = inp("Enter Server Invite > ")
threads = int(inp("Enter Amount Of Threads > "))
num_b = int(inp("Enter Number Of Tokens To Use ( Formula: Number Of Boosts To Put / 2 ) > "))
if "https://discord.gg/" in invite:
    invite = invite.replace("https://discord.gg/", "")
else:
    invite = invite


def ran_str():
    return "".join(
        random.choice("9830da1a6f376cc753f0fbc28d1ffbbe")
        for _ in range(len("9830da1a6f376cc753f0fbc28d1ffbbe"))
    )


def get_context_properties(token):
    chrome = "126"  # chrome_version.
    fingerprint_dict = random.choice(fps)
    ja3 = fingerprint_dict["ja3"]
    user_agent = fingerprint_dict["user-agent"]
    x_super_properties = fingerprint_dict["x-super-properties"]
    session = tls_client.Session(
        client_identifier="chrome_" + chrome,
        ja3_string=ja3,
        random_tls_extension_order=True,
    )
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "authorization": token,
        "priority": "u=1, i",
        "referer": "https://discord.com/channels",
        "sec-ch-ua": f'"Not)A;Brand";v="99", "Microsoft Edge";v="{chrome}", "Chromium";v="{chrome}"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": user_agent,
        "x-debug-options": "bugReporterEnabled",
        "x-discord-locale": "en-US",
        "x-discord-timezone": "Asia/Katmandu",
        "x-super-properties": x_super_properties,
    }
    params = {
        "inputValue": invite,
        "with_counts": "true",
        "with_expiration": "true",
    }
    response = session.get(
        "https://discord.com/api/v9/invites/wumpus",
        params=params,
        cookies=get_cookies(),
        headers=headers,
    )
    data_to_encode = {
        "location": "Join Guild",
        "location_guild_id": response.json()["guild"]["id"],
        "location_channel_id": response.json()["channel"]["id"],
        "location_channel_type": 5,
    }
    encoded_data = encode_to_base64(data_to_encode)
    return encoded_data


import httpx


def get_fingerprint():
    try:
        fingerprint = httpx.get(f"https://discord.com/api/v10/experiments")
        return fingerprint.json()["fingerprint"]
    except Exception as e:
        return get_fingerprint()


class btool:
    def __init__(self, token):
        self.chrome = "126"  # chrome_version.
        fingerprint_dict = random.choice(fps)
        self.ja3 = fingerprint_dict["ja3"]
        self.user_agent = fingerprint_dict["user-agent"]
        self.x_super_properties = fingerprint_dict["x-super-properties"]
        self.session = tls_client.Session(
            client_identifier="chrome_" + self.chrome, random_tls_extension_order=True
        )
        if config["UseProxy"]:
          self.session.proxies = {
            'https': 'http://'+config["Proxy"],
            'http': 'http://'+config["Proxy"]
          }
        else:
          self.session.proxies = None
        self.token = token.split(":")[2] if "@" in token else token
        log("INFO", f"Using [{self.token[:23]}***-***]")
        self.full_token = token
        self.headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "authorization": self.token,
            "content-type": "application/json",
            "origin": "https://discord.com",
            "priority": "u=1, i",
            "referer": "https://discord.com",
            "sec-ch-ua": f'"Not)A;Brand";v="99", "Microsoft Edge";v="{self.chrome}", "Chromium";v="{self.chrome}"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": self.user_agent,
            "x-debug-options": "bugReporterEnabled",
            "x-discord-locale": "en-US",
            "x-discord-timezone": "Asia/Katmandu",
            "x-super-properties": self.x_super_properties,
        }
        self.join_data = {
            "session_id": ran_str(),
        }

    def join_guild(self) -> bool:
        r = self.session.post(
            "https://discord.com/api/v9/invites/" + invite,
            headers=self.headers,
            json=self.join_data,
            cookies=get_cookies(),
        )
        if r.status_code == 200:
            log("DBG", "Joined Guild: {}".format(invite))
            self.guild = r.json()["guild"]["id"]
            return True
        else:
            log("ERR", f"Failed To Join Guild: {r.json()}")
            return False

    def put_boost(self) -> bool:
        if self.guild:
            try:

                boost_dat = self.session.get(
                    f"https://discord.com/api/v9/users/@me/guilds/premium/subscription-slots",
                    headers=self.headers,
                    cookies=get_cookies(),
                )
                if boost_dat.status_code == 200:
                    boost_data = boost_dat.json()
                    for boost in boost_data:
                        boost_id = boost["id"]
                        payload = {
                            "user_premium_guild_subscription_slot_ids": [boost_id]
                        }
                        boosted = self.session.put(
                            f"https://discord.com/api/v9/guilds/{self.guild}/premium/subscriptions",
                            json=payload,
                            headers=self.headers,
                        )
                        if boosted.status_code == 201:
                            log(
                                "SUCCESS",
                                f"Boosted Server [{invite}] With {self.token[:23]}***-***",
                            )
                            write_to_file("output/boosted.txt", self.full_token)
                        elif (
                            "Must wait for premium server subscription cooldown to expire"
                            in boosted.text
                        ):
                            log(
                                "ERROR",
                                f"Insufficient Boosts: {self.token[:23]}***-***",
                            )
                            write_to_file("output/boosting_error.txt", self.full_token)
                        else:
                            log("ERROR", f"Boosting Error: {boosted.json()}")
                            write_to_file("output/boosting_error.txt", self.full_token)
                else:
                    write_to_file("output/boosting_error.txt", self.full_token)
                    log("ERROR", "Failed To Fetch Boost Data")
            except Exception as e:
                log("ERROR", "ERROR: {}".format(e))
        else:
            log("WARN", f"Failed To Join... So Not Boosting!")


def process(token):
    ins = btool(token=token)
    j = ins.join_guild()
    ins.put_boost()


from concurrent.futures import ThreadPoolExecutor

with open("input/tokens.txt", "r") as f:
    tokens = f.read().splitlines()[:num_b]

with ThreadPoolExecutor(max_workers=threads) as exc:
    for tok in tokens:
        exc.submit(process, tok)
