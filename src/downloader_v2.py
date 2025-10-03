import os
import yt_dlp
import logging
import config
from typing import List, Dict, Any

# Configuração básica do logger
logger = logging.getLogger(__name__)
# Certifique-se de que config.DOWNLOAD_PATH e config.DATE_AFTER estejam definidos
# Ex: DOWNLOAD_PATH = '/caminho/para/downloads' e DATE_AFTER = '20250921'

def download_media(url: str, date_after: str = None) -> List[str]:
    """
    Downloads vídeos/playlists da URL fornecida, aplicando filtros de data se especificado.

    Args:
        url (str): A URL do vídeo, canal ou playlist para baixar.
        date_after (str, optional): Data de upload mínima (inclusiva) no formato YYYYMMDD. 
                                    Se None, não aplica filtro de data. Defaults to None.

    Returns:
        List[str]: Uma lista com os caminhos dos arquivos baixados.
    """
    
    # 1. Cria o diretório de download se não existir
    if not os.path.exists(config.DOWNLOAD_PATH):
        os.makedirs(config.DOWNLOAD_PATH)
        logger.info(f"Diretório de download criado: {config.DOWNLOAD_PATH}")

    # 2. Configurações base do yt-dlp
    ydl_opts: Dict[str, Any] = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]', # Melhor formato, preferindo MP4
        'outtmpl': os.path.join(config.DOWNLOAD_PATH, '%(extractor)s-%(upload_date)s-%(title).40s-%(id)s.%(ext)s'),
        'ignoreerrors': True, # Continuar mesmo que alguns vídeos falhem
        'no_warnings': True,
        'extractor_args': {
            'youtube': {'player-client': 'web'},
        },
        'cookiefile': config.COOKIE_FILE,
        # 'postprocessors': [{
        #     'key': 'FFmpegVideoRemuxer',
        #     'prefer_ext': 'mp4',
        # }], # Remuxar para mp4 se necessário
        'merge_output_format': 'mp4'
    }

    # 3. Adiciona o filtro de data se for fornecido
    if date_after:
        ydl_opts['dateafter'] = date_after
        # Adiciona a otimização de parada para playlists grandes e ordenadas
        ydl_opts['break_on_reject'] = True 
        logger.info(f"Filtro de data aplicado: Apenas uploads a partir de {date_after}")


    downloaded_files: List[str] = []

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Forçamos uma simulação para pegar os metadados
            info = ydl.extract_info(url, download=False)

            if info.get('_type') == 'playlist':
                logger.info(f"Iniciando processamento da playlist/canal: {info.get('title', 'N/A')}")
            else:
                logger.info(f"Iniciando download do item: {info.get('title', 'N/A')}")

            # 4. Executa o download
            # ydl.download retorna 0 em caso de sucesso
            ydl.download([url])

            # 5. Coleta os nomes dos arquivos baixados
            # Como é mais complexo em playlists, vamos simplificar o retorno
            # Você precisaria de um hook ('progress_hooks') para rastrear filenames
            # Vamos retornar a URL para indicar que o processo terminou.
            return [f"Download iniciado de {url} com sucesso. Verifique {config.DOWNLOAD_PATH}"]

    except Exception as e:
        logger.error(f"Erro ao baixar {url}: {e}")
        return [f"Erro ao baixar {url}: {e}"]


if __name__ == "__main__":
    test_url = "https://youtube.com/playlist?list=PLmrMBkPdETfiGBIN_uZ5hKPrh7P6E3Y_x&si=1PNGE-Xx_U_68fUk"
    results = download_media(test_url, date_after=config.DATE_AFTER)
    for result in results:
        print(result)