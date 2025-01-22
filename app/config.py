START_TEXT = "Hi {user},\n\nI am your Auto Request Accept Bot!"
HELP_TEXT = "Here's how to use the bot:\n\n- Add me to your channel\n- I will approve join requests automatically."
ACCEPTED_TEXT = "Hey {user},\n\nYour request to join {chat} is accepted ✅"

START_BUTTONS = [
    [
        {"text": "Help", "callback_data": "help"},
        {"text": "Updates", "url": "https://t.me/mkn_bots_updates"},
        {"text": "Support", "url": "https://t.me/MKN_BOTZ_DISCUSSION_GROUP"}
    ]
]

HELP_BUTTONS = [
    [
        {"text": "Back", "callback_data": "start"}
    ]
]

START_IMAGE = "https://example.com/start_image.jpg"
HELP_IMAGE = "https://example.com/help_image.jpg"
ACCEPTED_IMAGE = "https://example.com/accepted_image.jpg"