import yt_dlp
import os
import config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_video(url: str) -> str:
    """
    Downloads a video from the given URL using yt-dlp.

    Args:
        url (str): The URL of the video to download.

    Returns:
        str: The filename of the downloaded video.
    """
    if not os.path.exists(config.DOWNLOAD_PATH):
        os.makedirs(config.DOWNLOAD_PATH)

    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(config.DOWNLOAD_PATH, '%(title)s.%(ext)s'),
        'noplaylist': False,
        'dateafter': '20250921'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        filename = ydl.prepare_filename(info)
        logger.info(f"Iniciando o download do vídeo: {info['title']}")
        ydl.download([url])
        logger.info(f"Download concluído: {info['title']}")
        return filename

if __name__ == "__main__":
    test_url = "https://www.youtube.com/playlist?list=PLmrMBkPdETfiGBIN_uZ5hKPrh7P6E3Y_x"
    download_video(test_url)
