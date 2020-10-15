param([array]$numbers)

[array]$evens = @();
foreach ($number in $numbers) {
    if ($number % 2 -eq 0) {
        $evens = $evens + $number;
    }
}

Write-Host $evens;
