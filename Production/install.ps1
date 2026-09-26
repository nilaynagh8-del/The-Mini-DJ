# ============================================================
#  MIDI Keyboard - one-click installer (Windows)
#  Flashes CircuitPython, then copies the firmware files.
# ============================================================
$ErrorActionPreference = "Stop"

$fw = $PSScriptRoot
$uf2 = Join-Path $fw "firmware\adafruit-circuitpython-raspberry_pi_pico-en_US-10.3.1.uf2"
if (-not (Test-Path $uf2)) {
    Write-Host "Downloading CircuitPython 10.3.1 for Raspberry Pi Pico..."
    New-Item -ItemType Directory -Force -Path (Join-Path $fw "firmware") | Out-Null
    Invoke-WebRequest -Uri "https://downloads.circuitpython.org/bin/raspberry_pi_pico/en_US/adafruit-circuitpython-raspberry_pi_pico-en_US-10.3.1.uf2" -OutFile $uf2
}

Write-Host ""
Write-Host "============================================================" 
Write-Host " STEP 1: Put the Pico into bootloader mode"
Write-Host "============================================================"
Write-Host " 1. UNPLUG the USB cable from the keyboard"
Write-Host " 2. Hold the white BOOTSEL button on the Pico"
Write-Host " 3. Plug the USB cable back in (keep holding BOOTSEL)"
Write-Host " 4. Release BOOTSEL - a drive called 'RPI-RP2' appears"
Write-Host ""

$drive = $null
foreach ($i in 1..30) {
    $drive = Get-CimInstance Win32_LogicalDisk | Where-Object { $_.VolumeName -eq "RPI-RP2" } | Select-Object -First 1
    if ($drive) { break }
    Write-Host "   Waiting for RPI-RP2 drive... ($i/30)" -NoNewline
    Write-Host "`r" -NoNewline
    Start-Sleep -Seconds 1
}
if (-not $drive) {
    Write-Host ""
    Write-Host "ERROR: RPI-RP2 drive not found. Unplug, hold BOOTSEL, replug." -ForegroundColor Red
    exit 1
}
$bootDrive = "$($drive.DeviceID)\"
Write-Host ""
Write-Host " Found bootloader at $bootDrive" -ForegroundColor Green

Write-Host ""
Write-Host "Flashing CircuitPython (copying UF2)..."
Copy-Item $uf2 -Destination $bootDrive
Write-Host " Board will reboot. Waiting for CIRCUITPY drive..."

$cp = $null
foreach ($i in 1..45) {
    $cp = Get-CimInstance Win32_LogicalDisk | Where-Object { $_.VolumeName -eq "CIRCUITPY" } | Select-Object -First 1
    if ($cp) { break }
    Start-Sleep -Seconds 1
}
if (-not $cp) {
    Write-Host "ERROR: CIRCUITPY drive did not appear. Unplug/replug USB and re-run just the copy step." -ForegroundColor Red
    exit 1
}
$cpDrive = "$($cp.DeviceID)\"
Write-Host " Found CIRCUITPY at $cpDrive" -ForegroundColor Green

Write-Host ""
Write-Host "Copying firmware files..."
Copy-Item -Recurse -Force (Join-Path $fw "lib") $cpDrive
Copy-Item -Force (Join-Path $fw "code.py") $cpDrive
Copy-Item -Force (Join-Path $fw "boot.py") $cpDrive

Write-Host ""
Write-Host "============================================================" 
Write-Host " DONE! Your MIDI keyboard is ready." -ForegroundColor Green
Write-Host "============================================================"
Write-Host " - Plug it into any DAW and play."
Write-Host " - Serial console (REPL):  picocom / PuTTY / Mu / code.circuitpython.org"
Write-Host ""
