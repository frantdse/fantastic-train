import re
import requests

# URL donde el proveedor inyecta el token fresco
SOURCE_URL = "https://www.desdepylabs.com/External/tvaccion/gentv"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def extract_and_generate():
    try:
        response = requests.get(SOURCE_URL, headers=headers, timeout=10)
        html = response.text

        # Buscar los enlaces m3u8 con el token (k=... & exp=...)
        matches = re.findall(r"(https://[^\s'\"`]+\.m3u8\?k=[^\s'\"`]+)", html)

        if not matches:
            print("No se encontraron enlaces dinámicos, usando respaldo...")
            stream_url = "https://sesion.desdeparaguay.net/hls/playlist.m3u8"
        else:
            # Tomar el primer enlace encontrado (usualmente 1080p o 720p)
            stream_url = matches[0]

        # Formato Estándar de Lista IPTV (M3U)
        playlist_content = f"""#EXTM3U
#EXTINF:-1 tvg-id="GEN" tvg-name="GEN TV" tvg-logo="https://www.gen.com.py/favicon.ico", GEN TV (En Vivo)
{stream_url}
"""

        with open("playlist.m3u8", "w", encoding="utf-8") as f:
            f.write(playlist_content)
        
        print(f"Éxito: Se actualizó playlist.m3u8 con {stream_url}")

    except Exception as e:
        print(f"Error al extraer token: {e}")

if __name__ == "__main__":
    extract_and_generate()
