from pytube import YouTube
import os
import config
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

def download_video(url: str) -> str:
    yt = YouTube(url)
    stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    
    if not os.path.exists(config.DOWNLOAD_PATH):
        os.makedirs(config.DOWNLOAD_PATH)
    
    output_path = stream.download(output_path=config.DOWNLOAD_PATH)
    logger.info(f"Video downloaded to: {output_path}")
    return output_path


if __name__ == "__main__":
    test_url = "https://www.youtube.com/watch?v=hf6wIcz-gB8"
    downloaded_file = download_video(test_url)
    logger.info(f"Video downloaded to: {downloaded_file}")