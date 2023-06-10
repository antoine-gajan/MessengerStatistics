from global_info import *
from graph import *

def main():
    # Create dict
    #dict_msg = create_dict_global("messages")
    # Store dict in json
    #store_dict_in_json(dict_msg, "global_stats.json")
    dict_msg = json.load(open("global_stats.json", "r"))
    # Draw graph
    draw_messages_by_day(dict_msg)
    draw_messages_by_month(dict_msg)
    draw_messages_by_year(dict_msg)
    draw_most_active_conversation(dict_msg, 10, True, True)

if __name__ == "__main__":
    main()