import yt_dlp
import pandas as pd
import datetime
import config


def get_playlist_metadata(playlist_url, cookies_file="cookies.txt"):
    # Opções para capturar playlist completa (com cookies)
    ydl_opts = {
        "quiet": True,
        "extract_flat": True,   # captura apenas metadados básicos da playlist
        "cookiefile": cookies_file
    }

    video_ids = []
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(playlist_url, download=False)
        if not info:
            raise ValueError("❌ Não foi possível obter informações da playlist. Verifique se o link e os cookies estão corretos.")
        if "entries" not in info:
            raise ValueError("❌ Nenhum vídeo encontrado na playlist. Pode ser privada ou os cookies estão inválidos.")

        video_ids = [entry.get("id") for entry in info["entries"] if entry and entry.get("id")]

    # Agora baixa os metadados individuais
    videos_data = []
    with yt_dlp.YoutubeDL({"quiet": True, "cookiefile": cookies_file}) as ydl:
        for vid in video_ids:
            url = f"https://www.youtube.com/watch?v={vid}"
            try:
                video = ydl.extract_info(url, download=False)
                if not video:
                    print(f"⚠️ Não foi possível extrair {url}")
                    continue

                video_info = {
                    "Titulo": video.get("title"),
                    "URL": url,
                    "Data_Postagem": video.get("upload_date"),
                    "Duracao": str(datetime.timedelta(seconds=video.get("duration"))) if video.get("duration") else None,
                    "Canal": video.get("uploader"),
                    "Views": video.get("view_count"),
                }
                videos_data.append(video_info)
            except Exception as e:
                print(f"⚠️ Erro ao processar {url}: {e}")

    return videos_data


if __name__ == "__main__":
    playlist_url = "https://www.youtube.com/playlist?list=PL..."  # coloque aqui sua playlist não listada
    dados = get_playlist_metadata(playlist_url, cookies_file=config.COOKIE_FILE)

    df = pd.DataFrame(dados)
    if "Data_Postagem" in df.columns:
        df["Data_Postagem"] = pd.to_datetime(df["Data_Postagem"], errors="coerce").dt.strftime("%Y-%m-%d")

    df.to_csv("playlist_metadados.csv", index=False, encoding="utf-8-sig")
    print("✅ CSV gerado com sucesso!")
