import tkinter as tk
import hashlib
import math
from tkinter import messagebox
import numpy as np

class LoginApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MathGame")
        self.geometry("1280x700")
        self.iconbitmap("Mathgame.ico")
        self.logo_image = tk.PhotoImage(file="images.png")  # Chemin direct de l'image
        self.minsize(480, 360)
        self.config(bg='blue')
        self.image_label = tk.Label(self, image=self.logo_image, bg='blue')  # l'image
        self.label_id = tk.Label(self, text="Entrer Id:", font=("Courier", 20), bg='blue', fg='white')
        self.entry_id = tk.Entry(self, font=("Courier", 20) , )
        self.button_login = tk.Button(self, text="Connexion", command=self.login, font=("Courier", 20))
        self.button_inscrire = tk.Button(self, text="Inscrire", command=self.inscrire, font=("Courier", 20))
        self.nom_label = tk.Label(self, text="Nom d'utilisateur :", font=("Courier", 20), bg='blue', fg='white')
        self.nom_entry = tk.Entry(self, font=("Courier", 20))
        self.id_label = tk.Label(self, text="ID d'utilisateur :", font=("Courier", 20), bg='blue', fg='white')
        self.id_entry = tk.Entry(self, font=("Courier", 20))
        self.start_button = tk.Button(self, text="Start", font=("Courier", 20),command=self.start_game)
        self.classement_button = tk.Button(self  , text="Classement",command=self.afficher_classement, font=("courier",20))
        self.logout_button = tk.Button(self, text="Logout", command=self.logout,font=("Courier", 20))
        self.retour_button_inscription = tk.Button(self, text="Retour",command=self.retour_inscription, font = ("Courier", 20))
        self.inscrire_button_final = tk.Button(self,text = "Register" ,command=self.enregistrer_utilisateur , font = ("courier" , 20))
        self.return_button_menu_joueur = tk.Button(self,text="Retour" ,command=self.retour_menu_joueur, font = ("courier" , 20))
        self.classement_label = None
        #affichage des widgets sur menu principale
        self.image_label.pack()
        self.label_id.pack(pady=10)
        self.entry_id.pack(pady=10)
        self.button_login.pack(pady=10)
        self.button_inscrire.pack(pady=10)
        self.id_utilisateur = None 
    def login(self):
        # Récupérer l'ID saisi par l'utilisateur
        id_utilisateur = self.entry_id.get()
        self.entry_id.delete(0, tk.END)

        # Vérifier si l'ID est vide
        if not id_utilisateur:
            self.afficher_message("Veuillez saisir un ID utilisateur.")
            return

        # Vérifier si l'ID existe dans le fichier utilisateurs.txt
        if self.verifier_id_existant(id_utilisateur):
            self.id_utilisateur = id_utilisateur 
            self.afficher_message("Connexion réussie")
            self.effacer_widgets_menu_principale()
            self.afficher_menu_joueur()
        else:
            self.afficher_message("Erreur de connexion. ID utilisateur incorrect.")

    def verifier_id_existant(self, id_utilisateur):
        # Crypter l'ID entré par l'utilisateur
        id_crypte_entre = self.crypter_id(id_utilisateur)

        # Vérifier si l'ID crypté existe dans le fichier utilisateurs.txt
        with open("utilisateurs.txt", "r") as file:
            for ligne in file:
                id_crypte_fichier = ligne.split(":")[0]
                if id_crypte_fichier == id_crypte_entre:
                    return True
        return False
    def inscrire(self):
        self.afficher_menu_inscription()
    def afficher_menu_inscription(self):
        self.effacer_widgets_menu_principale()
        self.nom_label.pack(pady=10)
        self.nom_entry.pack(pady=10)
        self.id_label.pack(pady=10)
        self.id_entry.pack(pady=10)
        self.inscrire_button_final.pack(pady=10)
        self.retour_button_inscription.pack(pady=10)
    def afficher_menu_principale(self):
        # afficher menu principale packs
        self.image_label.pack()
        self.label_id.pack(pady=10)
        self.entry_id.pack(pady=10)
        self.button_login.pack(pady=10)effacer_widgets_menu_principale()
        self.start_button.pack(pady=10)
        self.classement_button.pack(pady=10)
        self.logout_button.pack(pady=10)
    def  effacer_widgets_menu_principale(self):
        self.label_id.pack_forget()
        self.entry_id.pack_forget()
        self.button_login.pack_forget()
        self.button_inscrire.pack_forget()
    def effacer_widgets_menu_inscription(self):
        self.nom_label.pack_forget()
        self.nom_entry.pack_forget()
        self.id_label.pack_forget()
        self.id_entry.pack_forget()
        self.inscrire_button_final.pack_forget()
        self.retour_button_inscription.pack_forget()
    def effacer_widget_menu_joueur(self):
        self.start_button.pack_forget()
        self.classement_button.pack_forget()
        self.logout_button.pack_forget()
    def logout(self):
        self.effacer_widget_menu_joueur()
        self.afficher_menu_principale()

    def retour_inscription(self):
        self.effacer_widgets_menu_inscription()
        self.afficher_menu_principale()

    def enregistrer_utilisateur(self):
        # Récupérer les données saisies par l'utilisateur
        nom_utilisateur = self.nom_entry.get()
        id_utilisateur = self.id_entry.get()
        self.nom_entry.delete(0, tk.END)
        self.id_entry.delete(0, tk.END)

        # Vérifier si les champs sont vides
        if not nom_utilisateur or not id_utilisateur:
            self.afficher_message("Veuillez remplir tous les champs.")
            return

        # Crypter l'ID (vous pouvez utiliser une méthode de cryptage appropriée)
        id_crypte = self.crypter_id(id_utilisateur)

        # Vérifier si l'ID crypté est déjà utilisé
        if self.verifier_id_unique(id_crypte):
            self.afficher_message("Cet ID est déjà utilisé. Veuillez choisir un autre.")
            return

        # Enregistrer les données dans un fichier texte
        with open("utilisateurs.txt", "a") as file:
            file.write(f"{id_crypte}:{nom_utilisateur}:0\n")

        self.afficher_message("Inscription réussie. Utilisateur enregistré avec succès !")

    def verifier_id_unique(self, id_crypte):
        # Vérifier si l'ID crypté est déjà utilisé en lisant le fichier texte
        with open("utilisateurs.txt", "r") as file:
            for ligne in file:
                if ligne.startswith(id_crypte):
                    return True
        return False

    def crypter_id(self, id_utilisateur):
        # Utiliser hashlib pour hacher l'ID de l'utilisateur
        id_crypte = hashlib.sha256(id_utilisateur.encode()).hexdigest()
        return id_crypte

    def afficher_message(self, message):
        self.message_label = tk.Label(self, text=message, font=("Courier", 14), bg='blue', fg='white')
        self.message_label.pack()
        # Effacer le message après 5 secondes
        self.after(1000, self.effacer_message)

    def effacer_message(self):
        self.message_label.pack_forget()
    def logout(self):
        self.effacer_widget_menu_joueur()
        self.afficher_menu_principale()

    def afficher_classement(self):
        self.effacer_widget_menu_joueur()  # Effacer tous les widgets du menu joueur

        # Récupérer les scores des utilisateurs à partir du fichier utilisateurs.txt
        scores_utilisateurs = []

        utilisateur_actuel = None
        score_utilisateur_actuel = None

        # Ouverture du fichier utilisateurs.txt
        fichier = open("utilisateurs.txt", "r")
        lignes = fichier.readlines()
        fichier.close()

        for ligne in lignes:
            # Diviser la ligne en utilisant ':' comme séparateur
            elements = ligne.strip().split(":")

            # S'assurer qu'il y a au moins 3 éléments dans la liste
            if len(elements) == 3:
                id_utilisateur, nom_utilisateur, score_utilisateur = elements
                score_utilisateur = int(score_utilisateur)
                scores_utilisateurs.append((nom_utilisateur, score_utilisateur))

                # Si l'utilisateur est connecté, récupérer son score
                if id_utilisateur == self.id_entry.get():
                    utilisateur_actuel = nom_utilisateur
                    score_utilisateur_actuel = score_utilisateur

        # Trier les scores des utilisateurs par ordre décroissant
        scores_utilisateurs.sort(key=lambda x: x[1], reverse=True)

        # Construire les classements pour les 10 premiers scores
        classement = "Top 10 des scores :\n\n"
        for i, (nom_utilisateur, score_utilisateur) in enumerate(scores_utilisateurs[:10]):
            # Ajouter des espaces pour aligner les noms d'utilisateur et les scores
            classement += f"{i + 1}. {nom_utilisateur.ljust(20)} : {str(score_utilisateur).rjust(10)}\n"

        # Inclure le score de l'utilisateur actuel dans le classement
        if utilisateur_actuel is not None and score_utilisateur_actuel is not None:
            classement += f"\nVotre score : {utilisateur_actuel.ljust(20)} : {str(score_utilisateur_actuel).rjust(10)}"

        # Afficher les classements dans une fenêtre ou une étiquette
        self.classement_label = tk.Label(self, text=classement, font=("Courier", 20),bg="lightblue")  # Couleur de fond personnalisée
        self.classement_label.pack()
        self.return_button_menu_joueur.pack(pady=10)

    def retour_menu_joueur(self):
        self.classement_label.pack_forget()
        self.return_button_menu_joueur.pack_forget()
        self.afficher_menu_joueur()

    def start_game(self):
        self.effacer_widget_menu_joueur()
        self.math_game = MathGame(self,self.id_utilisateur)


    def mettre_a_jour_score_utilisateur(self, id_utilisateur):
        id_crypte = self.crypter_id(id_utilisateur)
        # Lire les données des utilisateurs depuis le fichier
        utilisateurs = []
        with open("utilisateurs.txt", "r") as fichier:
            for ligne in fichier:
                id_user, nom_user, score = ligne.strip().split(":")
                if id_user == id_crypte:
                    score = str(int(score) + 1)

                utilisateurs.append((id_user, nom_user, score))

        # Écrire les nouvelles données dans le fichier en effaçant d'abord le contenu existant
        with open("utilisateurs.txt", "w") as fichier:
            for utilisateur in utilisateurs:
                fichier.write(f"{utilisateur[0]}:{utilisateur[1]}:{utilisateur[2]}\n")

class MathGame:
    def __init__(self, root,id_utilisateur):
        self.root = root
        self.root.title("MathGame")
        self.id_utilisateur = id_utilisateur

        self.mode_options = ["Quadratic Equation", "Linear Equation", "Simple Calculations"]
        self.selected_mode = tk.StringVar()
        self.selected_mode.set(self.mode_options[0])

        self.difficulty_options = ["Easy", "Medium", "Hard"]
        self.selected_difficulty = tk.StringVar()
        self.selected_difficulty.set(self.difficulty_options[0])

        self.mode_menu = tk.OptionMenu(self.root, self.selected_mode, *self.mode_options)
        self.mode_menu.pack(pady=10)

        self.difficulty_menu = tk.OptionMenu(self.root, self.selected_difficulty, *self.difficulty_options)
        self.difficulty_menu.pack(pady=10)

        self.start_button = tk.Button(self.root, text="Start", command=self.start_game)
        self.start_button.pack(pady=10)

        self.score_label = tk.Label(self.root, text="Score: 0", font=("Arial", 16))
        self.timer_label = tk.Label(self.root, text="Time left: 60", font=("Arial", 16))

        self.equation_label = tk.Label(self.root, text="", font=("Arial", 24))
        self.answer_entry1 = tk.Entry(self.root, font=("Arial", 18))
        self.answer_entry2 = tk.Entry(self.root, font=("Arial", 18))
        self.submit_button = tk.Button(self.root, text="Submit", command=self.check_answer)
        self.bind_enter_key()
        self.replay_button = tk.Button(self.root, text="Replay", command=self.replay_game)
        self.current_score = 0
        self.delta = 0

    def bind_enter_key(self):
        # Lier la touche "Entrée" à la fonction check_answer()
        self.root.bind('<Return>', lambda event: self.check_answer())

    def generate_equation(self, mode):
        self.difficulty = self.selected_difficulty.get()
        if mode == "Quadratic Equation":
            if self.difficulty == "Easy":
                operands = np.random.randint(1, 11, size=3)
            elif self.difficulty == "Medium":
                operands = np.random.randint(1, 101, size=3)
            else:
                operands = np.random.randint(1, 1001, size=3)

            a, b, c = operands
            equation = f"{a}x² + {b}x + {c}"
            self.delta = b ** 2 - 4 * a * c
            if self.delta < 0:
                return self.generate_equation(mode)
            elif self.delta > 0:
                x1 = (-b + math.sqrt(self.delta)) / (2 * a)
                x2 = (-b - math.sqrt(self.delta)) / (2 * a)
                result = (round(x1, 2), round(x2, 2))
                print(result)
                return equation, result
            else:
                x = -b / (2 * a)
                result = round(x, 2)
                print(result)
                return equation, result
        elif mode == "Linear Equation":
            if self.difficulty == "Easy":
                operands = np.random.randint(1, 11, size=2)
            elif self.difficulty == "Medium":
                operands = np.random.randint(1, 101, size=2)
            else:
                operands = np.random.randint(1, 1001, size=2)
            a, b = operands
            equation = f"{a}x + {b}"
            result = round((-b / a), 2)
            print(result)
            return equation, result
        elif mode == "Simple Calculations":
            num1 = np.random.randint(1, 10)
            num2 = np.random.randint(1, 10)
            operator = np.random.choice(["+", "-", "*", "/"])
            equation = f"{num1} {operator} {num2}"
            result = round(eval(equation), 2)
            print(result)
            return equation, result

    def start_game(self):
        if hasattr(self, '_timer_id'):
            self.root.after_cancel(self._timer_id)
            delattr(self, '_timer_id')

        mode = self.selected_mode.get()
        self.mode_menu.pack_forget()
        self.difficulty_menu.pack_forget()
        self.start_button.pack_forget()

        self.score_label.pack(pady=10)
        self.timer_label.pack(pady=10)

        self.equation_label.pack(pady=10)
        equation, result = self.generate_equation(mode)
        self.current_equation = equation
        self.current_result = result
        self.equation_label.config(text=equation)

        self.replay_button.pack_forget()
        self.submit_button.pack_forget() 

        if mode in ["Simple Calculations", "Linear Equation"]:
            self.answer_entry1.pack(pady=10)
            self.answer_entry2.pack_forget()
        else:
            if self.delta == 0:
                self.answer_entry2.pack(pady=10)
                self.answer_entry1.pack_forget()
            else:
                self.answer_entry1.pack(pady=10)
                self.answer_entry2.pack(pady=10)
        self.replay_button.pack(pady=10)
        self.submit_button.pack(pady=10)

        self.score = self.current_score
        if self.difficulty == "Easy":
            self.time_left = 30
        elif self.difficulty == "Medium":
            self.time_left = 60
        else:
            self.time_left = 90
        self.score_label.config(text=f"Score: {self.score}")
        self.timer_label.config(text=f"Time left: {self.time_left}")

        self.submit_button.config(state="normal")
        self.timer()
        

    def timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Time left: {self.time_left}")
            self._timer_id = self.root.after(1000, self.timer)  # Stocker l'ID du compte à rebours
        if self.time_left == 0:
            self.submit_button.config(state="disabled")
            messagebox.showinfo("Game Over", f"Your final score is {self.score}")

    def check_answer(self):
        mode = self.selected_mode.get()
        try:
            equation = self.current_equation  # Utilisez l'équation actuelle
            result = self.current_result  # Utilisez le résultat actuel

            self.equation_label.config(text=equation)

            if mode == "Simple Calculations" or mode == "Linear Equation":
                user_answer = float(self.answer_entry1.get())
                print("User answer:", user_answer)
                print("Expected answer:", result)
            else:
                if self.delta == 0:
                    user_answer = float(self.answer_entry2.get())
                    print("User answer:", user_answer)
                    print("Expected answer:", result)
                else:
                    user_answer1 = round(float(self.answer_entry1.get()), 2)
                    user_answer2 = round(float(self.answer_entry2.get()), 2)
                    user_answer = (user_answer1, user_answer2)
                    print("User answer:", user_answer)
                    print("Expected answer:", result)

            if isinstance(result, tuple):
                result_inverse = result[::-1]
                if user_answer == result or user_answer == result_inverse:
                    messagebox.showinfo("Correct", "You got it right!")
                    self.current_score += 1
                    app.mettre_a_jour_score_utilisateur(self.id_utilisateur)
                else:
                    messagebox.showerror("Incorrect", "Wrong answer!")
            else:
                if user_answer == result:
                    messagebox.showinfo("Correct", "You got it right!")
                    self.current_score += 1
                    app.mettre_a_jour_score_utilisateur(app.id_utilisateur)
                else:
                    messagebox.showerror("Incorrect", "Wrong answer!")

            self.score_label.config(text=f"Score: {self.score}")
            self.start_game()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers.")

    def replay_game(self):
        if hasattr(self, '_timer_id'):
            self.root.after_cancel(self._timer_id)  # Annuler le compte à rebours actuel
            delattr(self, '_timer_id')
        self.score = self.current_score
        if self.difficulty == "Easy":
            self.time_left = 30
        elif self.difficulty == "Medium":
            self.time_left = 60
        else:
            self.time_left = 90
        self.score_label.config(text=f"Score: {self.score}")
        self.timer_label.config(text=f"Time left: {self.time_left}")

        self.equation_label.config(text="")
        self.answer_entry1.delete(0, "end")
        self.answer_entry2.delete(0, "end")

        if self.selected_mode.get() in ["Quadratic Equation"]:
            if self.delta == 0:
                self.answer_entry2.pack(pady=10)
                self.answer_entry1.pack_forget()
            else:
                self.answer_entry1.pack(pady=10)
                self.answer_entry2.pack(pady=10)
        elif self.selected_mode.get() in ["Simple Calculations", "Linear Equation"]:
            self.answer_entry1.pack(pady=10)

        self.mode_menu.pack(pady=10)
        self.difficulty_menu.pack(pady=10)
        self.start_button.pack(pady=10)
        self.submit_button.pack_forget()
        self.replay_button.pack_forget()  # Cacher le bouton de rejouer


    

app = LoginApp()
app.mainloop()
