# err-profiles
ACLs management for errbot in errbot

## Install
!repos install https://github.com/shengis/err-profiles.git

## Usage

### Restrict commands
* !access add Plugin:*
* !access add my_command

### Remove restrictions
* !access del Plugin:*
* !access del my_command

### List restrictions
* !access list

### Add groups
* !group add mygroup

### Remove groups
* !group del mygroup

### Add a user to a group
* !group add user mygroup @myuser

### Remove a user from a group
* !group del user mygroup @myuser

### Add a group to access restricted commands
* !access add group Plugin:* mygroup
* !access add group my_command mygroup

### Remove group from acceding a restricted command
* !access del group Plugin:* mygroup

## Developement
Issues and PR are welcomes
