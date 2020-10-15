param([int]$a,[int]$b)

while (0 -ne $b) {
    [int]$temp = $a % $b;
    $a = $b;
    $b = $temp;
}

Write-Host $a;
