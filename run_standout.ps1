$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $repoRoot

if (-not (Test-Path ".env")) {
    throw "Repository-level .env file was not found. Add OPENAI_API_KEY before running the standout demo."
}

$outputPath = "submission_outputs/09-standout-alternate-workflow.txt"

Write-Host "Running alternate workflow + supplemental Product Manager quality scoring..."
python phase_2/standout_demo.py 2>&1 | Tee-Object -FilePath $outputPath

if ($LASTEXITCODE -ne 0) {
    throw "Standout demonstration failed with exit code $LASTEXITCODE. Review $outputPath before committing it."
}

Write-Host ""
Write-Host "Standout evidence created successfully: $outputPath"
Write-Host "Review the file for secrets before committing."
