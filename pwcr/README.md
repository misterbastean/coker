# Password Change Report
A program designed to query Google Admin via GAMADV-XTD3
and get a list of users who have/have not changed their
password in the last 6 months

## Options
- org_unit: Full OU name to search (e.g. "/Students/Commuters"). Default: "/Students"
- --months: Number of months to search, 1-6
- -c/--changed: Show users who have changed their password instead of those who have not
- -nc/--not-changed: Show users who have not changed their password (DEFAULT)

## Syntax
`pwcr org_unit [--months=1] [-c/--changed || -nc/--not-changed]`
