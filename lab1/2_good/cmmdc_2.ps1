[int]$a = Read-Host;
[int]$b = Read-Host;

while (0 -ne $b) {
    [int]$temp = $a % $b;
    $a = $b;
    $b = $temp;
}

Write-Host $a;
