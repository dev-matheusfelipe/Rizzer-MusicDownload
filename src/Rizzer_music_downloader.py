import os
import sys
import threading
import webbrowser
import winreg
from tkinter import filedialog, messagebox

import customtkinter as ctk
from PIL import Image
from yt_dlp import YoutubeDL

# =========================
# METADADOS DO APP
# =========================
APP_NAME = "Rizzer Music Download"
APP_VERSION = "Versão: 1.1"
APP_AUTHOR = "Rizzer Studio"
APP_ICON = "Rizzer_MusicDownload.ico"
APP_LOGO = "Rizzer_MusicDownload.png"

# =========================
# DOCUMENTS (COM / SEM ONEDRIVE)
# =========================
def get_documents_folder():
    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
        ) as key:
            path, _ = winreg.QueryValueEx(key, "Personal")
            return os.path.expandvars(path)
    except Exception:
        return os.path.join(os.path.expanduser("~"), "Documents")


DOCUMENTS_DIR = get_documents_folder()

DEFAULT_DESTINO = os.path.join(
    DOCUMENTS_DIR,
    "Euro Truck Simulator 2",
    "music"
)

os.makedirs(DEFAULT_DESTINO, exist_ok=True)

# =========================
# BASE DIR (SCRIPT / EXE)
# =========================
if getattr(sys, "frozen", False):
    BASE_DIR = sys._MEIPASS
    PROJECT_DIR = BASE_DIR
    ASSETS_DIR = os.path.join(BASE_DIR, "assets")
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
    ASSETS_DIR = os.path.join(PROJECT_DIR, "assets")

# =========================
# FFMPEG (PORTABLE)
# =========================
FFMPEG_DIR = os.path.join(PROJECT_DIR, "ffmpeg", "bin")

# =========================
# UI CONFIG
# =========================
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

APP_BG = "#0B0F14"
CARD_BG = "#121A26"
CARD_BG_ALT = "#0F1622"
CARD_BORDER = "#1B2838"
TEXT_MUTED = "#8B98AA"
TEXT_ACCENT = "#8CB4FF"
TEXT_TITLE = "#E6EDF6"
ACCENT = "#4DA3FF"
ACCENT_SOFT = "#16263D"
SUCCESS = "#34D399"
WARNING = "#FBBF24"

# =========================
# DOWNLOAD
# =========================
def baixar():
    url = entry_url.get().strip()
    destino = entry_destino.get().strip()
    formato = option_format.get()

    if not url:
        status_label.configure(text="Erro: informe o link do YouTube", text_color="red")
        return

    if not destino:
        status_label.configure(text="Erro: informe a pasta de destino", text_color="red")
        return

    if not os.path.exists(os.path.join(FFMPEG_DIR, "ffmpeg.exe")):
        messagebox.showerror(
            "FFmpeg não encontrado",
            f"FFmpeg não localizado em:\n\n{FFMPEG_DIR}"
        )
        return

    os.makedirs(destino, exist_ok=True)

    btn_start.configure(state="disabled")
    status_label.configure(text="Baixando...", text_color=WARNING)

    def task():
        try:
            if formato == "MP3 (Música)":
                ydl_opts = {
                    "format": "bestaudio/best",
                    "outtmpl": os.path.join(destino, "%(title)s.%(ext)s"),
                    "ffmpeg_location": FFMPEG_DIR,
                    "postprocessors": [{
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }],
                    "quiet": True,
                }
            else:
                ydl_opts = {
                    "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
                    "outtmpl": os.path.join(destino, "%(title)s.%(ext)s"),
                    "merge_output_format": "mp4",
                    "ffmpeg_location": FFMPEG_DIR,
                    "quiet": True,
                }

            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            status_label.configure(
                text="Download concluído com sucesso!",
                text_color=SUCCESS
            )

        except Exception as e:
            status_label.configure(text="Erro ao baixar", text_color="red")
            messagebox.showerror("Erro", str(e))

        finally:
            btn_start.configure(state="normal")

    threading.Thread(target=task).start()


def escolher_pasta():
    pasta = filedialog.askdirectory()
    if pasta:
        entry_destino.delete(0, "end")
        entry_destino.insert(0, pasta)


def abrir_linkedin():
    webbrowser.open_new_tab("https://www.linkedin.com/in/dev-matheusfelipe")


def abrir_github():
    webbrowser.open_new_tab("https://github.com/dev-matheusfelipe")


def load_logo_image(max_size):
    logo_path = os.path.join(ASSETS_DIR, APP_LOGO)
    if not os.path.exists(logo_path):
        return None
    try:
        img = Image.open(logo_path)
        img.thumbnail((max_size, max_size), Image.LANCZOS)
        return ctk.CTkImage(img, size=img.size)
    except Exception:
        return None


# =========================
# INTERFACE
# =========================
app = ctk.CTk()
app.title(f"{APP_NAME}")

# ÍCONE
icon_path = os.path.join(ASSETS_DIR, APP_ICON)
if os.path.exists(icon_path):
    try:
        app.iconbitmap(icon_path)
    except Exception:
        pass

app.geometry("920x700")
app.resizable(False, False)
app.configure(fg_color=APP_BG)

main_frame = ctk.CTkFrame(app, fg_color="transparent")
main_frame.pack(expand=True, fill="both", padx=20, pady=20)

# ===== HEADER =====
header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
header_frame.pack(fill="x", padx=10, pady=(10, 20))
header_frame.grid_columnconfigure(0, weight=1, uniform="header")
header_frame.grid_columnconfigure(1, weight=4, uniform="header")

logo_img = load_logo_image(128)
logo_label = ctk.CTkLabel(
    header_frame,
    text="",
    image=logo_img,
    font=ctk.CTkFont(size=34, weight="bold"),
    text_color=TEXT_TITLE
)
logo_label.grid(row=0, column=0, sticky="w", padx=(6, 14), pady=6)

info_card = ctk.CTkFrame(
    header_frame,
    height=160,
    corner_radius=20,
    border_width=1,
    border_color=CARD_BORDER,
    fg_color=CARD_BG
)
info_card.grid(row=0, column=1, sticky="nsew", padx=(14, 0))
info_card.grid_propagate(False)

accent_bar = ctk.CTkFrame(info_card, height=3, fg_color=ACCENT, corner_radius=10)
accent_bar.pack(fill="x", padx=18, pady=(14, 10))

title = ctk.CTkLabel(
    info_card,
    text=APP_NAME,
    font=ctk.CTkFont(size=22, weight="bold"),
    text_color=TEXT_TITLE
)
title.pack(anchor="w", padx=18, pady=(0, 6))

desc = ctk.CTkLabel(
    info_card,
    text="Ferramenta elegante para organizar downloads de áudio e vídeo.",
    font=ctk.CTkFont(size=12),
    text_color=TEXT_MUTED
)
desc.pack(anchor="w", padx=18, pady=(0, 16))

# ===== CONTEÚDO =====
content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
content_frame.pack(fill="both", expand=True, padx=10)
content_frame.grid_columnconfigure(0, weight=1)

download_card = ctk.CTkFrame(
    content_frame,
    corner_radius=20,
    border_width=1,
    border_color=CARD_BORDER,
    fg_color=CARD_BG
)
download_card.grid(row=0, column=0, sticky="nsew", padx=0, pady=(0, 18))

download_title = ctk.CTkLabel(
    download_card,
    text="Download",
    font=ctk.CTkFont(size=16, weight="bold"),
    text_color=TEXT_TITLE
)
download_title.pack(anchor="w", padx=18, pady=(16, 6))

download_hint = ctk.CTkLabel(
    download_card,
    text="Cole o link e escolha o formato desejado.",
    font=ctk.CTkFont(size=12),
    text_color=TEXT_MUTED
)
download_hint.pack(anchor="w", padx=18, pady=(0, 10))

entry_url = ctk.CTkEntry(
    download_card,
    placeholder_text="Cole aqui o link do YouTube"
)
entry_url.pack(fill="x", padx=18, pady=(0, 8))

status_label = ctk.CTkLabel(
    download_card,
    text="Aguardando link...",
    font=ctk.CTkFont(size=12),
    text_color=TEXT_MUTED
)
status_label.pack(anchor="w", padx=18, pady=(0, 12))

actions_row = ctk.CTkFrame(download_card, fg_color="transparent")
actions_row.pack(fill="x", padx=18, pady=(0, 18))
actions_row.grid_columnconfigure(0, weight=1)
actions_row.grid_columnconfigure(1, weight=0)

option_format = ctk.CTkOptionMenu(
    actions_row,
    values=["MP3 (Música)", "MP4 (Vídeo)"]
)
option_format.set("MP3 (Música)")
option_format.grid(row=0, column=0, sticky="ew", padx=(0, 10))

btn_start = ctk.CTkButton(
    actions_row,
    text="Iniciar Download",
    fg_color=ACCENT,
    hover_color="#2F7DDE",
    text_color="#0B0F14",
    command=baixar,
    width=170
)
btn_start.grid(row=0, column=1, sticky="e")

destino_card = ctk.CTkFrame(
    content_frame,
    corner_radius=20,
    border_width=1,
    border_color=CARD_BORDER,
    fg_color=CARD_BG
)
destino_card.grid(row=1, column=0, sticky="nsew", padx=0, pady=(0, 18))

destino_title = ctk.CTkLabel(
    destino_card,
    text="Destino",
    font=ctk.CTkFont(size=16, weight="bold"),
    text_color=TEXT_TITLE
)
destino_title.pack(anchor="w", padx=18, pady=(16, 6))

destino_hint = ctk.CTkLabel(
    destino_card,
    text="Escolha a pasta onde os arquivos serão salvos.",
    font=ctk.CTkFont(size=12),
    text_color=TEXT_MUTED
)
destino_hint.pack(anchor="w", padx=18, pady=(0, 10))

entry_destino = ctk.CTkEntry(destino_card)
entry_destino.pack(fill="x", padx=18, pady=(0, 10))
entry_destino.insert(0, DEFAULT_DESTINO)

btn_browse = ctk.CTkButton(
    destino_card,
    text="Selecionar pasta",
    width=160,
    fg_color=CARD_BG_ALT,
    hover_color="#18263A",
    text_color=TEXT_TITLE,
    border_width=1,
    border_color=CARD_BORDER,
    command=escolher_pasta
)
btn_browse.pack(anchor="w", padx=18, pady=(0, 18))

# RODAPÉ
footer_card = ctk.CTkFrame(
    main_frame,
    corner_radius=20,
    border_width=1,
    border_color=CARD_BORDER,
    fg_color=CARD_BG_ALT
)
footer_card.pack(fill="x", padx=10, pady=(6, 4))
footer_card.grid_columnconfigure(0, weight=1)
footer_card.grid_columnconfigure(1, weight=1)

footer_left = ctk.CTkFrame(footer_card, fg_color="transparent")
footer_left.grid(row=0, column=0, sticky="w", padx=18, pady=14)

footer_title = ctk.CTkLabel(
    footer_left,
    text="Rizzer Studio © 2026",
    font=ctk.CTkFont(size=12, weight="bold"),
    text_color=TEXT_TITLE
)
footer_title.pack(anchor="w")

footer_right = ctk.CTkFrame(footer_card, fg_color="transparent")
footer_right.grid(row=0, column=1, sticky="e", padx=18, pady=14)

footer_btns = [
    "GitHub",
    "LinkedIn"
]

for label in footer_btns:
    ctk.CTkButton(
        footer_right,
        text=label,
        width=90,
        height=26,
        fg_color=CARD_BG,
        hover_color="#1A2231",
        text_color=TEXT_TITLE,
        corner_radius=14,
        command=abrir_github if label == "GitHub" else abrir_linkedin
    ).pack(side="left", padx=4)

version_badge = ctk.CTkLabel(
    footer_right,
    text=APP_VERSION,
    font=ctk.CTkFont(size=11, weight="bold"),
    text_color=TEXT_MUTED,
    fg_color=CARD_BG,
    corner_radius=12,
    padx=10,
    pady=2
)
version_badge.pack(side="left", padx=(6, 0))

app.mainloop()
