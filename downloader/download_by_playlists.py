import sys
import argparse
import pytube
import re
import json

from pathlib import Path


YOUTUBE_STREAM_AUDIO = '140'

PLAYLIST_URL_FORMAT = 'https://www.youtube.com/playlist?list={}'

def download(filestream):
    def _configure_ssl():
        import ssl
        ssl._create_default_https_context = ssl._create_unverified_context

    _configure_ssl()

    config = json.loads(filestream.read())

    for channel_name, plist_ids in config.items():
        for plst in plist_ids:
            playlist_id = plst["id"]
            playlist_title = plst["title"]
            playlist = pytube.Playlist(PLAYLIST_URL_FORMAT.format(playlist_id))
            playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
            title = playlist.title.replace('/', '-', 100).replace('\\', '-', 100)
            print(f"--- Download playlist {title} ---")
            #print(playlist)

            Path(f"./{channel_name}/{playlist_title}").mkdir(parents=True, exist_ok=True)

            path_for_saved = f'./{channel_name}/{title}'

            print('Number of videos in playlist: %s' % len(playlist.video_urls))
            #playlist.download_all()
            count_downloaded = 0
            count_in_playlist = len(playlist.video_urls)
            for video in playlist.videos:
                video.streams.\
                filter(type='video', progressive=True, file_extension='mp4').\
                order_by('resolution').\
                desc().\
                first().\
                download(path_for_saved)
                #playlist.download()
                count_downloaded += 1
                print(f"Downloaded {count_downloaded}/{count_in_playlist} videos")

parser = argparse.ArgumentParser(description='Process cmdline arguments')

parser.add_argument('--input', dest='input',
                    type=argparse.FileType("r"), default=sys.stdin,
                    help='input stream (default stdin)')

args = parser.parse_args()

if __name__ == "__main__":
    download(filestream=args.input)
