# plugins/system_plugin/powershell_adapter.ps1
Write-Host "[dex.system.powershell] Starting interactive adapter. Type 'exit' to quit."
while ($true) {
    $cmd = Read-Host "ps>"
    if ($cmd -eq "exit") { break }
    try {
        Invoke-Expression $cmd
    } catch {
        Write-Host "Error: $_"
    }
}