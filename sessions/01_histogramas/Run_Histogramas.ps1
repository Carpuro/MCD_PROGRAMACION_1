# Configuration
$ImageName = "mcd_prog1:latest"
$CsvRel    = "data/categorias_de_corredores.csv"
$OutputRel = "output"

# Go to root directory
Set-Location $PSScriptRoot
$RepoRoot = (Resolve-Path "$PSScriptRoot\..\..").Path

# Build Docker image
Write-Host "Building Docker image: $ImageName" -ForegroundColor Cyan
Push-Location $RepoRoot
docker build -t $ImageName .
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Build failed." -ForegroundColor Red
    Pop-Location
    Read-Host "Press Enter to close"
    exit 1
}

# Run container
Write-Host "Running container..." -ForegroundColor Cyan
docker run --rm `
    -v "$RepoRoot\data:/app/data" `
    -v "$RepoRoot\output:/app/output" `
    $ImageName --csv "$CsvRel"
$ExitCode = $LASTEXITCODE
Pop-Location

# Check result
if ($ExitCode -eq 0) {
    Write-Host "✅ Done. Opening output folder..." -ForegroundColor Green
    $SessionOut = Join-Path "$RepoRoot\$OutputRel" "01_histogramas"
    if (Test-Path $SessionOut) { Start-Process explorer.exe $SessionOut } else { Start-Process explorer.exe "$RepoRoot\$OutputRel" }
} else {
    Write-Host "❌ Container run failed with exit code $ExitCode" -ForegroundColor Red
}

Read-Host "Press Enter to close"