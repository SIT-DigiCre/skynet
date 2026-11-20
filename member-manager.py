from config import load_settings
from messages import load_messages
from purge import run

if __name__ == "__main__":
    run(load_settings(), load_messages())
