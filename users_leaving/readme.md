# GAM Deprovision

## Summary
A tool that will automate **_GOOGLE_** tasks to be completed when an employee leaves the University.

## Installation
1. Install [GAMADV-XTD](https://github.com/taers232c/GAMADV-XTD) prior to cloning
2. Update the configuration section at the top of main.py

## Usage
1. Update data in users.csv. **_DO NOT_** edit the headers.
2. Make sure the csv is in the same directory as main.py
3. Run main.py

### Headers and Format of users.csv
|email*|remainActive*|vacationSubject*|vacationMessage*|managerEmail|driveTransferRecipient|
|---|---|---|---|---|---|
|employee1@company.com|n|Email Subject Here|Email Body Here|manager@company.com||
|employee2@company.com|y|Email Subject Here|Email Body Here|manager@company.com|replacement@company.com|
|employee3@company.com|y|Email Subject Here|Email Body Here|||

Required fields are marked with an asterisk (*).

If no value is supplied for managerEmail, no forwarding will be set up.

If no value is supplied for driveTransferRecipient, the contents of the Drive will be transferred to the account designated in the config section of main.py.

## Outcomes
1. Reset user password to random string
1. Set vacation Gmail message
2. Disable email forwarding
3. Add forwarding to manager (if desired).
4. Delete OAuth Tokens, asps, and backup codes
5. Copy entire Drive to itdrive@coker.edu Drive
6. Delete recovery information
7. Remove email delegates
8. Disable IMAP and POP
9. Hide user from directory
10. Remove user from all groups they belong to
11. Suspend user to kick off all logged-in sessions
12. If user account needs to remain active, unsuspend so delegation and vacation responses function

## Brief Outline of Each Step
### Reset password
Resets the former employee's (FE) password to a random string so that they can no longer login. This is redundant if their AD password has already been changed, as GADS will update it. But it's better to be safe.

### Set vacation message
Sets a vacation responder message to let anyone emailing the FE know that they are no longer with the University and providing an updated contact. This message will need to be provided by the FE's manager.

### Remove forwarding rules
All forwarding rules need to be removed in case the FE had set them up to forward to another address. This is for security purposes to make sure they are not continuing to receive emailes.

### Add forwarding to manager
In some circumstances, the FE's manager (or another Coker employee) will need to be set up to receive all their messages in order to preserve communication.

### Delete tokens and codes
These need to be deleted so that third-party apps cannot be used to login to the account. These apps include mail clients, file-sharing apps, etc. This step also deletes the "emergency" backup codes that each user can setup.

### Copy Drive
In order to preserve documents, the FE's entire drive has ownership transferred to itdrive@coker.edu. Currently, there is
no simple way to implement Coker's naming scheme programmatically, so it will need to be done manually after the transfer has
been completed.

### Change Recovery information
This step is taken to prevent users from calling Google to get into their accounts using the recovery information. This _should_ be redundant, as Google should not do this, but it has happened in other orgs, and it doesn't hurt to be sure.

### Remove Email Delegates
If the FE has any emails delegated to them, these need to be removed.

### Disable IMAP/POP
To ensure FE cannot access mail from any devices for which this was enabled.

### Hide user from directory
Helps keep the Gmail directory clean, as the email will remain extant, but suspended, so we don't want it to show up on anyone's address book.

### Remove user from groups
If the user is in any groups, remove them. Again, just to keep the groups clean and prevent any problems from messages being sent to suspended accounts.

### Suspend/Unsuspend user
This is a workaround to force any users still logged in to reauthenticate before being able to do anything. Because their AD password will have been reset prior to this, they will not be able to do so.