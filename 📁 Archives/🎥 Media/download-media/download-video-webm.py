import yt_dlp

url = input("Cole aqui sua URL: ")

try:
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        print(f"Titulo: {info['title']}")
        print(f"Thumbnail: {info['thumbnail']}")
    print("Download concluído!")
except Exception as e:
    print(f"Ocorreu um erro: {e}")

#The video will be downloaded at the page the script was exe. in .webm 