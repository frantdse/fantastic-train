import re
import requests

SOURCE_URL = "https://www.desdepylabs.com/External/tvaccion/gentv"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def extract_and_generate():
    stream_url = "https://sesion.desdeparaguay.net/hls/playlist.m3u8"
    try:
        response = requests.get(SOURCE_URL, headers=headers, timeout=10)
        if response.status_code == 200:
            matches = re.findall(r"(https://[^\s'\"`]+\.m3u8\?k=[^\s'\"`]+)", response.text)
            if matches:
                stream_url = matches[0]
    except Exception as e:
        print(f"Aviso: Ocurrió un fallo al consultar origen ({e}). Usando URL de respaldo.")

    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="refresh" content="0; url={stream_url}" />
    <script>window.location.href = "{stream_url}";</script>
</head>
<body>
    <p>Redirigiendo a la señal... Si no carga, <a href="{stream_url}">haz clic aquí</a>.</p>
</body>
</html>"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"Proceso finalizado con URL: {stream_url}")

if __name__ == "__main__":
    extract_and_generate()
