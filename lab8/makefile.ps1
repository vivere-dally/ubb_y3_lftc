[CmdletBinding()]
param (
    [Parameter(Mandatory = $false)]
    [string]
    $In = ".\in",

    [Parameter(Mandatory = $false)]
    [string]
    $Out = ".\out",

    [Parameter(Mandatory = $false)]
    [string]
    $WorkingDir = ".",

    [Parameter(Mandatory = $false)]
    $YaccFileName = "mmlp.y",

    [Parameter(Mandatory = $false)]
    [string]
    $FlexFileName = "mmlp.l",

    [Parameter(Mandatory = $false)]
    [string]
    $FlexFileNameExe = "mmlp",

    [Parameter(Mandatory = $false)]
    [switch]
    $Compile
)

$flexFileNameExeFullPath = Join-Path -Path $WorkingDir -ChildPath $FlexFileNameExe
if ($Compile) {
    $yaccFileNameFullPath = Join-Path -Path $WorkingDir -ChildPath $YaccFileName
    & "bison" @("-y", "-d", $yaccFileNameFullPath)
    $flexFileNameFullPath = Join-Path -Path $WorkingDir -ChildPath $FlexFileName
    & "flex" @($flexFileNameFullPath)
    & "gcc" @("lex.yy.c", "y.tab.c", "-o", $flexFileNameExeFullPath)
}

if (Test-Path "$flexFileNameExeFullPath.exe") {
    Get-ChildItem -Path $In -File | ForEach-Object {
        $result = & "$flexFileNameExeFullPath.exe" @($_.FullName)
        $outPath = Join-Path -Path $Out -ChildPath $_.BaseName
        Set-Content -Path  "$outPath.out" -Value $result
    }
}
else {
    Write-Error "Compilation failed!"
}

