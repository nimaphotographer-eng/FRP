# Huawei FRP Assistant 1.3

Windows 10/11 diagnostic application for Huawei devices, including EMUI 9.1.

## Safety scope

This project is intentionally limited to legitimate device diagnostics and official
account-recovery guidance. It does **not** bypass, remove, reset, patch, or disable
Factory Reset Protection (FRP), Google authentication, Huawei ID authentication, or
bootloader security.

## Features

- Huawei/Android ADB and Fastboot detection
- Model, manufacturer, Android and EMUI/build identification when ADB permits it
- Windows USB-driver diagnostics
- Huawei model database
- Diagnostic history
- TXT report export
- Official recovery guidance
- Automated GitHub Actions Windows build
- Automatic download of Android Platform Tools during CI

## Local development

Python is not required on the user's PC if GitHub Actions is used.

For local development with Python:

```bat
python -m pip install -r requirements.txt
python app.py
```

## GitHub Actions

1. Create an empty GitHub repository.
2. Upload the complete project.
3. Open **Actions** and run **Build Windows EXE**.
4. Download the `Huawei-FRP-Assistant-Windows` artifact.
5. The artifact contains `HuaweiFRPAssistant.exe`.

The workflow downloads the official Android Platform Tools archive at build time and
places `platform-tools` beside the application executable.

## Usage

Connect the phone with an appropriate USB cable and use the Diagnostics tab.
ADB information is only available when the device exposes an authorized ADB interface.
Fastboot information is available when the phone is actually in fastboot mode.

For an FRP prompt after a reset, use the Google account previously synchronized with
the phone and Google's official account-recovery process. This application does not
accept or store passwords.
