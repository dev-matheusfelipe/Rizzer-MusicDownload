[Setup]
AppId={{7A9F45D8-5F2B-4D83-9D70-1C3C9E6B0D1F}
AppName=Rizzer Music Download
AppVersion=1.2
AppPublisher=Rizzer Studio
DefaultDirName={autopf}\Rizzer Music Download
DefaultGroupName=Rizzer Music Download
DisableProgramGroupPage=yes
OutputDir=..\dist
OutputBaseFilename=RizzerMusicDownloadSetup
Compression=lzma
SolidCompression=yes
SetupIconFile=..\assets\Rizzer_MusicDownload.ico
UninstallDisplayIcon={app}\Rizzer_music_downloader.exe
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"; Flags: unchecked

[Files]
Source: "..\dist\Rizzer_music_downloader\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs ignoreversion

[Icons]
Name: "{group}\Rizzer Music Download"; Filename: "{app}\Rizzer_music_downloader.exe"; IconFilename: "{app}\Rizzer_music_downloader.exe"
Name: "{commondesktop}\Rizzer Music Download"; Filename: "{app}\Rizzer_music_downloader.exe"; IconFilename: "{app}\Rizzer_music_downloader.exe"; Tasks: desktopicon
