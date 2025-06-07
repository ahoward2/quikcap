; QuikCap Installer Script

[Setup]
AppName=QuikCap
AppVersion=1.0
DefaultDirName={pf}\QuikCap
DefaultGroupName=QuikCap
OutputBaseFilename=QuikCapInstaller
Compression=lzma
SolidCompression=yes
SetupIconFile=assets\favicon.ico
UninstallDisplayIcon={app}\main.exe
Uninstallable=yes
RestartIfNeededByRun=false
DisableDirPage=no
DisableProgramGroupPage=no
AllowNoIcons=no

[Files]
Source: "dist\main.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\QuikCap"; Filename: "{app}\main.exe"
Name: "{commondesktop}\QuikCap"; Filename: "{app}\main.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"; Flags: unchecked

[Run]
Filename: "{app}\main.exe"; Description: "Launch QuikCap"; Flags: nowait postinstall skipifsilent
