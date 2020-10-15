[int]$a = Read-Host;[int]$b = Read-Host;[int]$c = Read-Host;
[int]$min = $a;[int]$max = $a;

if ($b -lt $min) {
    $min = $b;
}

if ($c -lt $min) {
    $min = $c;
}

if ($b -gt $max) {
    $max = $b;
}

if ($c -gt $max) {
    $max = $c;
}

Write-Host $min;
Write-Host $max;
