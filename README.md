# Coker Scripts
A collection of scripts written for IT tasks at Coker University.

## Loan Cancellation Automation
A three-step automated process that uses the output from an Informer report to send emails to students notifying them that they have been awarded loans and that they have the right to decline them.

## Users Leaving
A GAM deprovision tool that will automate __GOOGLE__ tasks to be completed when an employee leaves the university. It will do nothing for other systems (e.g. Colleague, AD, etc.).

## Move Users
A simple PowerShell script that will move users from one OU in AD to another OU, based on a CSV of sAMAccountnames. Very "hacky" right now, as the target OU is hardcoded, but that was the desired implementation by the end user, instead of including a second column in the input CSV.
