import pytube
import re

YOUTUBE_STREAM_AUDIO = '140'

with open('channels.txt', 'r') as r:
    for line in r:
        channel = line.strip()
        channel = pytube.Channel(channel)
        channel._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
        title = channel.channel_name.replace('/', '-', 100).replace('\\', '-', 100)
        print(f"--- Download videos from channel {title} ---")
        path_for_saved = f'./{title}'
        print('Number of videos on channel: %s' % len(channel.video_urls))
        count_downloaded = 0
        count_on_channel = len(channel.video_urls)
        for video in channel.videos:
            video.streams.\
            filter(type='video', progressive=True, file_extension='mp4').\
            order_by('resolution').\
            desc().\
            first().\
            download(path_for_saved)
            count_downloaded += 1
            print(f"Downloaded {count_downloaded}/{count_on_channel} videos")
