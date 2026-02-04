# Rizzer Music Download

Ferramenta elegante para organizar downloads de áudio e vídeo do YouTube.

## Recursos
- Download em MP3 ou MP4
- Seleção de pasta de destino
- Interface moderna (CustomTkinter)
- Instalador para Windows (Inno Setup)

## Estrutura
- `src/` código-fonte
- `assets/` ícones e imagens do app
- `installer/` script do instalador
- `build/` e `dist/` gerados localmente (ignorados)

## Requisitos
- Python 3.13+
- `pip install -r requirements.txt` (se você tiver um requirements)

## Rodar localmente
```powershell
python src\Rizzer_music_downloader.py
```

## Build do executável (PyInstaller)
```powershell
pyinstaller -y Rizzer_music_downloader.spec
```

## Criar instalador (Inno Setup)
```powershell
& "C:\Users\matheus\AppData\Local\Programs\Inno Setup 6\ISCC.exe" "installer\Rizzer_music_downloader.iss"
```

O instalador gerado fica em `dist\RizzerMusicDownloadSetup.exe`.

## Links
- GitHub: https://github.com/dev-matheusfelipe/Rizzer-MusicDownload
