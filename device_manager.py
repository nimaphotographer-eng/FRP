import os
import subprocess
import sys
from pathlib import Path


class DeviceManager:
    def __init__(self):
        self.base_dir = self._get_base_dir()
        self.platform_tools = self.base_dir / "platform-tools"

        self.adb = self.platform_tools / (
            "adb.exe" if os.name == "nt" else "adb"
        )

        self.fastboot = self.platform_tools / (
            "fastboot.exe" if os.name == "nt" else "fastboot"
        )

    @staticmethod
    def _get_base_dir():
        """
        Returns the correct application resource directory.

        Normal Python execution:
            project directory

        PyInstaller --onefile execution:
            sys._MEIPASS
        """
        if getattr(sys, "frozen", False):
            meipass = getattr(sys, "_MEIPASS", None)

            if meipass:
                return Path(meipass)

        return Path(__file__).resolve().parent

    def _run(self, executable, arguments, timeout=20):
        executable = Path(executable)

        if not executable.exists():
            return {
                "ok": False,
                "error": f"Missing tool: {executable}"
            }

        try:
            process = subprocess.run(
                [str(executable), *arguments],
                capture_output=True,
                text=True,
                timeout=timeout,
                creationflags=(
                    subprocess.CREATE_NO_WINDOW
                    if os.name == "nt"
                    else 0
                )
            )

            return {
                "ok": process.returncode == 0,
                "returncode": process.returncode,
                "stdout": process.stdout.strip(),
                "stderr": process.stderr.strip()
            }

        except subprocess.TimeoutExpired:
            return {
                "ok": False,
                "error": f"Command timed out after {timeout} seconds."
            }

        except Exception as exc:
            return {
                "ok": False,
                "error": str(exc)
            }

    def adb_devices(self):
        return self._run(
            self.adb,
            ["devices", "-l"]
        )

    def fastboot_devices(self):
        return self._run(
            self.fastboot,
            ["devices"]
        )

    def get_properties(self):
        result = self._run(
            self.adb,
            ["shell", "getprop"]
        )

        if not result.get("ok"):
            return result

        properties = {}

        for line in result.get("stdout", "").splitlines():
            if "]: [" in line:
                try:
                    left, right = line.split("]: [", 1)

                    key = left.lstrip("[")
                    value = right.rstrip("]")

                    properties[key] = value

                except Exception:
                    continue

        wanted = [
            "ro.product.model",
            "ro.product.manufacturer",
            "ro.build.version.release",
            "ro.build.version.emui",
            "ro.build.display.id"
        ]

        return {
            "ok": True,
            "properties": {
                key: properties.get(key, "")
                for key in wanted
            }
        }

    def diagnostics(self):
        return {
            "adb": {
                "transport": "adb",
                **self.adb_devices()
            },

            "fastboot": {
                "transport": "fastboot",
                **self.fastboot_devices()
            },

            "paths": {
                "resource_root": str(self.base_dir),
                "platform_tools": str(self.platform_tools),
                "adb": str(self.adb),
                "fastboot": str(self.fastboot)
            }
        }
