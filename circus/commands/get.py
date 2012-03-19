from circus.commands.base import Command, ok, error
from circus.exc import ArgumentError, MessageError
from circus.util import convert_opt

class Get(Command):
    """Get the value of a show option"""

    name = "get"
    properties = ['name', 'keys']

    def message(self, *args, **opts):
        if len(args) < 2:
            raise ArgumentError("number of arguments invalid")

        return self.make_message(name=args[0], keys=args[1:])

    def execute(self, trainer, props):
        show = self._get_show(trainer, props.get('name'))

        # get options values. It return an error if one of the asked
        # options isn't found
        options = {}
        for name in props.get('keys', []):
            if name in show.optnames:
                options[name] = getattr(show, name)
            else:
                raise MessageError("%r option not found" % name)

        return {"options": options}

    def console_msg(self, msg):
        if msg['status'] == "ok":
            ret = []
            for k, v in msg.get('options', {}).items():
                ret.append("%s: %s" % (k, convert_opt(k, v)))
            return "\n".join(ret)
        return self.console_msg(self, msg)