$ROOT = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ROOT

Write-Host "" 
Write-Host "================================================" -ForegroundColor Yellow
Write-Host "  GoPropReels.com -- Deploy to Vercel" -ForegroundColor Yellow
Write-Host "  npm build -> git commit -> git push" -ForegroundColor Gray
Write-Host "================================================" -ForegroundColor Yellow
Write-Host ""

$conflict = Get-ChildItem $ROOT -Filter "*conflicted*" -Recurse -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -notmatch "\node_modules\\" -and $_.FullName -notmatch "\.git\\" } |
    Select-Object -First 1
if ($conflict) {
    Write-Host "[WARN] Dropbox conflict: $($conflict.FullName)" -ForegroundColor Red
    Read-Host "Press Enter to continue anyway, or Ctrl+C to abort"
}

Write-Host "[1/3] npm run build..." -ForegroundColor Cyan
npm run build
if ($LASTEXITCODE -ne 0) {
    Write-Host "[FAIL] Build failed -- deploy aborted." -ForegroundColor Red
    Read-Host "Press Enter to close"
    exit 1
}
Write-Host "[OK] Build success." -ForegroundColor Green

Write-Host ""
Write-Host "[2/3] git add + commit..." -ForegroundColor Cyan
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"
git add -A
git commit -m "deploy: $timestamp"
if ($LASTEXITCODE -ne 0) { Write-Host "  (nothing to commit -- continuing)" -ForegroundColor Gray }

Write-Host ""
Write-Host "[3/3] git push origin main..." -ForegroundColor Cyan
git push origin main
if ($LASTEXITCODE -ne 0) {
    Write-Host "[FAIL] git push failed." -ForegroundColor Red
    Read-Host "Press Enter to close"
    exit 1
}

Write-Host ""
Write-Host "[OK] Pushed! Vercel is deploying (~1-2 min)." -ForegroundColor Green
Write-Host "     https://vercel.com/dashboard" -ForegroundColor Gray
Write-Host ""
Read-Host "Press Enter to close"
