# youtube_download
Прога для того, чтобы качать с youtube ролики из плейлистов

Инструкция:


```
1. pip3 install pytube
2. Качаем скрипт в место, куда будут загружаться видео
3. Создаём файлик .json, куда кладем конфиг в формате {"<название канала>": ["playlist_id_1",  "playlist_id_2", ...], ...}
4. cd downloader
5. Если вам нужно получить конфиг по названию канала, то получаем youtube api token, делаем export YOUTUBE_API_TOKEN=<your_token> и делаем cat channels.txt | python get_playlists.py --output config.json. В channels.txt должны лежать ссылки на каналы в формате https://www.youtube.com/channel/UCV56iySuhfRQ1qSjXmAr1Yw
6. python download_by_playlists.py --input config.json
7. В папках, соответствующих названиям каналов будут лежать видосы по плейлистам
```
Overall, можно запускать так:
```
export YOUTUBE_API_TOKEN=<your_token>
cat channels.txt | python get_playlists.py | python download_by_playlists.py
```

Каждый плейлист будет в отдельной папке
Если непонятно как делать playlists.txt - приложил пример

В playlists.txt можно указывать как и прямую ссылку на плейлист, так и на конкретное видео из плейлиста, плейлист подтянется сам.

Естественно это не работает, если плейлист с ограничением доступа по пользователям.
У меня всё. Набросы для улучшения функционала приветствуются, так как я этим занимался ночью неск мин и в рабочий перерыв.
