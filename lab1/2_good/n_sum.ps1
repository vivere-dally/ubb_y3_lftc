[int]$n = Read-Host;[int]$i = 0;[int]$sum = 0;
while ($i -lt $n) {
    [int]$temp = Read-Host;
    $sum = $sum + $temp;
    $i = $i + 1;
}

Write-Host $sum;
