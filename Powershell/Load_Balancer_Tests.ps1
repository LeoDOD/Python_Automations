$sageURI = 'Your URl here!'
Function Get-MyIP {
  $text = (Invoke-Webrequest -Uri 'http://www.whatsmyip.org').content
  $text -match "Your IP Address is (\d+.\d+.\d+.\d+)"
  $Matches[0] 
}

For($i=0;$i -le 60;$i++) {
   $content = (Invoke-WebRequest -Uri $sageURI).AllElements | Select -First 1 -ExpandProperty innerText
   If($content -match 'Cloudflare'){
       Write-Host "Cloudflare error at $(Date)"
       Start-Sleep -Seconds 5
       Continue
   }
   $serverIP = $content -match 'Server\s*IP:\s*(\d+.\d+.\d+.\d+)'
   $userIP = $content -match 'User\s*IP:\s*(\d+.\d+.\d+.\d+)'
   If($currServerIP -eq $null) {
     $currServerIP = $serverIp
     $currUserIP = $userIP
   }
   If($currServerIP -ne $serverIp -or $currUserIP -ne $userIP) {
       Write-Host "$(Date)
       IP mismatch: Current Server IP: $serverIp
       Previous Server IP: $currServerIP
       IP mismatch: Current User IP: $userIp
       Previous User IP: $currUserIP
       
       Restarting..."

       $currUserIP = Get-MyIP
       $i = 0

   }
   $currServerIP = $serverIp
   $currUserIP = $userIP
   $results += $content
   Start-Sleep -Seconds 5
}

$timestamp = Get-Date -Format o | foreach {$_ -replace ":", "."}
$results | Out-File -FilePath ((pwd).Path + "\Downloads\$($timestamp)_$($env:UserName)_20.txt")