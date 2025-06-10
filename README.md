![quikcap logo](./assets/logo.png)

# QuikCap

A light-weight camera dumping application.

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
## git-bash
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
