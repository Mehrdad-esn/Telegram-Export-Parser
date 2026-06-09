import json
from pathlib import Path
from app import list_chat_names
from stats import MessageStats


def test_list_chat_names():
    names = list_chat_names(Path('test_data.json'))
    assert "Test Chat" in names
    assert "دوستان" in names


def test_message_stats_total():
    with open('test_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    chat = data['chats']['list'][0]
    stats = MessageStats(chat.get('messages', []))
    assert stats.get_total_messages() == len([m for m in chat.get('messages', []) if m.get('type') == 'message'])
