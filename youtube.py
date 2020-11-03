from youtubesearchpython import SearchVideos
import youtube_dl

ydl_opts = {
    'quiet': True,
    'prefer_insecure': False,
    'no_warnings': True,
    'format': 'bestaudio/best',
    'noplaylist': 'True',
    'outtmpl': 'song.mp3',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}


def search(arg):
    res = SearchVideos(arg, offset=1, mode="list", max_results=5)
    return res.result()


def download(url):
    while True:
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True )
                video_title = info_dict.get('title', None)
            return video_title
        except Exception as e:
            print(e)


if __name__ == '__main__':
    url1 = "https://www.youtube.com/watch?v=9fN7udMAMog"
    url2 = "www.youtube.com/watch?v=Suu9I9TNdnE"
    a = download(url1)
    print(a)
