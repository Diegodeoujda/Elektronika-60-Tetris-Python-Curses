import curses
import random
import time



#Dimension de JEU de la grille
Largeur = 10
Hauteur = 20
#Representation de chaque Tetriminos
Tétriminos = {
'Z' : [[1,1,0],[0,1,1]],
'S' : [[0,1,1],[1,1,0]],
'T' : [[1,1,1],[0,1,0]],
'J' : [[1,0,0],[1,1,1]],
'L' : [[0,0,1],[1,1,1]],
'I' : [[1,1,1,1]],
'O' : [[1,1],[1,1]]
}

class Tetris:
    def __init__(self, fenetre):
        self.fenetre = fenetre
        self.grille = self.creation_grille() #création grille

        self.piece_actu = random.choice(list(Tétriminos.values())) #piece_actuel
        self.prochaine_piece = random.choice(list(Tétriminos.values())) #prochaine piece
        self.pos_piece = [0, Largeur // 2 - len(self.piece_actu[0]) // 2] #position de la piece position -> [y,x] pour tout le jeu
        self.score = 0 #score
        self.vitesse = 0.2  #vitesse du jeu
        self.derniere_chute = time.time()#temps entre 2 chute
        self.running = True#booléen pour la boucle du jeu

        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        self.paire_couleurs = curses.color_pair(1)


    def creation_grille(self):
        '''Fonction permettant de retourner une representation de la grille composé de 0 et 1
        in: self
        out: grille -> liste composé de liste qui forme la grille'''
        grille = []
        for y in range(Hauteur+1): #hateur+1 car les il y a 1 delimitation
            ligne = []
            for x in range(Largeur+2): #largeur+2 car les il y a 2 bord
                if x == 0 or x == Largeur +1 or y == Hauteur: #Si on est au bord ou en bas de la grille
                    ligne.append(1)
                else:
                    ligne.append(0)
            grille.append(ligne)
        return grille


    def affichage_grille(self):
        '''Fonction permettant de retourner une representation graphique de la grille et d'afficher les pieces ainsi que la prochaine piece
        in: self
        out:x '''
        self.fenetre.clear()
        for y, ligne in enumerate(self.grille):                                
            for x, b in enumerate(ligne):                                           
                #Coté gauche de la grille                                               
                if x == 0 and b:
                    self.fenetre.addstr(y, x * 2 , "<!", self.paire_couleurs)
                #Coté droit de la grille
                elif x == Largeur +1 and b:
                    self.fenetre.addstr(y, x * 2, "!>", self.paire_couleurs)
                #bas de la grille
                elif y == Hauteur and b:
                    self.fenetre.addstr(y, x * 2 , "=", self.paire_couleurs)
                #intérieur de la grille
                elif b:  #blocs deja placé dans la grille
                    self.fenetre.addstr(y, x * 2, "[]",self.paire_couleurs)
                else:
                    self.fenetre.addstr(y, x*2 , ".", self.paire_couleurs)
        self.affichage_piece()
        self.affichage_prochaine_piece()
        self.fenetre.addstr(Hauteur + 1, 0, f"Score: {self.score}", self.paire_couleurs)
        self.fenetre.refresh()

    def affichage_piece(self):
        '''Fonction permettant de retourner une representation graphique de la piece actuel
        in: self
        out:x'''
        for y, ligne in enumerate(self.piece_actu):
            for x, b in enumerate(ligne):
                if b:
                    self.fenetre.addstr(self.pos_piece[0] + y, (self.pos_piece[1] + x) * 2, "[]",self.paire_couleurs)

    def affichage_prochaine_piece(self):
        '''Fonction permettant de retourner une representation graphique de la prochaine piece'''
        for y, ligne in enumerate(self.prochaine_piece):
            for x, b in enumerate(ligne):
                if b:
                    self.fenetre.addstr(8 + y, (Largeur + 5 + x) * 2, "[]",self.paire_couleurs)


    def rotation_anti_horaire(self, piece):
        '''fonction permettant de tourner la matrice de la piece a 90° dans le sens antihoraire
        in: self, piece
        out: piece_tournee etant la matrice de la piece tourner de 90° dans le sens antihoraire'''
        hauteur = len(piece)
        largeur = len(piece[0])
        piece_tournee = []
        for i in range(largeur):
            piece_tournee.append([0] * hauteur)

        for y in range(hauteur):
            for x in range(largeur):
                piece_tournee[largeur - 1 - x][y] = piece[y][x]
        return piece_tournee


    def check_collision(self, piece, pos):
        '''fonction permettant de detecter une colision entre un BLOC ou la grille de jeu
        in: self, piece, pos
        out: Booléen'''
        for y, ligne in enumerate(piece):
            for x, b in enumerate(ligne):
                if b:
                    y_piece = pos[0] + y
                    x_piece = pos[1] + x #--> permet d'avoir la postion de chaque bloc de la piece par rapport a la grille -> exemple si [[0,0,1],[1,1,1]] est en [2,4] alors position de chaque bloc -> (2, 6) (3, 4), (3, 5), (3, 6)
                    if x_piece < 0 or x_piece >= Largeur + 2 or y_piece >= Hauteur or self.grille[y_piece][x_piece]:
                        return True
        return False


    def rotation_piece(self):
        '''Fonction permettant d'effectuer la rotation de la piece dans la grille'''
        nouvelle_piece = self.rotation_anti_horaire(self.piece_actu)
        if not self.check_collision(nouvelle_piece, self.pos_piece):
            self.piece_actu = nouvelle_piece


    def placer_piece(self):
        '''fonction permettant de placer une piece dans la grille de jeu'''
        for y, ligne in enumerate(self.piece_actu):
            for x, b in enumerate(ligne):
                if b:
                    self.grille[self.pos_piece[0] + y][self.pos_piece[1] + x] = 1


    def supprimer_ligne(self):
        '''fonction permettant de supprimer les lignes complete'''
        ligne_pas_pleine = []

        for ligne in self.grille[:-1]: #on parcourt tout le tableau sauf la derniere car délimitation
            p = False
            for b in ligne[1:Largeur + 1]:
                if not b:
                    p = True
            if p:
                ligne_pas_pleine.append(ligne)

        nb_ligne_supprimé = Hauteur - len(ligne_pas_pleine) #nombre de ligne supprimé pour inserer des lignes vide

        ligne_vide = [1] + [0] * Largeur + [1]
        self.grille = [ligne_vide for i in range(nb_ligne_supprimé)] + ligne_pas_pleine
        self.grille.append([1] * (Largeur + 2))

        self.score += nb_ligne_supprimé


    def input(self):
        '''fonction qui gere les action de l'utilisateur'''
        key = self.fenetre.getch()

        if key == curses.KEY_LEFT:
            nouvelle_pos = [self.pos_piece[0], self.pos_piece[1] - 1]
            if not self.check_collision(self.piece_actu, nouvelle_pos):
                self.pos_piece = nouvelle_pos
        elif key == curses.KEY_RIGHT:
            nouvelle_pos = [self.pos_piece[0], self.pos_piece[1] + 1]
            if not self.check_collision(self.piece_actu, nouvelle_pos):
                self.pos_piece = nouvelle_pos
        elif key == curses.KEY_DOWN:
            nouvelle_pos = [self.pos_piece[0] + 1, self.pos_piece[1]]
            if not self.check_collision(self.piece_actu, nouvelle_pos):
                self.pos_piece = nouvelle_pos
        elif key == ord(" "):
                    self.rotation_piece()


    def update(self):
        '''fonction mettant a jour l'etat du jeu'''
        if time.time() - self.derniere_chute > self.vitesse: #verifie si le temps entre 2 deplacement est supérieur a 0.5
            self.derniere_chute = time.time() #on stocke le temps de la derniere chute
            nouvelle_pos = [self.pos_piece[0] + 1, self.pos_piece[1]]
            if not self.check_collision(self.piece_actu, nouvelle_pos):
                self.pos_piece = nouvelle_pos
            else:
                self.placer_piece()
                self.supprimer_ligne()
                self.piece_actu = self.prochaine_piece
                self.prochaine_piece = random.choice(list(Tétriminos.values()))
                self.pos_piece = [0, Largeur // 2 - len(self.piece_actu[0]) // 2]
                if self.check_collision(self.piece_actu, self.pos_piece):
                    self.running = False


    def run(self):
        self.fenetre.nodelay(1) #permet de continuer l'execution du programme meme si aucune touche n'est presser
        while self.running:
            self.affichage_grille()
            self.input()
            self.update()
            time.sleep(0.05)
        #game over
        self.fenetre.addstr(Hauteur // 2, Largeur, "GAME OVER", self.paire_couleurs)
        self.fenetre.refresh()
        time.sleep(5)


def main(fenetre):
    game = Tetris(fenetre)
    game.run()

curses.wrapper(main)

