# Auto-Elevate to Admin.
if (!([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) { Start-Process powershell.exe "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs; exit }

#region Variables{
# Global variables with the Server's names or ips
$Gateway = @{DEV = @('GW01');
             QA = @('GW01', 'GW02');
             PROD = @('GW01', 'GW02','GW03', 'GW04', 'GW05', 'GW06')}
#endregion}

#Thsi will make the script execute until you actively decide to exit out from the application.
Do{
    # i like to make ps script a bit Flashy
    Echo `n '

    __    ____  ______   ____  ________________  ___________    ____________ 
   / /   / __ \/ ____/  / __ \/ ____/_  __/ __ \/  _/ ____/ |  / / ____/ __ \
  / /   / / / / / __   / /_/ / __/   / / / /_/ // // __/  | | / / __/ / /_/ /
 / /___/ /_/ / /_/ /  / _, _/ /___  / / / _, _// // /___  | |/ / /___/ _, _/ 
/_____/\____/\____/  /_/ |_/_____/ /_/ /_/ |_/___/_____/  |___/_____/_/ |_|  
                                                                                                                                                 
'
    Echo "Select Server:
        1.- Gateway
        2.- MVR
        3.- Sage Exchange
        4.- UNO
        5.- Exit"

    #This makes sure that the input from the user is between that allowed options.
    do {
        $Server = Read-Host -Prompt 'Input your Selection [1-5]'
        }
    until($Server -ge 1 -and $Server -le 5)

    #Options
        if($Server -eq 1){
            Echo "Select Environment:
            - DEV
            - QA
            - PROD"
            do {
                $domain = Read-Host -Prompt 'Input your Selection'
            }
            until($domain -in ('DEV','QA', 'PROD'))
            $Target = $Gateway[$domain]
            $Server = "Gateway"
        }
        elseif($Server -eq 2){
            Echo "Select Environment:
            - DEV
            - QA
            - PROD"
            do {
                $domain = Read-Host -Prompt 'Input your Selection'
            }
            until($domain -in ('DEV','QA', 'PROD'))
            $Target = $MVR[$domain]
            $Server = "MVR"
        }
        elseif($Server -eq 3){
            Echo "Select Environment:
            - DEV
            - QA
            - PREPROD
            - PROD"
            do {
                $domain = Read-Host -Prompt 'Input your Selection'
            }
            until($domain -in ('DEV', 'QA', 'PREPROD', 'PROD'))
            $Target = $SE[$domain]
            $Server = "SE"
        }
        elseif($Server -eq 4){
            Echo "Select Environment:
            - DEV
            - QA
            - PROD"
            do {
                $domain = Read-Host -Prompt 'Input your Selection'
            }
            until($domain -in ('DEV','QA', 'PROD'))
            $Target = $UNO[$domain]
            $Server = "UNO"
        }
        elseif($Server -eq 5){
        Echo "Closing Log Retriever..."
        Start-Sleep -Seconds 2
        Exit
        }
        do {
            $address = Read-Host -Prompt 'Input location of the Logfile'
            $file_name = Read-Host -Prompt 'Input the name of the Logs we are retrieving'
            Echo "We will be retrieving $address\$file_name from the following Servers: $Target"
            $Continue = Read-Host -Prompt 'Is this correct?[Y-N]'
            if ($Continue -eq 'N') {break}
        }
        until($Continue -eq 'Y' -or $Continue -eq 'N')
        $stamp = get-date -u "%m-%d-%y_%H%M%S"
        $folder ="$Server-$stamp"
        New-Item -ItemType "Directory" -Path "$env:USERPROFILE\Desktop\$folder"
        foreach ($HostName in $Target){
            $SourceSession = New-PSSession $HostName
            Try{
                Copy-Item -FromSession $SourceSession -path "$address\$file_name" "$env:USERPROFILE\Desktop\$folder\2019-02-05-$HostName.log"
            } Catch {
                $ErrorMessage = $_.Exception.Message
                $FailedItem = $_.Exception.ItemName
                echo $ErrorMessage
                echo $FailedItem
                Write-Host "Server $HostName does not Contain a log name $file_name at the location $address"
            }
        }
    }while($true)
