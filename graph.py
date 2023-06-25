import matplotlib.pyplot as plt
from global_info import *


def draw_messages_by_day(global_dict: dict, type: str = "bar"):
    """Draw graph of number of messages by day"""
    # Get activity per day
    activity_per_day = global_dict["user"]["activity_per_day"]

    # Get x and y values
    x = list(activity_per_day.keys())
    y = list(activity_per_day.values())
    mean_y = sum(y) / len(y)

    # Tracé
    if type == "bar":
        plt.bar(x, y, color="#3ED8C9")
        plt.plot(x, [mean_y for _ in range(len(x))], color="#D83E3E")
        plt.xticks(range(len(x)),
                   ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"])
        # Add values above each bar
        for i, j in zip(x, y):
            plt.text(i, j, j, ha='center')
        plt.xlabel("Jour")
        plt.ylabel("Nombre de messages")
    elif type == "pie":
        plt.pie(y, labels=x, autopct="%1.1f%%",
                colors=["#3ED8C9", "#3E9CD8", "#3E3ED8", "#9C3ED8", "#D83ED8", "#D83E9C", "#D83E3E"])


    # Draw graph
    plt.legend(["Moyenne", "Nombre de messages"])
    plt.title("Nombre de messages par jour")
    # Save image
    plt.savefig("images/messages_by_day.png")
    plt.close()

def draw_messages_by_month(global_dict: dict):
    """Draw graph of number of messages by month"""
    # Get activity per month
    activity_per_month = global_dict["user"]["activity_per_month_year"]

    # Get x and y values
    x = list(range(12))
    data = list(activity_per_month.values())

    # Initialize y
    y = {}
    # Initialize for each month
    for month in range(1, 13):
        y[str(month)] = 0
    # Add values
    for data_year in data:
        for month, data_month in data_year.items():
            y[month] += data_month["nb_messages"]
    # Convert to list
    y = list(y.values())

    # Tracé
    plt.bar(x, y, color="#3ED8C9")
    plt.plot(x, [sum(y) / len(y) for _ in range(len(x))], color="#D83E3E")

    plt.xticks(x,
               ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août",
                "Septembre", "Octobre", "Novembre", "Décembre"])
    # Add values above each bar
    for i, j in zip(x, y):
        plt.text(i, j, j, ha='center')
    plt.xlabel("Mois")
    plt.ylabel("Nombre de messages")

    # Draw graph
    plt.legend([f"Moyenne mensuelle({int(sum(y) / len(y))})", "Nombre de messages"])
    plt.title("Nombre de messages par mois")

    # Save figure
    plt.savefig("images/messages_par_mois.png")
    plt.close()

def draw_messages_by_year(global_dict: dict):
    """Draw graph of number of messages by year"""
    # Get activity per year
    activity_per_year = global_dict["user"]["activity_per_month_year"]

    # Get x and y values
    x = list(activity_per_year.keys())
    data = activity_per_year.values()

    y = {}

    for year, data_year in zip(x, data):
        y[year] = {
            'nb_messages': sum(month['nb_messages'] for month in data_year.values()),
            'nb_messages_sent': sum(month['nb_messages_sent'] for month in data_year.values()),
            'nb_messages_received': sum(month['nb_messages_received'] for month in data_year.values())
        }

    y1 = [y[year]['nb_messages_sent'] for year in y.keys()]
    y2 = [y[year]['nb_messages_received'] for year in y.keys()]

    # Tracé
    plt.bar(x, y1, color="#3ED8C9")
    # Add values above each bar
    for i, j in zip(x, y1):
        plt.text(i, j / 2, j, ha='center', va='center')

    plt.bar(x, y2, bottom=y1, color="#EDFF91")
    # Add values above each bar
    for i, j in zip(x, y2):
        plt.text(i, j / 2 + y1[x.index(i)], j, ha='center', va='center')

    plt.xticks(range(len(x)), x)
    # Draw graph
    plt.legend(["Messages envoyés", "Messages reçus"])
    plt.xlabel("Year")
    plt.ylabel("Number of messages")
    plt.title("Number of messages by year")
    # Save image
    plt.savefig("images/messages_by_year.png")
    plt.close()

def draw_most_active_conversation(global_dict: dict, nb: int = 10, single: bool = False, group: bool = False):
    """Draw graph of most active conversation"""
    # Get most active conversation
    most_active_conversation = []
    if single:
        for elt in get_most_active_single_conversation(global_dict, nb):
            most_active_conversation.append(elt)
    if group:
        for elt in get_most_active_group_conversation(global_dict, nb):
            most_active_conversation.append(elt)

    if group and single:
        # Sort the list
        most_active_conversation.sort(key=lambda x: x[1]["nb_messages"], reverse=True)

    # Get x and y values
    x = range(1, len(most_active_conversation) + 1)
    y = [conversation[1]["nb_messages"] for conversation in most_active_conversation]
    top_write_plot = [conversation[0].encode('iso-8859-1').decode('utf-8') for conversation in most_active_conversation]

    # Tracé
    plt.bar(x, y, color="#3ED8C9")
    # Add name of persons in each bar
    for i, j in zip(x, top_write_plot):
        plt.text(i, 50, j, ha='center', rotation=90, fontsize=8)
    # Add conversation names above each bar
    for i, j in zip(x, y):
        plt.text(i, j + 1, j, ha='center', va='center')

    # Customize plot
    plt.xlabel('Conversations')
    plt.ylabel('Number of Messages')
    plt.title('Most Active Conversations by Number of Messages')

    plt.savefig('images/most_active_conversation.png')
    plt.close()

