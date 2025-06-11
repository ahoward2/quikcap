![quikcap logo](./assets/logo.png)

**QuikCap**

Fast and simple camera footage transfer.
- [Download](#download)
  - [Supported platforms](#supported-platforms)
- [Local Development](#local-development)
  - [Global Dependencies](#global-dependencies)
  - [Repository Setup](#repository-setup)
  - [Running the app](#running-the-app)
  - [Build](#build)
    - [Building the app .exe](#building-the-app-exe)
    - [Building Inno Installer Executable (Windows only)](#building-inno-installer-executable-windows-only)
- [SDLC](#sdlc)

## Download

Download the [latest version](https://ahoward2.github.io/quikcap/).

### Supported platforms

- Windows ✅
- Mac 🔜
- Linux 🔜

## Local Development

### Global Dependencies

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

### Repository Setup

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
# git-bash
source .venv\Scripts\activate
```

3. Install project dependencies.

```bash
uv sync
```

### Running the app

Recommended to run the application with a debugger.

**VSCode**

1. Run the debugger with `f5` key or in VSC UI.

### Build

#### Building the app .exe

**Mac / Linux**

```bash
chmod +x build.sh
./build.sh
```

**Windows**

```bash
./build.bat
```

#### Building Inno Installer Executable (Windows only)

1. Open the Inno Compiler Application.
2. Select `setup.iss` and execute script.

## SDLC

1. Make application changes.
2. Tag version for release → [Create Tags](./.github/workflows/create_tags.yml).
3. Build and publish version → [Build and Publish](./.github/workflows/build_and_publish.yml).
   - PyInstaller → (app.exe)
   - Inno Setup → (installer.exe)
   - Artifact Upload (upload installer)
4. [Landing Page](https://ahoward2.github.io/quikcap/) download button already configured to fetch lastest available version.
