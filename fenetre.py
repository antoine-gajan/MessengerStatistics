import json
import os
import tkinter
from tkinter import filedialog, TOP
import global_info
import graph

class MessengerStatistics (tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)
        self.title("Messenger statistics")
        self.geometry("1000x800")
        self.labels = []
        self.create_menu()

    def create_menu(self):
        """Crée le menu de la fenêtre"""
        menu_bar = tkinter.Menu(self)
        # Premier sous-menu
        menu1 = tkinter.Menu(menu_bar, tearoff = 0)
        menu1.add_command(label = "Ouvrir un fichier", command = self.open_file)
        menu1.add_command(label = "Ouvrir un dossier", command = self.open_folder)
        menu1.add_command(label = "Quitter", command = self.destroy)
        menu_bar.add_cascade(label = "Fichier", menu = menu1)

        # Deuxième sous-menu
        menu2 = tkinter.Menu(menu_bar, tearoff = 0)
        menu2.add("command", label = "Général", command = lambda: self.show_global_stats())
        menu2.add_command(label = "Messages par jour", command = lambda: self.show_messages_by_day())
        menu2.add_command(label = "Messages par mois", command = lambda: self.show_messages_by_month())
        menu2.add_command(label = "Messages par année", command = lambda: self.show_messages_by_year())
        menu2.add_command(label = "Conversations les plus actives", command = lambda: self.show_most_active_conversation())
        menu_bar.add_cascade(label = "Graphiques", menu = menu2)
        # Configuration du menu
        self.config(menu = menu_bar)


    def get_username(self):
        """Récupère le nom d'utilisateur"""
        return self.dict_messages["user"]["name"]

    def open_folder(self):
        """Ouvre un dossier et crée le dictionnaire des messages"""
        folder = filedialog.askdirectory()
        print(folder)
        self.create_dict_messages(folder)

    def open_file(self):
        """Ouvre un fichier et crée le dictionnaire des messages"""
        file = filedialog.askopenfilename(title = "Select a file", filetypes = (("json files", "*.json"), ("all files", "*.*")))
        print(file)
        self.set_dict_messages(file)

    def create_dict_messages(self, folder: str):
        """Crée le dictionnaire des messages à partir d'un dossier"""
        self.dict_messages = global_info.create_dict_global(folder)
        print("Dict messages set")
        self.create_images()

    def set_dict_messages(self, file: str):
        """Crée le dictionnaire des messages à partir d'un fichier"""
        self.dict_messages = json.load(open(file, "r"))
        print("Dict messages set")
        self.create_images()

    def create_images(self):
        """Crée les images des graphiques"""
        print(self.dict_messages)
        # Create images directory
        os.makedirs("images", exist_ok=True)
        graph.draw_messages_by_day(self.dict_messages)
        graph.draw_messages_by_month(self.dict_messages)
        graph.draw_messages_by_year(self.dict_messages)
        graph.draw_most_active_conversation(self.dict_messages, 10, True, True)

    def show_image(self, image_path: str):
        """Affiche une image dont le chemin est passé en paramètre"""
        self.image = tkinter.PhotoImage(file = image_path)
        label = tkinter.Label(self, image = self.image)
        self.labels.append(label)
        label.pack()

    def show_global_stats(self):
        """Affiche les statistiques générales"""
        # Supprimer les anciens labels
        self.delete_labels()
        # Titre général
        label = tkinter.Label(self, text = "Statistiques générales de " + self.get_username(), font = ("Arial", 20, "bold"))
        self.labels.append(label)
        label.pack()
        # Informations du compte
        label_info_compte = tkinter.Label(self, text = "Informations du compte", font = ("Arial", 16, "bold"))
        self.labels.append(label_info_compte)
        label_info_compte.pack(padx = 20, pady=20, side= TOP, anchor="w")
        label_nom = tkinter.Label(self, text = "Nom: " + self.get_username())
        self.labels.append(label_nom)
        label_nom.pack(pady=10, side= TOP, anchor="w")
        label_first_message = tkinter.Label(self, text = "Premier message: " + self.dict_messages["user"]["first_message"])
        self.labels.append(label_first_message)
        label_first_message.pack(pady=10, side= TOP, anchor="w")
        label_nb_conversations = tkinter.Label(self, text = "Nombre de conversations: " + str(self.dict_messages["user"]["nb_conversations"]))
        self.labels.append(label_nb_conversations)
        label_nb_conversations.pack(pady=10, side= TOP, anchor="w")
        label_nb_messages = tkinter.Label(self, text = "Nombre de messages: " + str(self.dict_messages["user"]["nb_total_messages"]))
        self.labels.append(label_nb_messages)
        label_nb_messages.pack(pady=10, side= TOP, anchor="w")
        # Statistiques par conversation
        label_subtitle_stats = tkinter.Label(self, text = "Statistiques par conversation", font = ("Arial", 16, "bold"))
        self.labels.append(label_subtitle_stats)
        label_subtitle_stats.pack(padx = 20, pady=20, side= TOP, anchor="w")
        label_nb_avg_messages_per_conversation = tkinter.Label(self, text = "Nombre moyen de messages par conversation: " + str(self.dict_messages["user"]["nb_avg_messages_per_conversation"]))
        self.labels.append(label_nb_avg_messages_per_conversation)
        label_nb_avg_messages_per_conversation.pack(pady=10, side= TOP, anchor="w")
        label_nb_avg_messages_sent_per_conversation = tkinter.Label(self, text = "Nombre moyen de messages envoyés par conversation: " + str(self.dict_messages["user"]["nb_avg_messages_sent_per_conversation"]))
        self.labels.append(label_nb_avg_messages_sent_per_conversation)
        label_nb_avg_messages_sent_per_conversation.pack(pady=10, side= TOP, anchor="w")
        label_nb_avg_messages_received_per_conversation = tkinter.Label(self, text = "Nombre moyen de messages reçus par conversation: " + str(self.dict_messages["user"]["nb_avg_messages_received_per_conversation"]))
        self.labels.append(label_nb_avg_messages_received_per_conversation)
        label_nb_avg_messages_received_per_conversation.pack(pady=10, side= TOP, anchor="w")
        label_nb_avg_messages_per_day = tkinter.Label(self, text = "Nombre moyen de messages par jour: " + str(self.dict_messages["user"]["nb_avg_messages_per_day"]))
        self.labels.append(label_nb_avg_messages_per_day)
        label_nb_avg_messages_per_day.pack(pady=10, side= TOP, anchor="w")

    def show_messages_by_day(self):
        """Fonction qui affiche le graphique des messages par jour"""
        self.delete_labels()
        label = tkinter.Label(self, text = "Messages par jour", font = ("Arial", 20, "bold"))
        self.labels.append(label)
        label.pack()
        self.show_image("images/messages_by_day.png")

    def show_messages_by_year(self):
        """Fonction qui affiche le graphique des messages par année"""
        self.delete_labels()
        label = tkinter.Label(self, text = "Messages par année", font = ("Arial", 20, "bold"))
        self.labels.append(label)
        label.pack()
        self.show_image("images/messages_by_year.png")

    def show_messages_by_month(self):
        """Fonction qui affiche le graphique des messages par mois"""
        self.delete_labels()
        label = tkinter.Label(self, text = "Messages par mois", font = ("Arial", 20, "bold"))
        self.labels.append(label)
        label.pack()
        self.show_image("images/messages_par_mois.png")

    def show_most_active_conversation(self):
        """Fonction qui affiche le graphique des conversations les plus actives"""
        self.delete_labels()
        label = tkinter.Label(self, text = "Conversations les plus actives", font = ("Arial", 20, "bold"))
        self.labels.append(label)
        label.pack()
        self.show_image("images/most_active_conversation.png")

    def delete_labels(self):
        """Fonction qui supprime tous les labels de la fenêtre"""
        # Supprimer tous les labels
        for label in self.labels:
            label.destroy()
            label.pack_forget()
            label.destroy()
        # Nettoyer la liste
        self.labels.clear()
