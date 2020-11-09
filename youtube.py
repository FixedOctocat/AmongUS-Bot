from youtubesearchpython import SearchVideos
import youtube_dl
import re

regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

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
    if re.match(regex, url) is not None:
        while True:
            try:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(url, download=True)
                    video_title = info_dict.get('title', None)
                return video_title
            except Exception as e:
                print(e)
    else:
        raise TypeError("This is not correct url")


def music_title(url):
    if re.match(regex, url) is not None:
        while True:
            try:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(url, download=False)
                    video_title = info_dict.get('title', None)
                return video_title
            except Exception as e:
                print(e)
    else:
        raise TypeError("This is not correct url")


def music_duration(url):
    if re.match(regex, url) is not None:
        while True:
            try:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(url, download=False)
                    video_duration = info_dict.get('duration', None)
                return video_duration
            except Exception as e:
                print(e)
    else:
        raise TypeError("This is not correct url")


if __name__ == '__main__':
    url1 = "https://www.youtube.com/watch?v=9fN7udMAMog"
    url2 = "www.youtube.com/watch?v=Suu9I9TNdnE"
    url3 = "https://www.youtube.com/watch?v=S8KqHUQUOKI&ab_channel=iMiles"
    a = music_duration("https://www.youtube.com/watch?v=sA6NDPKVg6g")
    print(a)
