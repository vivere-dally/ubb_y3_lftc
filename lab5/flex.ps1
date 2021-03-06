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
    [string]
    $FlexFileName = "pslexer.l",

    [Parameter(Mandatory = $false)]
    [string]
    $FlexFileNameExe = "pslexer",

    [Parameter(Mandatory = $false)]
    [switch]
    $Compile
)

$flexFileNameExeFullPath = Join-Path -Path $WorkingDir -ChildPath $FlexFileNameExe
if ($Compile) {
    $flexFileNameFullPath = Join-Path -Path $WorkingDir -ChildPath $FlexFileName
    & "flex" @($flexFileNameFullPath)
    & "gcc" @("lex.yy.c", "-o", $flexFileNameExeFullPath)
}

Get-ChildItem -Path $In -Filter "*.in" -File | ForEach-Object {
    $result = & "$flexFileNameExeFullPath.exe" @($_.FullName)
    $outPath = Join-Path -Path $Out -ChildPath $_.BaseName
    Set-Content -Path  "$outPath.out" -Value $result
}
