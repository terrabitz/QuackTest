Write-Host "Starting Build"

$bins = Get-ChildItem -Path ./bin -Include "*.py"
foreach ($bin in $bins) {
    if ($env:APPVEYOR_REPO_TAG -eq "true") {
        $newName = "$($bin.BaseName)-${env:APPVEYOR_REPO_TAG_NAME}_win"
    } else {
        $newName = "$($bin.BaseName)-build${env:APPVEYOR_BUILD_VERSION}_win"
    }

    if ($bin.BaseName -like "*gui*") {
        pyinstaller -F ($bin.PSPath) -n $newName -w
    } else {
        pyinstaller -F ($bin.PSPath) -n $newName
    }
}

