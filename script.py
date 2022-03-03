import pytube
import re

YOUTUBE_STREAM_AUDIO = '140'

with open('playlists.txt', 'r') as r:
    for line in r:
        playlist = line.strip()
        playlist = pytube.Playlist(playlist)
        playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
        title = playlist.title.replace('/', '-', 100).replace('\\', '-', 100)
        print(f"--- Download playlist {title} ---")
        #print(playlist)
        path_for_saved = f'./{title}'
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
