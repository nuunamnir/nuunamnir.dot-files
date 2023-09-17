# Reset faillock
## Description and Process
After too many failed attempts to login, the account gets locked for a certain period of time. To reset this lock, log in as root user and run following command:
```
faillock --user username --reset
```