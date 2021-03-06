# This is a hack of crap straight from the pit of hell. It does not follow even a semblance of best practice and should not be used by anyone, ever.
# User requirements resulted in this abomination of hard-coded values. I am so sorry, and I feel bad for this atrocity. At least it's a super simple piece of crap.

#Specify target OU (this is where users will be moved). Get this by right-clicking on the OU, choosing "Properties" => "Attribute Editor" then copying the "distinguishedName" property.
$TargetOU = "OU=Dec 2019,OU=Alumni,OU=Users,OU=Coker,DC=profs,DC=local"

#==========================================
# NO CHANGES PAST THIS POINT!
#==========================================

# Import AD Module
import-module ActiveDirectory

# Initialize counter
$count = 0

# Import CSV data
$Imported_csv = Import-Csv -Path "C:\Move_Users\moves.csv"

$Imported_csv | ForEach-Object {
    # Retrieve DN of User
    $UserDN = (Get-ADUser -Identity $_.Name).distinguishedName
    $UserSAM = (Get-ADUser -Identity $_.Name).SamAccountName
    Write-Host " Moving $UserSAM... "
    # Move user to target OU
    Move-ADObject -Identity $UserDN -TargetPath $TargetOU
    $count++
}

Write-Host "Completed operation"
Write-Host "Attempted to move $count account(s)"
pause
