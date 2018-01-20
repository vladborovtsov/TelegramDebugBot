import config as CONFIG
import json
import os


def AddSubscription(chat):
    CHATS = _load()
    for ch in CHATS:
        if ch["id"] == chat["id"]:
            return False

    CHATS.append(json.loads(chat.to_json()))
    _save(CHATS)
    return True


def RemoveSubscription(chat):
    CHATS = _load()
    for ch in CHATS:
        if ch["id"] == chat["id"]:
            CHATS.remove(ch)
            _save(CHATS)
            return True
    return False


def AllChatIds():
    return [a["id"] for a in _load()]


def _load():
    if os.path.exists(CONFIG.CHAT_IDs_FILENAME):
        CHATS = json.load(open(CONFIG.CHAT_IDs_FILENAME, "r+t"))
    else:
        CHATS = []
    return CHATS


def _save(CHATS):
    f = open(CONFIG.CHAT_IDs_FILENAME, "w+t")
    f.write(json.dumps(CHATS, indent=1))
    f.close()