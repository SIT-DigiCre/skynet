import cli
import dm
import purge
from config import load_settings
from messages import load_messages

if __name__ == "__main__":
    args = cli.parse()
    settings = load_settings()
    if args.mode == "purge":
        purge.run(settings, load_messages())
    else:
        dm.run(settings, args.target, args.message_file)
