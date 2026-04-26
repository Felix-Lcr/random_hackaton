import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import os
import subprocess
import sys
from PIL import Image, ImageTk

from logic import calculer_score
from boss import calcul_degats_boss, BOSS_MAX_HP, BOSS_ATTACK_BASE, BOSS_ATTACKS_PER_TURN
from scoreboard import charger_scores, sauvegarder_score

JOUEUR_MAX_HP = 150
MAX_REROLLS = 3

BG_JEU = "#1a1a2e"
COULEUR_BOSS = "#e74c3c"
COULEUR_JOUEUR = "#2ecc71"
COULEUR_TENU = "#f1c40f"
COULEUR_DE_NORMAL = "#2c3e50"


class PokerDiceBattler:
    def __init__(self, root):
        self.root = root
        self.root.title("Poker-Dice Battler")
        self.root.geometry("1000x700")
        self.root.resizable(False, False)

        self.dice_images = []
        for i in range(1, 7):
            chemin = f"assets/dice_{i}.png"
            if os.path.exists(chemin):
                img = tk.PhotoImage(file=chemin)
                self.dice_images.append(img.subsample(3, 3))
            else:
                self.dice_images.append(None)

        self.bg_image_tk = self._preparer_fond("assets/background.png", 0.4)
        self.afficher_menu()

    def _preparer_fond(self, chemin, opacite):
        if os.path.exists(chemin):
            img = Image.open(chemin).convert("RGBA")
            alpha = img.getchannel("A")
            img.putalpha(alpha.point(lambda i: int(i * opacite)))
            return ImageTk.PhotoImage(img)
        return None

    def _nettoyer_fenetre(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ------------------------------------------------------------------ Menu --

    def afficher_menu(self):
        self._nettoyer_fenetre()
        self.root.configure(bg="#1a1a1a")

        if self.bg_image_tk:
            tk.Label(self.root, image=self.bg_image_tk, bg="#1a1a1a").place(
                x=0, y=0, relwidth=1, relheight=1
            )

        tk.Label(
            self.root,
            text="POKER-DICE BATTLER",
            font=("Arial", 45, "bold"),
            fg="#f1c40f",
            bg="#1a1a1a",
        ).pack(pady=(80, 40))

        for texte, action, couleur in [
            ("JOUER", self.lancer_partie, "#27ae60"),
            ("RÈGLES", self.afficher_regles, "#2980b9"),
            ("SCOREBOARD", self.afficher_scoreboard, "#8e44ad"),
            ("DICE QUEST ↗", self.lancer_dice_quest, "#c0392b"),
        ]:
            tk.Button(
                self.root,
                text=texte,
                command=action,
                font=("Arial", 18, "bold"),
                bg=couleur,
                fg="white",
                width=20,
                height=2,
                bd=0,
                cursor="hand2",
            ).pack(pady=10)

    def afficher_regles(self):
        degat_niv1 = BOSS_ATTACK_BASE * BOSS_ATTACKS_PER_TURN
        regles = (
            f"Survivez le plus longtemps possible !\n"
            f"Chaque boss tué = 1 niveau de plus.\n\n"
            f"Chaque tour :\n"
            f"  • Lancez 5 dés — jusqu'à {MAX_REROLLS} relances\n"
            f"  • Cliquez un dé pour le garder avant de relancer\n"
            f"  • Choisissez : ATTAQUER ou SOIGNER\n"
            f"  • Le boss contre-attaque {BOSS_ATTACKS_PER_TURN}× (fixe)\n\n"
            f"Boss attaque : {BOSS_ATTACK_BASE} dmg × 2 par tour au niveau 1\n"
            f"Soit {degat_niv1} dmg/tour — double à chaque niveau !\n\n"
            f"Score = niveaux franchis\n\n"
            f"Score = (Chips + Somme des dés) × Multiplicateur\n\n"
            f"Hands :\n"
            f"  Five of a Kind  120 × 12\n"
            f"  Four of a Kind   60 × 7\n"
            f"  Straight         50 × 5\n"
            f"  Full House       40 × 4\n"
            f"  Three of a Kind  30 × 3\n"
            f"  Two Pair         20 × 2\n"
            f"  Pair             10 × 2\n"
            f"  High Card         5 × 1\n\n"
            f"Overheal → surplus de soin = Armure."
        )
        messagebox.showinfo("Règles", regles)

    def afficher_scoreboard(self):
        scores = charger_scores()
        texte = "TOP 3 :\n"
        for r, n, s in scores:
            texte += f"{r}. {n} — {s} niveau(x)\n"
        messagebox.showinfo("Scores", texte)

    def lancer_dice_quest(self):
        src_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "random_hackaton", "src"
        )
        subprocess.Popen([sys.executable, "main.py"], cwd=src_dir)

    # ------------------------------------------------------------------ Game setup --

    def lancer_partie(self):
        self._nettoyer_fenetre()
        self.root.configure(bg=BG_JEU)

        self.pv_joueur = JOUEUR_MAX_HP
        self.armure = 0
        self.pv_boss = BOSS_MAX_HP
        self.niveau = 1
        self.des = []
        self.tenus = [False] * 5
        self.rerolls_restants = MAX_REROLLS
        self._score_actuel = 0

        self._construire_ui_jeu()
        self._lancer_des()

    def _construire_ui_jeu(self):
        # Level indicator
        self.ui_niveau = tk.Label(
            self.root,
            text=self._texte_niveau(),
            font=("Arial", 18, "bold"),
            fg="#9b59b6",
            bg=BG_JEU,
        )
        self.ui_niveau.pack(pady=(10, 0))

        # Boss status
        self.ui_boss_hp = tk.Label(
            self.root,
            text=self._texte_boss_hp(),
            font=("Arial", 20, "bold"),
            fg=COULEUR_BOSS,
            bg=BG_JEU,
        )
        self.ui_boss_hp.pack(pady=(4, 0))

        self.ui_boss_log = tk.Label(
            self.root, text=self._texte_attaque_boss(), font=("Arial", 12), fg="#e67e22", bg=BG_JEU
        )
        self.ui_boss_log.pack()

        # Player status
        self.ui_joueur_hp = tk.Label(
            self.root,
            text=self._texte_joueur_hp(),
            font=("Arial", 15, "bold"),
            fg=COULEUR_JOUEUR,
            bg=BG_JEU,
        )
        self.ui_joueur_hp.pack(pady=(6, 0))

        # Score breakdown
        self.ui_score = tk.Label(
            self.root, text="—", font=("Arial", 13, "bold"), fg="#f1c40f", bg=BG_JEU
        )
        self.ui_score.pack(pady=(4, 0))

        # Rerolls counter
        self.ui_rerolls = tk.Label(
            self.root,
            text=self._texte_rerolls(),
            font=("Arial", 12),
            fg="white",
            bg=BG_JEU,
        )
        self.ui_rerolls.pack(pady=(2, 8))

        # Dice row
        cadre_des = tk.Frame(self.root, bg=BG_JEU)
        cadre_des.pack()

        self.labels_des = []
        self.labels_tenu = []
        for i in range(5):
            col = tk.Frame(cadre_des, bg=BG_JEU)
            col.pack(side="left", padx=8)

            lbl = tk.Label(
                col,
                bg=COULEUR_DE_NORMAL,
                highlightbackground=COULEUR_DE_NORMAL,
                highlightthickness=3,
                cursor="hand2",
            )
            lbl.pack()
            lbl.bind("<Button-1>", lambda e, idx=i: self._basculer_tenu(idx))
            self.labels_des.append(lbl)

            lbl_tenu = tk.Label(
                col, text="", font=("Arial", 9, "bold"), fg=COULEUR_TENU, bg=BG_JEU, width=10
            )
            lbl_tenu.pack()
            self.labels_tenu.append(lbl_tenu)

        # Action buttons
        cadre_btns = tk.Frame(self.root, bg=BG_JEU)
        cadre_btns.pack(pady=12)

        self.btn_lancer = tk.Button(
            cadre_btns,
            text="RELANCER",
            command=self._lancer_des,
            font=("Arial", 14, "bold"),
            bg="#e67e22",
            fg="white",
            padx=18,
            pady=8,
            cursor="hand2",
        )
        self.btn_lancer.pack(side="left", padx=6)

        self.btn_attaquer = tk.Button(
            cadre_btns,
            text="⚔  ATTAQUER",
            command=self._attaquer,
            font=("Arial", 14, "bold"),
            bg="#c0392b",
            fg="white",
            padx=18,
            pady=8,
            cursor="hand2",
            state="disabled",
        )
        self.btn_attaquer.pack(side="left", padx=6)

        self.btn_soigner = tk.Button(
            cadre_btns,
            text="♥  SOIGNER",
            command=self._soigner,
            font=("Arial", 14, "bold"),
            bg="#27ae60",
            fg="white",
            padx=18,
            pady=8,
            cursor="hand2",
            state="disabled",
        )
        self.btn_soigner.pack(side="left", padx=6)

        tk.Button(
            self.root,
            text="RETOUR MENU",
            command=self.afficher_menu,
            font=("Arial", 10),
            bg="#34495e",
            fg="white",
            cursor="hand2",
        ).pack(side="bottom", pady=10)

        self._construire_table_combinaisons()

    def _construire_table_combinaisons(self):
        panel = tk.Frame(self.root, bg="#16213e", highlightbackground="#9b59b6", highlightthickness=1)
        panel.place(x=790, y=460, width=200, height=230)

        tk.Label(
            panel, text="COMBINAISONS", font=("Arial", 10, "bold"), fg="#f1c40f", bg="#16213e"
        ).pack(pady=(8, 6))

        self.labels_combo = {}
        for nom_logique, nom_affiche, chips, multi in [
            ("FIVE OF A KIND",  "Five of a Kind",  120, 12),
            ("FOUR OF A KIND",  "Four of a Kind",   60,  7),
            ("STRAIGHT",        "Straight",          50,  5),
            ("FULL HOUSE",      "Full House",        40,  4),
            ("THREE OF A KIND", "Three of a Kind",   30,  3),
            ("TWO PAIR",        "Two Pair",          20,  2),
            ("PAIR",            "Pair",              10,  2),
            ("HIGH CARD",       "High Card",          5,  1),
        ]:
            row = tk.Frame(panel, bg="#16213e")
            row.pack(fill="x", padx=8, pady=2)

            lbl_nom = tk.Label(
                row, text=nom_affiche, font=("Arial", 9), fg="#aaaaaa", bg="#16213e", anchor="w"
            )
            lbl_nom.pack(side="left")

            lbl_score = tk.Label(
                row, text=f"{chips}×{multi}", font=("Arial", 9, "bold"), fg="#aaaaaa", bg="#16213e", anchor="e"
            )
            lbl_score.pack(side="right")

            self.labels_combo[nom_logique] = (row, lbl_nom, lbl_score)

    def _surligner_combinaison(self, nom_actif):
        for nom, (row, lbl_nom, lbl_score) in self.labels_combo.items():
            if nom == nom_actif:
                row.config(bg="#2d1b4e")
                lbl_nom.config(fg="#f1c40f", bg="#2d1b4e", font=("Arial", 9, "bold"))
                lbl_score.config(fg="#f1c40f", bg="#2d1b4e", font=("Arial", 9, "bold"))
            else:
                row.config(bg="#16213e")
                lbl_nom.config(fg="#aaaaaa", bg="#16213e", font=("Arial", 9))
                lbl_score.config(fg="#aaaaaa", bg="#16213e", font=("Arial", 9))

    # ------------------------------------------------------------------ Dice --

    def _basculer_tenu(self, i):
        if not self.des:
            return
        self.tenus[i] = not self.tenus[i]
        self._rafraichir_des()

    def _lancer_des(self):
        if self.rerolls_restants <= 0:
            return

        if not self.des:
            self.des = [random.randint(1, 6) for _ in range(5)]
        else:
            self.rerolls_restants -= 1
            self.des = [
                self.des[i] if self.tenus[i] else random.randint(1, 6)
                for i in range(5)
            ]

        self._rafraichir_des()
        self._rafraichir_score()
        self.ui_rerolls.config(text=self._texte_rerolls())

        if self.rerolls_restants == 0:
            self.btn_lancer.config(state="disabled")

        self.btn_attaquer.config(state="normal")
        self.btn_soigner.config(state="normal")

    def _rafraichir_des(self):
        for i in range(5):
            if not self.des:
                return
            val = self.des[i]
            img = self.dice_images[val - 1]
            bord = COULEUR_TENU if self.tenus[i] else COULEUR_DE_NORMAL
            lbl = self.labels_des[i]

            if img:
                lbl.config(
                    image=img, text="", width=120, height=120,
                    highlightbackground=bord, highlightthickness=3,
                )
            else:
                lbl.config(
                    image="", text=str(val), font=("Arial", 36),
                    fg="white", width=3, height=1,
                    highlightbackground=bord, highlightthickness=3,
                )

            self.labels_tenu[i].config(text="TENU" if self.tenus[i] else "")

    def _rafraichir_score(self):
        nom, chips_base, somme_des, multi, score = calculer_score(self.des)
        self.ui_score.config(
            text=f"{nom}   ({chips_base} + {somme_des}) × {multi} = {score} pts"
        )
        self._score_actuel = score
        self._surligner_combinaison(nom)

    # ------------------------------------------------------------------ Player actions --

    def _desactiver_boutons(self):
        self.btn_lancer.config(state="disabled")
        self.btn_attaquer.config(state="disabled")
        self.btn_soigner.config(state="disabled")

    def _attaquer(self):
        self._desactiver_boutons()
        self.pv_boss = max(0, self.pv_boss - self._score_actuel)
        self.ui_boss_hp.config(text=self._texte_boss_hp())
        if self.pv_boss <= 0:
            self._niveau_suivant()
            return
        self._tour_boss()

    def _soigner(self):
        self._desactiver_boutons()
        soin = self._score_actuel
        hp_manquant = JOUEUR_MAX_HP - self.pv_joueur
        if soin > hp_manquant:
            self.armure += soin - hp_manquant
            self.pv_joueur = JOUEUR_MAX_HP
        else:
            self.pv_joueur += soin
        self.ui_joueur_hp.config(text=self._texte_joueur_hp())
        self._tour_boss()

    # ------------------------------------------------------------------ Boss turn --

    def _tour_boss(self):
        degat_par_coup, nb_coups = calcul_degats_boss(self.niveau)

        for _ in range(nb_coups):
            if self.pv_joueur <= 0:
                break
            absorbé = min(self.armure, degat_par_coup)
            self.armure -= absorbé
            self.pv_joueur = max(0, self.pv_joueur - (degat_par_coup - absorbé))

        self.ui_joueur_hp.config(text=self._texte_joueur_hp())
        self.ui_boss_log.config(text=self._texte_attaque_boss())

        if self.pv_joueur <= 0:
            self._defaite()
            return

        self._nouveau_tour()

    # ------------------------------------------------------------------ Level up --

    def _niveau_suivant(self):
        self.niveau += 1
        self.pv_boss = BOSS_MAX_HP

        degat_par_coup, _ = calcul_degats_boss(self.niveau)
        messagebox.showinfo(
            f"Niveau {self.niveau} !",
            f"Boss vaincu !\n\nNIVEAU {self.niveau}\nAttaque du boss : {degat_par_coup} × 2 dmg/tour",
        )

        self.ui_niveau.config(text=self._texte_niveau())
        self.ui_boss_hp.config(text=self._texte_boss_hp())
        self.ui_boss_log.config(text=self._texte_attaque_boss())
        self._nouveau_tour()

    # ------------------------------------------------------------------ Turn reset --

    def _nouveau_tour(self):
        self.des = []
        self.tenus = [False] * 5
        self.rerolls_restants = MAX_REROLLS

        self.ui_score.config(text="—")
        self.ui_rerolls.config(text=self._texte_rerolls())
        self.btn_attaquer.config(state="disabled")
        self.btn_soigner.config(state="disabled")
        self.btn_lancer.config(state="normal")

        self._lancer_des()

    # ------------------------------------------------------------------ End conditions --

    def _defaite(self):
        niveaux = self.niveau - 1
        messagebox.showinfo(
            "Défaite",
            f"Vous avez été vaincu au niveau {self.niveau}...\nScore : {niveaux} niveau(x) franchi(s)",
        )
        scores = charger_scores()
        if len(scores) < 3 or niveaux > int(scores[-1][2]):
            nom = simpledialog.askstring("Record !", "Ton nom :") or "Anonyme"
            sauvegarder_score(nom, niveaux)
        self.afficher_menu()

    # ------------------------------------------------------------------ Helpers --

    def _texte_niveau(self):
        return f"— NIVEAU {self.niveau} —"

    def _texte_boss_hp(self):
        return f"BOSS  {self.pv_boss} / {BOSS_MAX_HP} PV"

    def _texte_attaque_boss(self):
        degat_par_coup, nb_coups = calcul_degats_boss(self.niveau)
        return f"Boss attaque {nb_coups}× {degat_par_coup} dmg/coup ({degat_par_coup * nb_coups} total)"

    def _texte_joueur_hp(self):
        base = f"Vos PV : {self.pv_joueur} / {JOUEUR_MAX_HP}"
        return base + (f"   Armure : {self.armure}" if self.armure > 0 else "")

    def _texte_rerolls(self):
        return f"Relances restantes : {self.rerolls_restants} / {MAX_REROLLS}"
