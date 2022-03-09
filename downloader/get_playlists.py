import argparse
import json
import os
import sys
import time

from collections import defaultdict

from requests import Session

from pytube import Channel


API_KEY = os.environ.get("YOUTUBE_API_TOKEN")
assert API_KEY

MAX_RESULTS_PER_PAGE = 50
PLAYLISTS_URL = "https://www.googleapis.com/youtube/v3/playlists"

class TextColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def get_plists(input_stream, output_stream):
    def _configure_ssl():
        import ssl
        ssl._create_default_https_context = ssl._create_unverified_context

    _configure_ssl()

    plists = defaultdict(list)

    session = Session()

    for channel_url in input_stream:
        if not channel_url.strip():
            continue

        channel = Channel(channel_url)

        try:
            channel_id = channel.channel_id
            channel_name = channel.channel_name
            base_params = {
                "channelId": channel_id,
                "part": "snippet",
                "key": API_KEY,
                "maxResults": MAX_RESULTS_PER_PAGE,
            }

            next_page_token = ""

            # youtube responses the same next page token on last page and further too :/
            has_next_page = True
            while has_next_page:
                response = session.get(
                    PLAYLISTS_URL,
                    params={
                        **base_params,
                        **{"pageToken": next_page_token},
                    },
                )

                assert response.status_code == 200
                data = response.json()

                next_page_token = data.get("nextPageToken")
                batch_items = data.get("items", [])
                plists[channel_name].extend(
                    list(
                        map(lambda item: {"id": item["id"], "title": item["snippet"]["title"]}, batch_items),
                    )
                )
                print(f"{TextColors.OKCYAN}[{channel_name}] Debug: loaded {len(batch_items)} playlists, next page is {next_page_token} {TextColors.ENDC}")

                has_next_page = bool(next_page_token)

                time.sleep(0.1)
            print(f"{TextColors.OKGREEN}[{channel_name}] Found {len(plists[channel_name])} playlists {TextColors.ENDC}")
        except Exception as exc:
            print(f"{TextColors.FAIL}Error on getting playlists: {exc}{TextColors.ENDC}")

    output_stream.write(json.dumps(plists))


parser = argparse.ArgumentParser(description='Process cmdline arguments')

parser.add_argument('--input', dest='input',
                    type=argparse.FileType("r"), default=sys.stdin,
                    help='input stream (default stdin)')

parser.add_argument('--output', dest='output',
                    type=argparse.FileType("w"), default=sys.stdout,
                    help='output stream (default stdout)')

args = parser.parse_args()

if __name__ == "__main__":
    get_plists(input_stream=args.input, output_stream=args.output)
