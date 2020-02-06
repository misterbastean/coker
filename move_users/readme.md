# Move Users
This is a PowerShell script that moves users from one OU in ActiveDirectory to another OU. It needs to be on the AD domain controller and requires to be run as admin, by a user who has permissions in AD to move the users. It does NOT automatically elevate privileges, thus why it needs to be run as admin.

This is a hacky hack of a script due to end-user requirements - I would highly suggest rewriting to eliminate hard-coded values before using in another environment. Don't crucify me for the bad practices evidenced here - I tried and was overruled :-(

## Choosing Target OU
Per end-user request, the target OU is hard-coded into the script. To change, open the .ps1 file and edit the $TargetOU variable to the desired distringuishedName of the target OU. To find this, open AD Users and Computers on the DC, find the target OU, right click and choose "Properties" => "Attribute Editor". Copy the "distinguishedName" and paste into the script (making sure to put it inside the quotation marks). I hate this so much...

## Input CSV
The input CSV just needs one column titled "Name" with the sAMAccountname of each user to be moved. Currently, it's hard-coded to "C:\Move_Users\moves.csv" (again, per user request). I'm so sorry...
