from datetime import datetime


def convert_timestamp_to_date(timestamp: float) -> datetime:
    """Convert timestamp to date"""
    # Convert timestamp to date
    date = datetime.fromtimestamp(timestamp)
    return date


def get_day_from_date(date: datetime) -> str:
    """Get day from date"""
    day = date.weekday()
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return days[day]


def get_message(message_json) -> str:
    """Get message"""
    message = message_json["content"]
    return message


def get_reactions(message_json) -> list:
    """Get reactions"""
    reactions = message_json["reactions"]
    return reactions


def get_date(message_json) -> datetime:
    """Get date of the message"""
    timestamp = message_json["timestamp_ms"]
    timestamp = float(timestamp / 1000)
    date = convert_timestamp_to_date(timestamp)
    return date


def get_nb_words(message: str) -> int:
    """Get number of words in a message"""
    # Split message into words
    words = message.split()
    # Get number of words
    nb_words = len(words)
    return nb_words


def get_nb_reactions(reactions: list) -> int:
    """Get number of reactions"""
    nb_reactions = len(reactions)
    return nb_reactions
