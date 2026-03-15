function Sync-Directory {
    [CmdletBinding()]
    param(
        [ValidateNotNullOrEmpty()][string]$name,
        [ValidateNotNullOrEmpty()][string]$srcDir,
        [ValidateNotNullOrEmpty()][string]$destDir
    )

    # Header
    $text = "Sync $name Folder"
    $border = "=" * $text.length
    Write-Host $border
    Write-Host $text
    Write-Host $border
    Start-Sleep -Seconds 1

    # Dry run
    Robocopy.exe $srcDir $destDir /MIR /Z /MT:4 /R:1 /W:1 /NJS /NDL /L
    Write-Host
    Pause

    # Sync directory
    Robocopy.exe $srcDir $destDir /MIR /Z /MT:4 /R:1 /W:1 /NJH /NDL

}
