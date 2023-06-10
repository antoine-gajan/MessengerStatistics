import json
import os
from conversation_info import *


def get_full_name():
    """Get full name of Messenger user"""
    # Read autofill_information.json file
    if os.path.exists("messages/autofill_information.json"):
        with open("messages/autofill_information.json", "r") as autofill_file:
            # Load json file
            autofill_information = json.load(autofill_file)
            # Get full name
            full_name = autofill_information["autofill_information_v2"]["FULL_NAME"][0]
            return full_name
    else:
        print("File autofill_information.json does not exist.")
        return None

def get_nb_conversations(directory):
    """Get number of conversations"""
    # Go into inbox folder
    directory = directory + "/inbox"
    # Read inbox folder
    inbox_folder = os.listdir(directory)
    # Get number of conversations
    nb_conversations = len(inbox_folder)
    return nb_conversations

def get_nb_total_messages_sent(directory: str, year = None, month = None):
    """Get number of messages sent by user"""
    # Get full name of Messenger user
    user = get_full_name()
    # Go into inbox folder
    directory = directory + "/inbox"
    # Read inbox folder
    inbox_folder = os.listdir(directory)
    nb_messages = 0
    # Run over conversations
    for conversation_folder in inbox_folder:
        path = directory + "/" + conversation_folder
        nb_messages += get_nb_messages_sent_by_user(path, user, year, month)
    return nb_messages

def get_nb_total_messages_received(directory: str, year = None, month = None):
    """Get number of messages received by user"""
    # Get full name of Messenger user
    user = get_full_name()
    # Go into inbox folder
    directory = directory + "/inbox"
    # Read inbox folder
    inbox_folder = os.listdir(directory)
    nb_messages = 0
    # Run over conversations
    for conversation_folder in inbox_folder:
        path = directory + "/" + conversation_folder
        nb_messages += get_nb_messages_received_by_user(path, user, year, month)
    return nb_messages

def get_nb_total_messages(directory: str, year = None, month = None):
    """Get number of total messages sent and received by user"""
    # Get number of messages sent
    nb_messages_sent = get_nb_total_messages_sent(directory, year, month)
    # Get number of messages received
    nb_messages_received = get_nb_total_messages_received(directory, year, month)
    # Get number of total messages
    nb_messages = nb_messages_sent + nb_messages_received
    return nb_messages

def nb_total_messages_by_month_year(directory: str):
    """Get number of total messages sent and received by user by year"""
    dict = {}
    for year in range(2010, 2024):
        for month in range(1, 13):
            nb_messages_sent = get_nb_total_messages_sent(directory, year, month)
            nb_messages_received = get_nb_total_messages_received(directory, year, month)
            nb_messages = nb_messages_sent + nb_messages_received
            if nb_messages != 0 and str(year) not in dict:
                dict[str(year)] = {}
            if nb_messages != 0:
                dict[str(year)][str(month)] = {"nb_messages": nb_messages, "nb_messages_sent": nb_messages_sent, "nb_messages_received": nb_messages_received}
    return dict

def get_nb_avg_messages_sent(directory: str):
    """Get average number of messages sent by user"""
    # Get number of conversations
    nb_conversations = get_nb_conversations(directory)
    # Get number of messages sent
    nb_messages_sent = get_nb_total_messages_sent(directory)
    # Get average number of messages sent
    avg_messages_sent = nb_messages_sent / nb_conversations
    return avg_messages_sent

def get_nb_avg_messages_received(directory: str):
    """Get average number of messages received by user"""
    # Get number of conversations
    nb_conversations = get_nb_conversations(directory)
    # Get number of messages received
    nb_messages_received = get_nb_total_messages_received(directory)
    # Get average number of messages received
    avg_messages_received = nb_messages_received / nb_conversations
    return avg_messages_received

def get_nb_avg_messages(directory: str):
    """Get average number of messages per conversation"""
    # Get number of conversations
    nb_conversations = get_nb_conversations(directory)
    # Get number of total messages
    nb_messages = get_nb_total_messages(directory)
    # Get average number of total messages
    avg_messages = nb_messages / nb_conversations
    return avg_messages

def add_activity_per_day(activity_per_day: dict, activity_per_day_conversation: dict):
    """Add activity per day of conversation to activity per day"""
    for day in activity_per_day_conversation.keys():
        if day in activity_per_day:
            activity_per_day[day] += activity_per_day_conversation[day]
        else:
            activity_per_day[day] = activity_per_day_conversation[day]
    return activity_per_day

def get_activity_per_day(directory: str):
    """Get activity per day"""
    user = get_full_name()
    # Go into inbox folder
    directory = directory + "/inbox"
    # Read inbox folder
    inbox_folder = os.listdir(directory)
    # Create dictionary to store activity per day
    activity_per_day = {}
    # Run over conversations
    for conversation_folder in inbox_folder:
        path = directory + "/" + conversation_folder
        # Get activity per day for conversation
        activity_per_day_conversation = get_repartition_messages_day(path, user)
        # Add activity per day for conversation to activity per day
        activity_per_day = add_activity_per_day(activity_per_day, activity_per_day_conversation)
    return activity_per_day

def get_first_message_date(directory: str):
    # Go into inbox folder
    directory = directory + "/inbox"
    # Read inbox folder
    inbox_folder = os.listdir(directory)
    # First date
    first_date = datetime.now()
    # Run over conversations
    for conversation_folder in inbox_folder:
        path = directory + "/" + conversation_folder
        # Get first date message in conversation
        date = get_date_first_message(path)
        # If date is earlier than first date, update first date
        if date < first_date:
            first_date = date
    return first_date

def count_number_days_between_date(start_date: datetime, end_date: datetime):
    """Count number of days between two dates"""
    # Count number of days between two dates
    delta = end_date - start_date
    return delta.days

def store_dict_in_json(dict: dict, path: str):
    """Store dictionary in json file"""
    with open(path, 'w') as fp:
        json.dump(dict, fp)

def create_dict_global(directory):
    """Create dictionary of global stats"""
    # Create dictionary of global stats
    stats = {}
    # Stats about user
    user_stats = {}
    user_stats["name"] = get_full_name()
    user_stats["first_message"] = get_first_message_date(directory)
    user_stats["nb_conversations"] = get_nb_conversations(directory)
    user_stats["nb_total_messages"] = get_nb_total_messages(directory)
    user_stats["nb_avg_messages_sent_per_conversation"] = get_nb_avg_messages_sent(directory)
    user_stats["nb_avg_messages_received_per_conversation"] = get_nb_avg_messages_received(directory)
    user_stats["nb_avg_messages_per_conversation"] = get_nb_avg_messages(directory)
    user_stats["nb_avg_messages_per_day"] = user_stats["nb_total_messages"] / count_number_days_between_date(user_stats["first_message"], datetime.now())
    user_stats["activity_per_day"] = get_activity_per_day(directory)
    user_stats["activity_per_month_year"] = nb_total_messages_by_month_year(directory)
    user_stats["first_message"] = user_stats["first_message"].strftime("%d/%m/%Y")
    # Add user stats to global stats
    stats["user"] = user_stats

    # Stats about conversations
    conversations_stats = {}
    directory = directory + "/inbox"
    inbox_folder = os.listdir(directory)
    for conversation_folder in inbox_folder:
        # Create a conversation dictionary
        conversation = get_dict_conv(directory + "/" + conversation_folder, user_stats["name"])
        # Add conversation to conversations stats
        conversations_stats[conversation["title"]] = conversation
    # Add conversation to global stats
    stats["conversations"] = conversations_stats
    return stats

def get_most_active_conversation(dictionary: dict):
    """Get the top (num = 10 by default) most active single conversations"""
    # Sort dictionary by number of messages
    sorted_dict = sorted(dictionary["conversations"], key=lambda x: x[1]["nb_messages"], reverse=True)
    return sorted_dict

def get_most_active_single_conversation(dictionary: dict, num = 10):
    """Get the top (num = 10 by default) most active single conversations"""
    # Sort dictionary by number of messages
    sorted_dict = sorted(dictionary["conversations"].items(), key=lambda x: x[1]['nb_messages'], reverse=True)
    # Get the top (num = 10 by default) most active single conversations
    filtered_single_conv = [item for item in sorted_dict if len(item[1]["participants"]) == 2]
    # Return the top (num = 10 by default) most active single conversations
    if len(filtered_single_conv) < num:
        return filtered_single_conv
    else:
        return filtered_single_conv[:num]

def get_most_active_group_conversation(dictionary: dict, num = 10):
    """Get the top (num = 10 by default) most active group conversations"""
    # Sort dictionary by number of messages
    sorted_dict = sorted(dictionary["conversations"].items(), key=lambda x: x[1]['nb_messages'], reverse=True)
    # Get the top (num = 10 by default) most active group conversations
    filtered_group_conv = [item for item in sorted_dict if len(item[1]["participants"]) > 2]
    # Return the top (num = 10 by default) most active group conversations
    if len(filtered_group_conv) < num:
        return filtered_group_conv
    else:
        return filtered_group_conv[:num]
