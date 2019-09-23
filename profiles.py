import fnmatch
from errbot import BotPlugin, botcmd, cmdfilter


BLOCK_COMMAND = (None, None, None)


def get_acl_usr(msg):
    if hasattr(msg.frm, 'aclattr'):
        return msg.frm.aclattr
    return msg.frm.person

def canonize_cmd(cmd_str):
    """
    Canonize the command string into 'plugin:command' format
    """
    if ':' in cmd_str:
        return cmd_str

    return '*:' + cmd_str


class Profiles(BotPlugin):
    """
    ACLs with user and group management
    """

    def activate(self):
        super().activate()

        if 'groups' not in self:
            self['groups'] = {}

        if 'access' not in self:
            self['access'] = {}

    @cmdfilter
    def acls(self, msg, cmd, args, dry_run):
        cmd_str = "{plugin}:{command}".format(
                plugin=self._bot.all_commands[cmd].__self__.name,
                command=cmd)

        # Get groups allowed to access the command
        restricted = False
        groups = []
        for access, group in self['access'].items():
            if fnmatch.fnmatch(cmd_str, access):
                restricted = True
                groups.extend(group)

        # Check if the command is in the access list
        if not restricted:
            return (msg, cmd, args)

        usr = get_acl_usr(msg)

        # Check if user is in the groups allowed to access
        for group, users in self['groups'].items():
            if group in groups:
                if usr in users:
                    return (msg, cmd, args)

        # Check if the user is a bot admin
        if usr in self.bot_config.BOT_ADMINS:
            return (msg, cmd, args)

        if not dry_run and not self.bot_config.HIDE_RESTRICTED_ACCESS:
            self._bot.send_simple_reply(msg, "You're not allowed to access this command")

        return BLOCK_COMMAND

    @botcmd(template="access_list")
    def access_list(self, msg, args):
        """
        Show the access list
        """
        summary = []
        if self['access']:
            summary = [ (access, ' '.join(groups)) for access, groups in self['access'].items() ]

        return {'summary': summary}

    @botcmd
    def access_add(self, msg, cmd_str):
        """
        Add an entrie to the access list
        """
        if not cmd_str:
            return 'usage: !access add <cmd>'

        command = canonize_cmd(cmd_str)

        # Check if plugin or cmd match existing plugin or command
        match = False
        for c in self._bot.all_commands:
            cmd = "{plugin}:{command}".format(
                    plugin=self._bot.all_commands[c].__self__.name,
                    command=c)
            if fnmatch.fnmatch(cmd, command):
                match = True
                break

        if not match:
            return 'pattern does not match any command'

        with self.mutable('access') as access:
            if command not in access:
                access[command] = []
            else:
                return 'command already in access list'

        return 'command added to the access list'

    @botcmd
    def access_del(self, msg, cmd_str):
        """
        Remove an entrie of the access list
        """
        if not cmd_str:
            return 'usage: !access del <cmd>'

        command = canonize_cmd(cmd_str)

        with self.mutable('access') as access:
            if command not in access:
                return 'command wasnt there in the first place'
            else:
                del access[command]

        return 'command was removed of the access list'

    @botcmd(split_args_with=None)
    def access_add_group(self, msg, args):
        """
        Add a group to an entrie of the access list
        """
        if not args or not len(args) == 2:
            return 'usage: !access add group <cmd> <group>'

        cmd_str = args[0]
        group = args[1]

        command = canonize_cmd(cmd_str)

        with self.mutable('access') as access:
            if command not in access:
                return 'command not present in the access list'

# TODO: check if the group exists
            access[command].append(group)

        return 'group added to the access list'

    @botcmd(split_args_with=None)
    def access_del_group(self, msg, args):
        """
        Add a group to an entrie of the access list
        """
        if not args or not len(args) == 2:
            return 'usage: !access del group <cmd> <group>'

        cmd_str = args[0]
        group = args[1]

        command = canonize_cmd(cmd_str)

        with self.mutable('access') as access:
            if command not in access:
                return 'command not present in the access list'

            if group not in access[command]:
                return 'group wasnt there in the first place'

            access[command].remove(group)

        return 'group removed from the access list'

    @botcmd(template='group_list')
    def group_list(self, msg, args):
        """
        Show the group list
        """
        summary = []
        if self['groups']:
            summary = [ (group, ' '.join(users)) for group, users in self['groups'].items() ]

        return {'summary': summary}

    @botcmd
    def group_add(self, msg, group):
        """
        Add a group to the group list
        """
        if not group:
            return 'usage: !group add <group>'

        with self.mutable('groups') as groups:
            if group not in groups:
                groups[group] = []
            else:
                return 'group already in the group list'

        return 'group added to the group list'

    @botcmd
    def group_del(self, msg, group):
        """
        Remove a group from the group list
        """
        if not group:
            return 'usage: !group del <group>'

        with self.mutable('groups') as groups:
            if group not in groups:
                return 'group wasnt there in the first place'
            else:
                del groups[group]

        return 'group removed from the group list'

    @botcmd(split_args_with=None)
    def group_add_user(self, msg, args):
        """
        Add a user to a group
        """
        if not args or not len(args) == 2:
            return 'usage: !group add user <group> <user>'

        group = args[0]
        user = args[1]

        with self.mutable('groups') as groups:
            if group not in groups:
                return 'group not present in the group list'

            if user in groups[group]:
                return 'user already in the group'

            groups[group].append(user)

        return 'user was added to the group'

    @botcmd(split_args_with=None)
    def group_del_user(self, msg, args):
        """
        Remove user from a group
        """
        if not args or not len(args) == 2:
            return 'usage: !group del user <group> <user>'

        group = args[0]
        user = args[1]

        with self.mutable('groups') as groups:
            if group not in groups:
                return 'group not present in the group list'

            if user not in groups[group]:
                return 'user wasnt there in the first place'

            groups[group].remove(user)

        return 'user was removed from the group'
