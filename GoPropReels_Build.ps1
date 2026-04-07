$ROOT = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ROOT

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  GoPropReels.com -- Build Tool" -ForegroundColor Cyan
Write-Host "  Astro · TypeScript · Vercel" -ForegroundColor Gray
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  1. BUILD ONLY" -ForegroundColor White
Write-Host "  2. BUILD AND PREVIEW (localhost:4321)" -ForegroundColor White
Write-Host ""
$choice = Read-Host "Chon (1/2)"

$conflict = Get-ChildItem $ROOT -Filter "*conflicted*" -Recurse -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -notmatch "\node_modules\\" -and $_.FullName -notmatch "\.git\\" } |
    Select-Object -First 1
if ($conflict) {
    Write-Host "[WARN] Dropbox conflict: $($conflict.FullName)" -ForegroundColor Red
    Read-Host "Press Enter to continue anyway, or Ctrl+C to abort"
}

Write-Host ""
Write-Host "[BUILD] npm run build..." -ForegroundColor Cyan
npm run build
if ($LASTEXITCODE -ne 0) {
    Write-Host "[FAIL] Build failed." -ForegroundColor Red
    Read-Host "Press Enter to close"
    exit 1
}
Write-Host "[OK] Build success!" -ForegroundColor Green

if ($choice -eq "2") {
    Write-Host ""
    Write-Host "[PREVIEW] Starting on http://localhost:4321 ..." -ForegroundColor Cyan
    Start-Process "http://localhost:4321"
    npm run preview
}

Write-Host ""
Read-Host "Press Enter to close"
