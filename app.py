
import sys
from PySide6.QtWidgets import QApplication
from device_manager import DeviceManager
from diagnostics import DiagnosticsEngine
from database_manager import DeviceDatabase
from history_manager import HistoryManager
from report_manager import ReportManager
from driver_checker import DriverChecker
from pathlib import Path
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, QTabWidget, QFileDialog, QMessageBox

APP_TITLE = "Huawei FRP Assistant 1.3"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_TITLE)
        self.resize(1050, 720)
        self.dm = DeviceManager()
        self.diag = DiagnosticsEngine(self.dm)
        self.db = DeviceDatabase(Path(__file__).with_name("device_database.json"))
        self.history = HistoryManager(Path.home() / "HuaweiFRPAssistant" / "history.json")
        self.report = ReportManager(Path.home() / "HuaweiFRPAssistant" / "reports")
        self.drivers = DriverChecker()
        self.build_ui()

    def build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        title = QLabel("Huawei FRP Assistant 1.3")
        title.setObjectName("title")
        layout.addWidget(title)

        tabs = QTabWidget()
        layout.addWidget(tabs)

        # Device tab
        device_tab = QWidget()
        dl = QVBoxLayout(device_tab)
        buttons = QHBoxLayout()
        for text, fn in [
            ("Detect Device", self.detect),
            ("ADB Devices", self.adb),
            ("Fastboot Devices", self.fastboot),
            ("Driver Check", self.driver_check),
        ]:
            b = QPushButton(text); b.clicked.connect(fn); buttons.addWidget(b)
        dl.addLayout(buttons)
        self.output = QTextEdit(); self.output.setReadOnly(True)
        dl.addWidget(self.output)
        tabs.addTab(device_tab, "Diagnostics")

        # Recovery guidance
        recovery = QWidget(); rl = QVBoxLayout(recovery)
        rl.addWidget(QLabel("Official account recovery / device ownership guidance"))
        guide = QTextEdit()
        guide.setReadOnly(True)
        guide.setPlainText(
            "This application does not bypass or remove FRP authentication.\n\n"
            "If a reset device asks for the previously synchronized Google account, "
            "complete Google's official account recovery process and sign in with the "
            "account previously associated with the device.\n\n"
            "For Huawei account issues, use Huawei's official support/account recovery "
            "channels. Keep proof of purchase available if service support requests it.\n\n"
            "Do not enter passwords or recovery codes into this application."
        )
        rl.addWidget(guide)
        tabs.addTab(recovery, "Official Recovery")

        # History/report
        reports = QWidget(); pl = QVBoxLayout(reports)
        b1 = QPushButton("Export Current Diagnostic Report"); b1.clicked.connect(self.export_report)
        b2 = QPushButton("Open Report Folder"); b2.clicked.connect(self.open_report_folder)
        pl.addWidget(b1); pl.addWidget(b2)
        tabs.addTab(reports, "Reports")

    def write(self, text):
        self.output.append(text)
        QApplication.processEvents()

    def detect(self):
        result = self.diag.collect()
        self.write(json_dumps(result))
        self.history.add(result)

    def adb(self):
        result = self.dm.adb_devices()
        self.write(json_dumps(result))

    def fastboot(self):
        result = self.dm.fastboot_devices()
        self.write(json_dumps(result))

    def driver_check(self):
        self.write(json_dumps(self.drivers.check()))

    def export_report(self):
        result = self.diag.collect()
        path = self.report.export_txt(result)
        self.history.add(result)
        QMessageBox.information(self, "Report", f"Report saved to:\n{path}")

    def open_report_folder(self):
        import os
        os.startfile(str(self.report.root))

def json_dumps(value):
    import json
    return json.dumps(value, indent=2, ensure_ascii=False)

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QWidget { background:#1e1e1e; color:#eeeeee; font-size:14px; }
        QLineEdit, QTextEdit { background:#252526; border:1px solid #3f3f46; padding:7px; }
        QPushButton { background:#333333; border:1px solid #555555; padding:9px 14px; border-radius:4px; }
        QPushButton:hover { background:#444444; }
        QTabBar::tab { background:#2d2d30; padding:9px 18px; }
        QTabBar::tab:selected { background:#3e3e42; }
        QLabel#title { font-size:24px; font-weight:bold; padding:8px; }
    """)
    w = MainWindow(); w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
