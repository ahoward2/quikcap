![quikcap logo](./assets/logo.png)

<!-- vscode-markdown-toc -->

- 1. [Local Development](#LocalDevelopment)
  - 1.1. [Global Dependencies](#GlobalDependencies)
  - 1.2. [Repository Setup](#RepositorySetup)
  - 1.3. [Running the app](#Runningtheapp)
  - 1.4. [Build](#Build)
    - 1.4.1. [Building the app .exe](#Buildingtheapp.exe)
    - 1.4.2. [Building Inno Installer Executable (Windows only)](#BuildingInnoInstallerExecutableWindowsonly)
- 2. [ SDLC](#SDLC)

<!-- vscode-markdown-toc-config
	numbering=true
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->

# QuikCap

A light-weight camera dumping application.

## 1. <a name='LocalDevelopment'></a>Local Development

### 1.1. <a name='GlobalDependencies'></a>Global Dependencies

**UV**

```bash
pip install uv
```

**PyInstaller**

```bash
pip install -U pyinstaller
```

**Inno Setup Compiler (Windows Development Only)**

- Install from https://jrsoftware.org/isdl.php

### 1.2. <a name='RepositorySetup'></a>Repository Setup

1. Create virtual environment with `uv`.

```bash
uv venv quikcap
```

2. Activate virtual environment.

**Mac / Linux**

```bash
source .venv/bin/activate
```

**Windows**

```bash
## git-bash
source .venv\Scripts\activate
```

3. Install project dependencies.

```bash
uv sync
```

### 1.3. <a name='Runningtheapp'></a>Running the app

Recommended to run the application with a debugger.

**VSCode**

1. Run the debugger with `f5` key or in VSC UI.

### 1.4. <a name='Build'></a>Build

#### 1.4.1. <a name='Buildingtheapp.exe'></a>Building the app .exe

**Mac / Linux**

```bash
chmod +x build.sh
./build.sh
```

**Windows**

```bash
./build.bat
```

#### 1.4.2. <a name='BuildingInnoInstallerExecutableWindowsonly'></a>Building Inno Installer Executable (Windows only)

1. Open the Inno Compiler Application.
2. Select `setup.iss` and execute script.

## 2. <a name='SDLC'></a> SDLC

1. Make application changes.
2. Tag version for release -> [Create Tags](./.github/workflows/create_tags.yml).
3. Build and publish version -> [Build and Publish](./.github/workflows/build_and_publish.yml).

- PyInstaller -> (app.exe)
- Inno Setup -> (installer.exe)
- Artifact Upload (upload installer)

4. [Landing Page](https://ahoward2.github.io/quikcap/) download button already configured to fetch lastest available version.
