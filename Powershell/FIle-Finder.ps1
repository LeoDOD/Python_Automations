# Auto-Elevate to Admin.
if (!([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) { Start-Process powershell.exe "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs; exit }
# List every single file under directory & Returns every file that matches the Regex.
$Results = Get-ChildItem -Path "C:\" -Recurse | Where-Object { $_.Name -Match '(\w+\.config\b|\w+\.cs\b|\w+\.vb\b|\w+\.js\b|\w+\.json\b|\w+\.txt\b|\w+\.yml\b)'}
# Declare the Variable to store all the results in.
$hashtable = @()
# We iterate Thru all of our results.
Foreach($file in $Results){
    $Matches = Select-String -Path $file -Pattern '((<machineKey [^(><.)]+\/>)|("[uU]ser\s[iI][dD]=[\S]+|[pP]assword=[\S]+|[dD]atabase=[\w0-9\-]+|[sS]erver=[\w0-9\-\\\.]+))' -AllMatches
        if($Matches)
        {
            # All the variable we will use this to store each individual result.
            $linePath = $null
            $lineLineNumber = $null
            $lineLine = $null
            # Container for the results of the current file.
            $hash = $null
            # We iterate thru all the Files that Matched the previous Regex.
            foreach($line in $Matches)
            {
                # We store, the path, line number, the line it self.
                $linePath = $line.Path
                $lineLineNumber = $line.LineNumber
                $lineLine = $line.Line
                # We check if we found a machine Keyif so, save the match else just mark it as false        
                if($lineline -match "(<machineKey [^(><.)]+\/>)")
                {
                    $MHtag = $matches[0]
                }
                else
                {
                    $MHtag = "False"
                }
                #Store all the results in the Hash and then append the hash to the Final results Hash.
                $hash = new-object PSobject -Property @{"File_Name"=$file.Name;"File_Path"="$linePath";"Line_number"="$lineLineNumber";"Machine_KEY?"="$MHtag" ;"String"="$lineLine"}
                $hashtable += $hash
            }
        }
}
#Create a name for the csv and then load the final results on to it.
$servername = $env:COMPUTERNAME
$stamp = get-date -u "%m%d%y_%H%M%S"
$csvname = $servername + "_" + $stamp + ".csv"
$hashtable | sort -Descending File_path | select File_Name,File_path,Line_number,Machine_KEY?,String | export-csv "$env:USERPROFILE\Desktop\$folder\$csvname" -NoTypeInformation
$SourceSession = New-PSSession $env:COMPUTERNAME
Copy-Item -FromSession $SourceSession -path "$env:USERPROFILE\Desktop\$csvname.csv" -Destination 'C:\Users\ldoliveira\Desktop'
