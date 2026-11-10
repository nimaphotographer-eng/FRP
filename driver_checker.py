
import os, subprocess, shutil

class DriverChecker:
    def check(self):
        result = {"platform": os.name, "adb_in_path": bool(shutil.which("adb")),
                  "fastboot_in_path": bool(shutil.which("fastboot"))}
        if os.name == "nt":
            try:
                p = subprocess.run(["pnputil", "/enum-drivers"], capture_output=True, text=True,
                                   timeout=15, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
                text = (p.stdout or "").lower()
                result["pnputil_available"] = p.returncode == 0
                result["android_usb_driver_detected"] = ("android" in text or "huawei" in text)
            except Exception as e:
                result["pnputil_error"] = str(e)
        return result
