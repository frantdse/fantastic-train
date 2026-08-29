    import re
import requests

SOURCE_URL = "https://www.desdepylabs.com/External/tvaccion/gentv"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def extract_and_generate():
    try:
        response = requests.get(SOURCE_URL, headers=headers, timeout=10)
        html = response.text

        matches = re.findall(r"(https://[^\s'\"`]+\.m3u8\?k=[^\s'\"`]+)", html)

        if not matches:
            stream_url = "https://sesion.desdeparaguay.net/hls/playlist.m3u8"
        else:
            stream_url = matches[0]

        # Genera el HTML con redirección automática inmediata
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="refresh" content="0; url={stream_url}" />
    <script>window.location.href = "{stream_url}";</script>
</head>
<body>
    <p>Redirigiendo a la señal en vivo... Si no carga automáticamente, <a href="{stream_url}">haz clic aquí</a>.</p>
</body>
</html>"""

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"Éxito: Redirección guardada hacia {stream_url}")

    except Exception as e:
        print(f"Error al extraer token: {e}")

if __name__ == "__main__":
    extract_and_generate()
