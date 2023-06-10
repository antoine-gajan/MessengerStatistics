from message_info import *


def get_participants(conversation_directory):
    """Get name of participants in conversation"""
    name_receivers = []
    # Read message_1.json file
    with open(conversation_directory + "/" + "message_1.json", "r") as messages_file:
        # Load json file
        messages = json.load(messages_file)
        # Get name of receiver
        participants = messages["participants"]
        for participant in participants:
            name_receivers.append(participant["name"])
        return name_receivers

def get_number_of_participants(participants):
    """Get number of participants in conversation"""
    return len(participants)

def is_group_conversation(participants):
    """Check if conversation is group conversation"""
    if get_number_of_participants(participants) > 2:
        return True
    else:
        return False

def get_other_participants(list_participants, user):
    """Get name of other participants in conversation"""
    # Get name of other participants
    other_participants = []
    for participant in list_participants:
        if participant != user:
            other_participants.append(participant)
    return other_participants


def get_conversation_name(conversation_directory):
    """Get name of conversation"""
    with open(conversation_directory + "/message_1.json", "r") as messages_file:
        # Load json file
        messages = json.load(messages_file)
        return messages["title"]

def get_nb_messages_sent_by_user(conversation_directory, user, year = None, month = None):
    """Get number of messages sent by user in conversation"""
    # Get full name of Messenger user
    # Go to directory of conversation and read message_1.json file
    with open(conversation_directory + "/message_1.json", "r") as messages_file:
        # Load json file
        messages = json.load(messages_file)
        # Get number of messages sent
        nb_messages_sent = 0
        for message in messages["messages"]:
            date = get_date(message)
            if message["sender_name"] == user:
                if (year is None or date.year == year) and (month is None or date.month == month):
                    nb_messages_sent += 1
        return nb_messages_sent

def get_nb_messages_received_by_user(conversation_directory, user, year = None, month = None):
    """Get number of messages received by user in conversation"""
    # Go to directory of conversation and read message_1.json file
    with open(conversation_directory + "/message_1.json", "r") as messages_file:
        # Load json file
        messages = json.load(messages_file)
        # Get number of messages received
        nb_messages_received = 0
        for message in messages["messages"]:
            date = get_date(message)
            if message["sender_name"] != user:
                if (year is None or date.year == year) and (month is None or date.month == month) :
                    nb_messages_received += 1
        return nb_messages_received

def get_nb_messages(conversation_directory, user, year = None, month = None):
    """Get number of messages sent and received by user in conversation"""
    # Get number of messages sent
    nb_messages_sent = get_nb_messages_sent_by_user(conversation_directory, user, year, month)
    # Get number of messages received
    nb_messages_received = get_nb_messages_received_by_user(conversation_directory, user, year, month)
    return nb_messages_sent + nb_messages_received

def get_avg_length_messages_sent(conversation_directory, user):
    """Get average length of messages sent by user in conversation"""
    # Go to directory of conversation and read message_1.json file
    with open(conversation_directory + "/message_1.json", "r") as messages_file:
        # Load json file
        messages = json.load(messages_file)
        # Get average length of messages sent
        nb_messages_sent = 0
        total_length = 0
        for message in messages["messages"]:
            if message["sender_name"] == user and "content" in message.keys():
                nb_messages_sent += 1
                total_length += len(message["content"])
        if nb_messages_sent == 0:
            return 0
        return total_length / nb_messages_sent

def get_nb_reactions_given(conversation_directory, user):
    """Get number of reactions given by user in conversation"""
    # Go to directory of conversation and read message_1.json file
    with open(conversation_directory + "/message_1.json", "r") as messages_file:
        # Load json file
        messages = json.load(messages_file)
        # Get number of reactions given
        nb_reactions_given = 0
        for message in messages["messages"]:
            if message["sender_name"] == user and "content" in message.keys():
                nb_reactions_given += get_nb_reactions(message["content"])
    return nb_reactions_given

def get_nb_reactions_received(conversation_directory, user):
    """Get number of reactions received by user in conversation"""
    # Go to directory of conversation and read message_1.json file
    with open(conversation_directory + "/message_1.json", "r") as messages_file:
        # Load json file
        messages = json.load(messages_file)
        # Get number of reactions received
        nb_reactions_received = 0
        for message in messages["messages"]:
            if message["sender_name"] != user:
                nb_reactions_received += get_nb_reactions(message)
    return nb_reactions_received

def get_repartition_messages_day(conversation_directory, user):
    """Get repartition of messages sent by user in conversation per day"""
    # Go to directory of conversation and read message_1.json file
    with open(conversation_directory + "/message_1.json", "r") as messages_file:
        # Load json file
        messages = json.load(messages_file)
        # Get repartition of messages per day
        repartition_messages_day = {"Monday": 0, "Tuesday": 0, "Wednesday": 0, "Thursday": 0, "Friday": 0, "Saturday": 0, "Sunday": 0}
        for mess in messages["messages"]:
            if mess["sender_name"] == user:
                date = get_date(mess)
                day = get_day_from_date(date)
                repartition_messages_day[day] += 1
        return repartition_messages_day

def get_date_first_message(conversation_directory):
    """Get date of first message in conversation"""
    # Go to directory of conversation and read message_1.json file
    with open(conversation_directory + "/message_1.json", "r") as messages_file:
        # Load json file
        messages = json.load(messages_file)
        # Get date of first message
        first_message = messages["messages"][-1]
        return get_date(first_message)

def get_dict_conv(conversation_folder: str, name: str):
    # Create a conversation dictionary
    conversation = {}
    # Get participants
    participants = get_participants(conversation_folder)
    conversation["participants"] = participants
    # Get title
    conversation["title"] = get_conversation_name(conversation_folder)
    # Get number of messages sent
    nb_messages_sent = get_nb_messages_sent_by_user(conversation_folder, name)
    conversation["nb_messages_sent"] = nb_messages_sent
    # Get number of messages received
    nb_messages_received = get_nb_messages_received_by_user(conversation_folder, name)
    conversation["nb_messages_received"] = nb_messages_received
    # Get number of messages
    conversation["nb_messages"] = nb_messages_sent + nb_messages_received
    # Get average number of messages sent
    avg_messages_sent = get_avg_length_messages_sent(conversation_folder, name)
    conversation["avg_messages_sent"] = avg_messages_sent
    # Get number of reactions
    nb_reactions_given = get_nb_reactions_given(conversation_folder, name)
    conversation["nb_reactions_given"] = nb_reactions_given
    # Get number of reactions received
    nb_reactions_received = get_nb_reactions_received(conversation_folder, name)
    conversation["nb_reactions_received"] = nb_reactions_received
    return conversation