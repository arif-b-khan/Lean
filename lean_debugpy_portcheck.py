#!/usr/bin/env python3
import socket
import sys

def check_port(host='127.0.0.1', port=5678, timeout=1.0):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        return s.connect_ex((host, port)) == 0

def debugpy_info():
    try:
        import debugpy
        return True, getattr(debugpy, "__file__", "<unknown>")
    except Exception as e:
        return False, str(e)

def main():
    installed, info = debugpy_info()
    print(f"debugpy installed: {installed} - {info}")
    if check_port():
        print("OK: debugpy (or some process) is listening on 127.0.0.1:5678")
        sys.exit(0)
    else:
        print("FAIL: no listener on 127.0.0.1:5678 (connection refused or timed out)")
        sys.exit(1)

if __name__ == '__main__':
    main()