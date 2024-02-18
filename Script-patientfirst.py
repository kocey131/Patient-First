import csv              
import hashlib          
import random
import string
from tabulate import tabulate      


def hash_password(password):                                #Fonction pour hashé le mot de passe
    md5_hash = hashlib.md5()
    md5_hash.update(password.encode('utf-8'))
    return md5_hash.hexdigest()

def generate_password():                                    #Fonction pour generé le mot de passe avec une liste de charactére
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(8))
    return password

def generate_id(nom, prenom):                                #Contacténé le nom et le prénom pour former un ID
    prenom_minuscules = prenom.lower()
    premiere_lettre_prenom = prenom_minuscules[0]
    identifiant = premiere_lettre_prenom + nom.lower()
    return identifiant

def save_user():                                              #fonction pour enregistrer un utilisateur
    with open("utilisateurs.csv", mode="a", newline="") as f:
        writer = csv.writer(f, delimiter=",")
        print("Entrez les informations de l'utilisateur à enregistrer")
        nom = input("Entrez le nom : ")
        prenom = input("Entrez le prénom : ")
        type_account = "utilisateur"
        password_plain = generate_password()
        password_hashed = hash_password(password_plain)
        user_id = generate_id(nom, prenom)
        password_changed = "0"                                    #chaque nouveau compte on affecte 0 sur cette valeur pour changé le mot de passe lors de leur premiere connexion
        writer.writerow([nom, prenom, user_id, password_hashed, type_account, password_changed])          #ecrire les données dans la base de données du fichier csv
        print("Utilisateur enregistré avec succès!")
        print("L'ID est:", user_id)
        print("Le mot de passe temporaire est:", password_plain)
        print("Le type de compte est:", type_account)

def delete_user(user_id):                                                               #fonction pour supprimer un utilisateur/admin
    with open("utilisateurs.csv", mode="r") as f:
        users = list(csv.reader(f))

    for user in users:
        if user[2] == user_id:
            users.remove(user)
            print("Utilisateur supprimé avec succès.")
            break
    else:
        print("Utilisateur non trouvé.")

    with open("utilisateurs.csv", mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(users)

def login_user():                                                                   #Pour se connecter à l'interface, grace au if statements le programme reconnais le  type de comptes et redirige vers le menu approprié
    print("Veuillez entrer vos informations de connexion")
    user_id = input("ID : ")
    password = input("Mot de passe : ")

    with open("utilisateurs.csv", mode="r") as f:
        reader = csv.reader(f, delimiter=",")
        for row in reader:
            if row[2] == user_id:
                stored_password = row[3]
                password_changed = row[5]
                if hash_password(password) == stored_password:
                    type_account = row[4]
                    if type_account == "admin": 
                        if password_changed == "0":                                                     #verifié si le mot de passe n'as pas etait changé et prompt à l'utilisateur de le changé lors de sa premiere connexion 
                            print("Veuillez changer votre mot de passe")                                #(valablle aussi pour les admins car il sont crée par le superadmin et affecté un mot de passe provisoire) 
                            change_password(user_id)                                                            
                        elif password_changed == "1":
                            print("Connexion réussie, vous êtes super administrateur")              
                            admin_menu(user_id)
                            return
                    elif type_account == "sadmin":
                        print("Connexion réussie, vous etes superadminstrateur")
                        superadmin_menu(user_id)
                    elif type_account == "utilisateur":
                        if password_changed == "0":
                            print("Veuillez changer votre mot de passe")
                            change_password(user_id) 
                        elif password_changed == "1":
                            print("Connexion réussie")
                            user_menu(user_id)  
                        return
    print("ID ou mot de passe incorrects")

def display_user_information(user_id):                          #cette fonction nous affiche les informations de notre compte connecté(marche aussi si les admins veulent consulter les informations des  autres comptes)
    with open("utilisateurs.csv", 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            if row[2] == user_id:
                nom = row[0]
                prenom = row[1]
                identifiant = row[2]
                print("Les informations de l'utilisateur", user_id)
                print(f"Nom : {nom}")
                print(f"Prénom : {prenom}")
                print(f"ID : {identifiant}")
                break
        else:
            print("Utilisateur non trouvé")
def superadmin_menu(user_id):                                           #menu superadmin
    while True:
        print("Bienvenue! Que souhaitez-vous faire ?")
        print("1. Modifier mes informations")
        print("2. modifier mon mot de passe")
        print("3. Gérer les comptes utilisateurs")
        print("4. Gérer les admins")
        print("0. Déconnexion")

        choix = input("Sélectionnez une option : ")

        
        if choix == "1":
            modify_user_information(user_id)
        elif choix == "3":
            manage_user_accounts()
        elif choix == "2":
            change_password(user_id)
        elif choix == "4":
            manage_admin_accounts()
        elif choix == "0":
            print("Déconnexion réussie.")
            break
        else:
            print("Option invalide. Veuillez sélectionner une option valide.")
    
def admin_menu(user_id):                                                    #menu admin
    while True:
        print("Bienvenue! Que souhaitez-vous faire ?")
        print("1. Modifier mes informations")
        print("2. modifier mon mot de passe")
        print("3. Gérer les comptes utilisateurs")
        print("0. Déconnexion")

        choix = input("Sélectionnez une option : ")

        
        if choix == "1":
            modify_user_information(user_id)
        elif choix == "3":
            manage_user_accounts()
        elif choix == "2":
            change_password(user_id)
        elif choix == "0":
            print("Déconnexion réussie.")
            break
        else:
            print("Option invalide. Veuillez sélectionner une option valide.")

def user_menu(user_id):                                                 #menu des utilisateur ordinaire sans priviliége
    while True:
        print("Bienvenue! Que souhaitez-vous faire ?")
        print("1. Consulter mes informations")
        print("2. Modifier mes informations")
        print("3. Modifier mon mot de passe")
        print("0. Déconnexion")

        choix = input("Sélectionnez une option : ")

        if choix == "1":
            display_user_information(user_id)
        elif choix == "2":
            modify_user_information(user_id)
        elif choix == "3":
            change_password(user_id)
        elif choix == "0":
            print("Déconnexion réussie.")
            break
        else:
            print("Option invalide. Veuillez sélectionner une option valide.")

def manage_admin_accounts():                                                            #menu pour gerer les compte administrateur (exclusive au superadmin)
    while True:
        print("Gérer les comptes admins")
        print("1. Consulter les informations d'un admin")
        print("2. Modifier le mot de passe d'un admin")
        print("3. Afficher la liste des admins")
        print("4. Créer un admin")
        print("5. Supprimer un admin")
        print("0. Retour en arrière")

        choix = input("Choisissez une option : ")

        if choix == "1":
            admin_id_consulter = input("Entrez l'ID de l'admin à consulter : ")
            display_user_information(admin_id_consulter)
        elif choix == "2":
            admin_id_modifier = input("Entrez l'ID de l'admin : ")
            change_password(admin_id_modifier)
        elif choix == "3":
            show_admin_list()
        elif choix == "4":
            save_admin()
        elif choix == "5":
            admin_id_supprimer = input("Entrez l'ID de l'admin à supprimer : ")
            delete_user(admin_id_supprimer)
        elif choix == "0":
            print("Retour au menu principal.")
            break
        else:
            print("Option invalide. Veuillez sélectionner une option valide.")

def show_admin_list():                                                                  #pour afficher la liste des admins
    print("Afficher la liste des admins")
    with open("utilisateurs.csv", mode="r") as f:
        reader = csv.reader(f, delimiter=",")
        admin_list = [row for row in reader if row[4] == "admin"]      #filtrer les lignes avec le type de compte "admin"
        if admin_list:
            headers = ["Nom", "Prénom", "ID", "Mot de passe", "Type de compte"]
            print(tabulate(admin_list, headers=headers, tablefmt="grid"))
        else:
            print("Aucun administrateur trouvé.")

def save_admin():                                                           #fonction pour crée des comptes admin (exclusive au superadmin)
    with open("utilisateurs.csv", mode="a", newline="") as f:
        writer = csv.writer(f, delimiter=",")
        print("Entrez les informations de l'admin à enregistrer")
        nom = input("Entrez le nom : ")
        prenom = input("Entrez le prénom : ")
        type_account = "admin"
        password_plain = generate_password()
        password_hashed = hash_password(password_plain)
        user_id = generate_id(nom, prenom)
        writer.writerow([nom, prenom, user_id, password_hashed, type_account])
        print("Utilisateur enregistré avec succès!")
        print("L'ID est:", user_id)
        print("Le mot de passe temporaire est:", password_plain)
        print("Le type de compte est:", type_account)
    
    
def modify_Admin_user_information():                                    #fonction pour modifier les comptes admins aussi exclusive au superadmin
    user_id = input("Entrez l'ID de l'utilisateur : ")
    with open("utilisateurs.csv", mode="r") as f:
        users = list(csv.reader(f))

    for user in users:
        if user[2] == user_id:
            new_nom = input("Entrez le nouveau nom : ")
            new_prenom = input("Entrez le nouveau prénom : ")
            user[0] = new_nom
            user[1] = new_prenom
            print("Informations utilisateur mises à jour avec succès.")
            break
    else:
        print("Utilisateur non trouvé.")

    with open("utilisateurs.csv", mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(users)

def modify_user_information(user_id):                                                               #pour modifier les information d'un utilisateur
    with open("utilisateurs.csv", mode="r") as f:
        users = list(csv.reader(f))

    for user in users:
        if user[2] == user_id:
            new_nom = input("Entrez le nouveau nom : ")
            new_prenom = input("Entrez le nouveau prénom : ")
            user[0] = new_nom
            user[1] = new_prenom
            print("Informations utilisateur mises à jour avec succès.")
            break
    else:
        print("Utilisateur non trouvé.")

    with open("utilisateurs.csv", mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(users)

def change_password(user_id):                                                           #fonction pour modifier le mot de passe
    with open("utilisateurs.csv", mode="r") as f:
        users = list(csv.reader(f))

    for user in users:
        if user[2] == user_id:
            while True:
                new_password = input("Entrez votre nouveau mot de passe : ")
                if len(new_password) < 8 or not any(char.isupper() for char in new_password):        #ici on indique que le mot de passe doit avoir 8 charactere et au moin une majiscule (politique de mot de passe fort)
                    print("Le mot de passe doit contenir au moins 8 caractères avec au moins une majuscule.")
                else:
                    user[3] = hash_password(new_password)
                    user[5] = "1"                                             #on hash ensuite le mot de passe et on l'enregistre dans le ficher csv
                    print("Mot de passe mis à jour avec succès.")
                    break
            break
    else:
        print("Utilisateur non trouvé.")

    with open("utilisateurs.csv", mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(users)

def manage_user_accounts():                                                                             #menu pour gérer les comptes utilisateur (super admin + admins)
    while True:
        print("Gérer les comptes utilisateurs")
        print("1. Consulter les informations d'un utilisateur")
        print("2. Modifier le mot de passe d'un utilisateur")
        print("3. Afficher la liste des utilisateurs")
        print("4. Créer un utilisateur")
        print("5. Supprimer un utilisateur")
        print("0. Retour en arrière")

        choix = input("Choisissez une option : ")

        if choix == "1":
            user_id_consulter = input("Entrez l'ID de l'utilisateur à consulter : ")
            display_user_information(user_id_consulter)
        elif choix == "2":
            user_id_modifier = input("Entrez l'ID de l'utilisateur : ")
            change_password(user_id_modifier)
        elif choix == "3":
            show_user_list()
        elif choix == "4":
            save_user()
        elif choix =="5":
            id_user = input("Donnez l'id de l'utilisateur à supprimer: ")
            delete_user(id_user)    
        elif choix == "0":
            print("Retour au menu principal.")
            break
        else:
            print("Option invalide. Veuillez sélectionner une option valide.")
        
    
def show_user_list():                                                                                   #afficher la liste des utilisateurs
    print("Afficher la liste des utilisateur")
    with open("utilisateurs.csv", mode="r") as f:
        reader = csv.reader(f, delimiter=",")
        user_list = [row for row in reader if row[4] == "utilisateur"]                      #filtrer les lignes avec le type de compte "utilisateur"
        if user_list:
            headers = ["Nom", "Prénom", "ID", "Mot de passe", "Type de compte"]
            print(tabulate(user_list, headers=headers, tablefmt="grid"))                    #l'affichage par tableau grace a tabulate (plus clean, et plus comprehensible)
        else:
            print("Aucun administrateur trouvé.")

# Boucle principale de notre script
while True:
    print("Annuaire - Patient First")
    print("1. Connexion")
    print("2. Inscription")
    print("3. À propos")
    print("0. Quitter")

    choix = input("Sélectionnez une option : ")

    if choix == "1":
        login_user()
    elif choix == "2":
        save_user()
    elif choix == "3":
        print("Patient First est une application de gestion des utilisateurs.")
    elif choix == "0":
        print("Merci d'avoir utilisé Patient First. À bientôt !")
        break
    else:
        print("Option invalide. Veuillez sélectionner une option valide.")






