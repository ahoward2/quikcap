import platform


def get_os():
    os_name = platform.system().lower()
    if os_name == 'windows':
        return 'windows'
    # No support
    # elif os_name == 'linux':
    #     return 'linux'
    # elif os_name == 'darwin':
    #     return 'macos'
    else:
        raise ValueError(f"Unsupported operating system: {os_name}")


if __name__ == "__main__":
    os = get_os()
    print(f"Detected OS: {os}")
