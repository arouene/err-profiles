# err-profiles
ACLs management for errbot in errbot

## Install
!repos install https://github.com/shengis/err-profiles.git
```
# Add an administrator group
!group add administrators
# Add a member to the administrator group
!group add user administrators @user
# Add the Profile plugin to the restricted access
!access add Profiles:*
# Authorize the administrator group to access
!access add group Profiles:* administrators
```

These commands should be done by an errbot administrator to be able to use Profiles after adding it to the restricted access.

## Usage

### Restrict commands
* !access add Plugin:*
* !access add my_command

### Remove restrictions
* !access del Plugin:*
* !access del my_command

### Show restrictions
* !access list

### Add groups
* !group add mygroup

### Remove groups
* !group del mygroup

### Add a user to a group
* !group add user mygroup @myuser

### Remove a user from a group
* !group del user mygroup @myuser

### Show groups
* !group list

### Add a group to access restricted commands
* !access add group Plugin:* mygroup
* !access add group my_command mygroup

### Remove group from acceding a restricted command
* !access del group Plugin:* mygroup

## Development
Issues and PR are welcomes
