$ErrorActionPreference = "Stop"

Write-Host "AI-Powered Agentic Workflow - Full Validation" -ForegroundColor Cyan
Write-Host "Repository: $PWD"

if (-not (Test-Path ".env")) {
    throw "Missing .env file. Copy .env.example to .env and set OPENAI_API_KEY first."
}

New-Item -ItemType Directory -Force -Path "submission_outputs" | Out-Null

function Invoke-AgentTest {
    param(
        [Parameter(Mandatory = $true)][string]$Script,
        [Parameter(Mandatory = $true)][string]$OutputFile
    )

    Write-Host "`n============================================================" -ForegroundColor DarkGray
    Write-Host "Running: $Script" -ForegroundColor Yellow
    Write-Host "============================================================" -ForegroundColor DarkGray

    python $Script 2>&1 | Tee-Object -FilePath $OutputFile

    if ($LASTEXITCODE -ne 0) {
        throw "Test failed: $Script (exit code $LASTEXITCODE)"
    }
}

Invoke-AgentTest "phase_1/tests/direct_prompt_agent.py" "submission_outputs/01-direct-prompt.txt"
Invoke-AgentTest "phase_1/tests/augmented_prompt_agent.py" "submission_outputs/02-augmented-prompt.txt"
Invoke-AgentTest "phase_1/tests/knowledge_augmented_prompt_agent.py" "submission_outputs/03-knowledge-augmented-prompt.txt"
Invoke-AgentTest "phase_1/tests/rag_knowledge_prompt_agent.py" "submission_outputs/04-rag-knowledge-prompt.txt"
Invoke-AgentTest "phase_1/tests/evaluation_agent.py" "submission_outputs/05-evaluation-agent.txt"
Invoke-AgentTest "phase_1/tests/routing_agent.py" "submission_outputs/06-routing-agent.txt"
Invoke-AgentTest "phase_1/tests/action_planning_agent.py" "submission_outputs/07-action-planning-agent.txt"
Invoke-AgentTest "phase_2/agentic_workflow.py" "submission_outputs/08-agentic-workflow.txt"

Write-Host "`nAll project scripts completed successfully." -ForegroundColor Green
Write-Host "Execution evidence is in submission_outputs/." -ForegroundColor Green
Write-Host "Review those files for secrets before committing them." -ForegroundColor Green
