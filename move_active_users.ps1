 # Import modules
import-module ActiveDirectory

# Constants
$CSVPath = "C:\Move_Users\AD - REGISTERED.csv"

# OU Constants
$OUNotActive = "OU=NotActiveCurrentSemester,OU=Day,OU=Students,OU=Users,OU=Coker,DC=profs,DC=local"
$OUStudentResident = "OU=Resident,OU=Day,OU=Students,OU=Users,OU=Coker,DC=profs,DC=local"
$OUStudentCommuter = "OU=Commuter,OU=Day,OU=Students,OU=Users,OU=Coker,DC=profs,DC=local"
$OUGradProgram = "OU=GradProgram,OU=Students,OU=Users,OU=Coker,DC=profs,DC=local"
$OUADPFDTC = "OU=ADP.FDTC,OU=ADP,OU=Students,OU=Users,OU=Coker,DC=profs,DC=local"
$OUADPFlorence = "OU=ADP.FLORENCE,OU=ADP,OU=Students,OU=Users,OU=Coker,DC=profs,DC=local"
$OUADPHartsville = "OU=ADP.HARTSVILLE,OU=ADP,OU=Students,OU=Users,OU=Coker,DC=profs,DC=local"
$OUADPMarion = "OU=ADP.MARION,OU=ADP,OU=Students,OU=Users,OU=Coker,DC=profs,DC=local"
$OUAPDMidlands = "OU=ADP.MIDLANDS,OU=ADP,OU=Students,OU=Users,OU=Coker,DC=profs,DC=local"
$OUADPNortheastern = "OU=ADP.NORTHEASTERN,OU=ADP,OU=Students,OU=Users,OU=Coker,DC=profs,DC=local"
$OUADPOnline = "OU=ADP.ONLINE,OU=ADP,OU=Students,OU=Users,OU=Coker,DC=profs,DC=local"
$OUHighSchool = "OU=High School,OU=Students,OU=Users,OU=Coker,DC=profs,DC=local"

# Treat all errors as terminating, so we can catch and log them
$ErrorActionPreference = 'Stop'


# Delete old logs
$Path = "C:\Move_Users\automatic/logs"
$Daysback = "-30"
 
$CurrentDate = Get-Date
$DatetoDelete = $CurrentDate.AddDays($Daysback)
Get-ChildItem $Path | Where-Object { $_.LastWriteTime -lt $DatetoDelete } | Remove-Item


# Logging Function
function Write-Log
{
    [CmdletBinding()]
    Param
    (
        [Parameter(Mandatory=$true,
                   ValueFromPipelineByPropertyName=$true)]
        [ValidateNotNullOrEmpty()]
        [Alias("LogContent")]
        [string]$Message,

        [Parameter(Mandatory=$false)]
        [Alias('LogPath')]
        [string]$Path="C:\Move_Users\automatic\logs\logs_$(Get-Date -Format "yyyy-MM-dd_HH-mm").txt",
        
        [Parameter(Mandatory=$false)]
        [ValidateSet("Error","Warn","Info")]
        [string]$Level="Info",
        
        [Parameter(Mandatory=$false)]
        [switch]$NoClobber
    )

    Begin
    {
        # Set VerbosePreference to Continue so that verbose messages are displayed.
        # $VerbosePreference = 'Continue'
    }
    Process
    {
        
        # If the file already exists and NoClobber was specified, do not write to the log.
        if ((Test-Path $Path) -AND $NoClobber) {
            Write-Error "Log file $Path already exists, and you specified NoClobber. Either delete the file or specify a different name."
            Return
            }

        # If attempting to write to a log file in a folder/path that doesn't exist create the file including the path.
        elseif (!(Test-Path $Path)) {
            Write-Verbose "Creating $Path."
            $NewLogFile = New-Item $Path -Force -ItemType File
            }

        else {
            # Nothing to see here yet.
            }

        # Format Date for our Log File
        $FormattedDate = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

        # Write message to error, warning, or verbose pipeline and specify $LevelText
        switch ($Level) {
            'Error' {
                Write-Error $Message
                $LevelText = 'ERROR:'
                }
            'Warn' {
                Write-Warning $Message
                $LevelText = 'WARNING:'
                }
            'Info' {
                Write-Verbose $Message
                $LevelText = 'INFO:'
                }
            }
        
        # Write log entry to $Path
        "$FormattedDate $LevelText $Message" | Out-File -FilePath $Path -Append
    }
    End
    {
    }
}


# Import CSV data
$Imported_csv = Import-Csv -Path $CSVPath
Write-Log -Message "CSV imported, begin move process..." -Level Info

# Get number of rows
[int]$LinesInFile = 0
$reader = New-Object IO.StreamReader $CSVPath
while($reader.ReadLine() -ne $null){ $LinesInFile++ }
$reader.Close()
Write-Log -Message "Total number of students in CSV: $($LinesInFile-1)"

# Initialize counter
[int]$count = 0
[int]$movedCount = 0


$Imported_csv | ForEach-Object { # For each user
    Try {
        $username = $_.'C69 Stu Username'
        $currentHome = $_.'C69.STU.CURRENT.HOME.LOCATION'
        $studentType = $_.'Student Type'
        $residency = $_.'Stu Current Residency Status'

        # Search NotActiveCurrentSemester OU for the student. If they're not there, it will be empty.
        $user = Get-ADUser -Filter "SamAccountName -eq '$username'" -SearchBase "OU=NotActiveCurrentSemester,OU=Day,OU=Students,OU=Users,OU=Coker,DC=profs,DC=local" -SearchScope OneLevel

        # If user is in NotActiveCurrentSemester
        if ($user) {
            Write-Log -Message "User $username found in NotActiveCurrentSemester." -Level Info
    
            # If user is a Day student
            if ($studentType -eq "D") {
                Write-Log -Message "User is a Day student, checking residency" -Level Info
                if ($residency -eq "DORM") {  # If user is a Resident, move to Student/Resident OU
                    Write-Log -Message "User is a DORM student, moving to Students/Day/Resident" -Level Info
                    Move-ADObject -Identity $user -TargetPath $OUStudentResident
                    $movedCount++
                } elseif ($residency -eq "COM") {  # Else if user is a Commuter, move to Student/Commuter OU
                    Write-Log -Message "User is a COM student, moving to Students/Day/Commuter" -Level Info
                    Move-ADObject -Identity $user -TargetPath $OUStudentCommuter
                    $movedCount++
                } else { # Else, log error
                    Write-Log -Message "Day student $username residency not DORM or COM." -Level Error
                }
            } else { # Else, move user to correct OU
                Write-Log -Message "User is not a Day student" -Level Info
                Switch ($studentType) {
                    "E" {
                        Write-Log -Message "Type is E, move user to Students/ADP/APD.HARTSVILLE" -Level Info
                        Move-ADObject -Identity $user -TargetPath $OUADPHartsville
                        $movedCount++
                    }
                    "FDTC" {
                        Write-Log -Message "Type is FDTC, move user to Students/ADP/APD.FDTC" -Level Info
                        Move-ADObject -Identity $user -TargetPath $OUADPFDTC
                        $movedCount++
                    }
                    "FL" {
                        Write-Log -Message "Type is FL, move user to Students/ADP/APD.FLORENCE" -Level Info
                        Move-ADObject -Identity $user -TargetPath $OUADPFlorence
                        $movedCount++
                    }
                    "H" {
                        Write-Log -Message "Type is H, move user to Students/High School" -Level Info
                        Move-ADObject -Identity $user -TargetPath $OUHighSchool
                    }
                    "M" {
                        Write-Log -Message "Type is M, move user to Students/ADP/APD.MARION" -Level Info
                        Move-ADObject -Identity $user -TargetPath $OUADPMarion
                    }
                    "MP" {
                        Write-Log -Message "Type is MP, move user to Students/GradProgram" -Level Info
                        Move-ADObject -Identity $user -TargetPath $OUGradProgram
                        $movedCount++
                    }
                    "MTC" {
                        Write-Log -Message "Type is MTC, move user to Students/ADP/APD.MIDLANDS" -Level Info
                        Move-ADObject -Identity $user -TargetPath $OUAPDMidlands
                        $movedCount++
                    }
                    "N" {
                        Write-Log -Message "Type is N, move user to Students/ADP/ADP.NORTHEASTERN" -Level Info
                        Move-ADObject -Identity $user -TargetPath $OUADPNortheastern
                        $movedCount++
                    }
                    "OUG" {
                        Write-Log -Message "Type is OUG, move user to Students/ADP/ADP.ONLINE" -Level Info
                        Move-ADObject -Identity $user -TargetPath $OUADPOnline
                        $movedCount++
                    }
                    Default {
                        Write-Log -Message "studentType $studentType for $username is invalid! Should be FDTC, FL, E, M, MTC, N, O, or MP." -Level Error
                    }
                }
            }
        } else { # Else, pass
            Write-Log -Message "User $username not in NotActiveCurrentSemester. Skipping..." -Level Info
        }
        $count++
    } Catch {
        $ErrorMessage = $_.Exception.Message
        $FailedItem = $_.Exception.ItemName
        Write-Log -Message $ErrorMessage -Level Warn
    }
}
Write-Log -Message "Done checking users" -Level Info

if ($count -eq $($LinesInFile - 1)) {
    Write-Log -Message "SUCCESS: Total users checked: $count. Total users in CSV: $($LinesInFile - 1). Total users moved: $movedCount." -Level Info
} else {
    Write-Log -Message "ERROR: Total users checked: $count. Total users in CSV: $($LinesInFile - 1).  Total users moved: $movedCount." -Level Warn
}
