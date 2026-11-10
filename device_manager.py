
import os, shutil, subprocess, re
from pathlib import Path

class DeviceManager:
    def __init__(self):
        self.base = Path(__file__).parent
        self.pt = self.base / "platform-tools"
        self.adb = self.pt / ("adb.exe" if os.name == "nt" else "adb")
        self.fastboot = self.pt / ("fastboot.exe" if os.name == "nt" else "fastboot")

    def _run(self, exe, args, timeout=8):
        if not exe.exists():
            return {"ok": False, "error": f"Missing tool: {exe}"}
        try:
            p = subprocess.run([str(exe), *args], capture_output=True, text=True,
                               timeout=timeout, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
            return {"ok": p.returncode == 0, "returncode": p.returncode,
                    "stdout": p.stdout.strip(), "stderr": p.stderr.strip()}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def adb_devices(self):
        r = self._run(self.adb, ["devices", "-l"])
        return {"transport": "adb", **r}

    def fastboot_devices(self):
        r = self._run(self.fastboot, ["devices"])
        return {"transport": "fastboot", **r}

    def shell_getprop(self, prop):
        return self._run(self.adb, ["shell", "getprop", prop])

    def detect(self):
        result = {"adb": self.adb_devices(), "fastboot": self.fastboot_devices()}
        adb = result["adb"]
        if adb.get("ok") and adb.get("stdout"):
            serials = []
            for line in adb["stdout"].splitlines():
                if line.startswith("List of devices"): continue
                m = re.match(r"(\S+)\s+(\S+)", line)
                if m and m.group(2) == "device":
                    serials.append(m.group(1))
            if serials:
                result["device"] = {
                    "serial": serials[0],
                    "model": self.shell_getprop("ro.product.model").get("stdout",""),
                    "manufacturer": self.shell_getprop("ro.product.manufacturer").get("stdout",""),
                    "android": self.shell_getprop("ro.build.version.release").get("stdout",""),
                    "emui": self.shell_getprop("ro.build.version.emui").get("stdout",""),
                    "build": self.shell_getprop("ro.build.display.id").get("stdout",""),
                }
        return result
