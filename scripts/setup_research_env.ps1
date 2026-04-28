$ErrorActionPreference = 'Stop'

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $ScriptDir '..')

$Python = $env:PYTHON_BIN
if ([string]::IsNullOrWhiteSpace($Python)) {
    $PyLauncher = Get-Command py -ErrorAction SilentlyContinue
    if ($null -ne $PyLauncher) {
        $Python = 'py -3'
    } else {
        $Python = 'python'
    }
}

$ArgsList = @('"' + (Join-Path $ScriptDir 'setup_research_env.py') + '"', '--workspace', '"' + $RepoRoot + '"')
$ArgsList += $args
$ArgString = $ArgsList -join ' '

Invoke-Expression "$Python $ArgString"
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
