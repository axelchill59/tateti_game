import tkinter
from tkinter import ttk
from tkinter import messagebox
from tkinter import PhotoImage
import os
import sqlite3 as lite
import time
from time import sleep
import random

#Quit functions
def quit():
	quit_prompt=messagebox.askyesno("Confirmar", "¿Salir del juego?")

	if quit_prompt:
		connection.close()
		main_window.destroy()

def closing_game(vs,diff):
	global game_window
	global player1, player2
	global player1_score, player2_score

	pause_timer()

	close_prompt=messagebox.askyesno("Confirmar","¿Desea salir del juego?")

	if close_prompt:
		if vs=="ia" and diff=="hard":
			stop_timer()
		exit_restart(vs)
		game_window.destroy()
		main_window.deiconify()
		game_window=None
	else:
		unpause_timer()

def quit_game(game_window,main_window):
	game_window.destroy()
	main_window.deiconify()
	
def close_choose_mode(choose_game_window):
	choose_game_window.destroy()
	main_window.deiconify()

def scores_window_closing(scores_window,vs,diff):
	global game_window

	scores_window.destroy()

	if game_window:
		pass

	if game_window==None:
		main_window.deiconify()

	if vs =="ia" and diff=="hard":
		unpause_timer()

def change_players_window_closing(scores_window,vs,diff):
	if vs == "ia":
		if diff == "hard":
			unpause_timer()

	scores_window.destroy()

def tutorial_close(vs,diff,tutorial_window):
	if vs=="ia" and diff=="hard":
		unpause_timer()
		tutorial_window.destroy()
	else:
		tutorial_window.destroy()

	if main_window:
		if not game_window:
			main_window.deiconify()


#Restart functions
def exit_restart(vs):
	global clicked, count
	global player1,player2
	global player1_score, player2_score
	global player1_label, player2_label

	clicked = True
	count = 0

	if vs=="two":
		player1="Jugador 1"
		player2="Jugador 2"

	if vs=="ia":
		player1="Jugador 1"
		
		if diff=="easy":
			player2="I.A.(F)"
		if diff=="normal":
			player2="I.A.(N)"
		if diff=="hard":
			player2="I.A.(D)"

	player1_score=0
	player2_score=0

	bot1.config(text=" ", state="normal", bg="SystemButtonFace")
	bot2.config(text=" ", state="normal", bg="SystemButtonFace")
	bot3.config(text=" ", state="normal", bg="SystemButtonFace")
	bot4.config(text=" ", state="normal", bg="SystemButtonFace")
	bot5.config(text=" ", state="normal", bg="SystemButtonFace")
	bot6.config(text=" ", state="normal", bg="SystemButtonFace")
	bot7.config(text=" ", state="normal", bg="SystemButtonFace")
	bot8.config(text=" ", state="normal", bg="SystemButtonFace")
	bot9.config(text=" ", state="normal", bg="SystemButtonFace")

	player1_label.config(text=f"{player1} : {player1_score}")
	player2_label.config(text=f"{player2} : {player2_score}")

	turn_label.config(text="[TURNO]",bg="DeepSkyBlue1")
	turn_label.place(x="110",y="456",width=60,height=30)

def disable_all_buttons():
	bot1.config(state="disabled")
	bot2.config(state="disabled")
	bot3.config(state="disabled")
	bot4.config(state="disabled")
	bot5.config(state="disabled")
	bot6.config(state="disabled")
	bot7.config(state="disabled")
	bot8.config(state="disabled")
	bot9.config(state="disabled")

def reset_game(vs,diff):
	global player1, player2

	if vs=="ia" and diff=="hard":
		pause_timer()

	confirm_prompt=messagebox.askyesno("Confirmar", "¿Está segudo que desea reiniciar?")

	if confirm_prompt:
		stop_timer()
		exit_restart(vs)
		if vs=="ia":
			reset_timer()
	else:
		unpause_timer()

def restart_board():
	global clicked, count
	global player1_label, player2_label

	clicked = True
	count = 0

	bot1.config(text=" ", state="normal", bg="SystemButtonFace")
	bot2.config(text=" ", state="normal", bg="SystemButtonFace")
	bot3.config(text=" ", state="normal", bg="SystemButtonFace")
	bot4.config(text=" ", state="normal", bg="SystemButtonFace")
	bot5.config(text=" ", state="normal", bg="SystemButtonFace")
	bot6.config(text=" ", state="normal", bg="SystemButtonFace")
	bot7.config(text=" ", state="normal", bg="SystemButtonFace")
	bot8.config(text=" ", state="normal", bg="SystemButtonFace")
	bot9.config(text=" ", state="normal", bg="SystemButtonFace")

	turn_label.config(text="[TURNO]",bg="DeepSkyBlue1")
	turn_label.place(x="110",y="456",width=60,height=30)


#Scores window & functions
def scores_window(vs,diff):
	main_window.iconify()
	scores_window=tkinter.Toplevel()
	scores_window.geometry("550x450")
	scores_window.resizable(0,0)
	scores_window.title("")
	scores_window.iconbitmap("assets/game.ico")

	if vs == "ia" and diff=="hard":
		pause_timer()

	#scores_window_closing_protocol
	scores_window.protocol("WM_DELETE_WINDOW", lambda:scores_window_closing(scores_window,vs,diff))

	scores_background=tkinter.Label(scores_window,image=scores_bg)
	scores_background.place(x="0",y="0",width=550,height=430)

	menu_scores = tkinter.Menu(scores_window)
	scores_window.config(menu=menu_scores)

	scores_option_menu=tkinter.Menu(menu_scores,tearoff=False)

	menu_scores.add_cascade(label="Acciones", menu=scores_option_menu)

	scores_option_menu.add_command(label="Eliminar selección",command=lambda:delete_selected_score(tree))
	scores_option_menu.add_separator()
	scores_option_menu.add_command(label="Eliminar todo",command=lambda:delete_all_scores(tree))


	#TreeView
	tree = ttk.Treeview(scores_window, columns=("ID Juego", "Jugador 1", "Jugador 2", "Puntos Jugador 1", "Puntos Jugador 2"))
	tree['show'] = 'headings'

	#Vertical scroll bar
	vsb = ttk.Scrollbar(scores_window, orient="vertical", command=tree.yview)

	# Configurar Treeview para usar los Scrollbars
	tree.configure(yscrollcommand=vsb.set)

	#Headings
	tree.heading("#1", text="ID Juego")
	tree.heading("#2", text="Jugador 1")
	tree.heading("#3", text="Jugador 2")
	tree.heading("#4", text="Puntos Jugador 1")
	tree.heading("#5", text="Puntos Jugador 2")

    # Configurar columnas
	tree.column("#1", width=60)
	tree.column("#2", width=80)
	tree.column("#3", width=80)
	tree.column("#4", width=120)
	tree.column("#5", width=120)

    # Ejecutar una consulta SQL para obtener los datos
	cursor.execute("SELECT * FROM scores")

	# Insertar datos desde la base de datos
	for row in cursor.fetchall():
		tree.insert("", "end", values=row)
	
	tree.update()

	tree.place(x=35,y=114,height=290)
	vsb.place(x=497,y=114,height=290)

def delete_selected_score(tree):
    # Obtener la selección actual en el Treeview
    selected_item = tree.selection()
    
    delete_selected_prompt=messagebox.askyesno("Confirmar", "¿Desea eliminar este puntaje?")

    if delete_selected_prompt:
	    if selected_item:
	        # El primer elemento de la selección es el ID del juego
	        selected_game_id = tree.item(selected_item)['values'][0]
	        
	        # Ejecutar la consulta SQL para eliminar el juego seleccionado de la base de datos
	        cursor.execute("DELETE FROM scores WHERE game_id = ?", (selected_game_id,))
	        connection.commit()  # Guardar los cambios en la base de datos
	        
	        # Eliminar la selección del Treeview
	        tree.delete(selected_item)
	    else:
	    	messagebox.showinfo("", "No ha seleccionado ningún puntaje")

def delete_all_scores(tree):
    # Confirmar la eliminación de todos los puntajes
    confirm = tkinter.messagebox.askyesno("Eliminar todos los puntajes", "¿Seguro que quieres eliminar todos los puntajes?")
    
    if confirm:
        # Eliminar la tabla "scores" y luego volver a crearla
        cursor.execute("DROP TABLE IF EXISTS scores")
        cursor.execute("CREATE TABLE IF NOT EXISTS scores (game_id INTEGER PRIMARY KEY AUTOINCREMENT, player_1 TEXT, player_2 TEXT, player_1_score INTEGER, player_2_score INTEGER)")
        connection.commit()
        
        # Eliminar todas las filas del Treeview
        for item in tree.get_children():
            tree.delete(item)

def save_scores(vs,diff):
	if vs=="ia" and diff =="hard":
			pause_timer()
	
	confirm_save_prompt=messagebox.askyesno("", "¿Guardar los puntajes?")

	if confirm_save_prompt:
		saving_scores()
	else:
		unpause_timer()

def saving_scores():
	global player1, player2
	global player1_score, player2_score

	connection.execute(" insert into scores (player_1, player_2,player_1_score,player_2_score) values (?, ?, ?, ?)", (player1, player2,player1_score,player2_score))
	connection.commit()


#Secondary windows
def change_players_names(entry_player1, entry_player2,change_players_window):
	global player1, player2
	global player1_label, player2_label

	entry_text = entry_player1.get()

	if len(entry_text) <= 9:
		player1=entry_player1.get()
		player2=entry_player2.get()

		player1_label.config(text=f"{player1} : {player1_score}")
		player2_label.config(text=f"{player2} : {player2_score}")

		change_players_window.destroy()
	else:
		messagebox.showinfo("", "El nombre debe tener 9 caracteres o menos.")
	
def change_players(vs,diff):
	global player1
	global player2
	global detener_temporizador

	if vs == "ia":
		pause_timer()

	player1_name=tkinter.StringVar(value=player1)
	player2_name=tkinter.StringVar(value=player2)
	
	change_players_window=tkinter.Toplevel()
	change_players_window.geometry("300x200")
	change_players_window.title("")
	change_players_window.resizable(0,0)
	change_players_window.iconbitmap("assets/game.ico")

	change_players_window.protocol("WM_DELETE_WINDOW", lambda:change_players_window_closing(change_players_window,vs,diff))

	change_players_background=tkinter.Label(change_players_window,image=change_players_bg)
	change_players_background.place(x="0",y="0",width=300,height=200)

	confirm_button=tkinter.Button(change_players_window, image=change_players_button_bg,bd=0,command=lambda:(change_players_names(entry_player1, entry_player2,change_players_window),unpause_timer()))
	confirm_button.place(x="97",y="160",width=105,height=19)

	entry_player1=tkinter.Entry(change_players_window, textvariable=player1_name,bg="DeepSkyBlue1",bd=0,font="Courier 15")
	entry_player1.place(x="89",y="60",width=140,height=27)

	entry_player2=tkinter.Entry(change_players_window, textvariable=player2_name,bg="chocolate1",bd=0,font="Courier 15")
	entry_player2.place(x="89",y="108",width=140,height=27)

	if vs=="ia":
		entry_player2.config(state="disabled", disabledbackground="chocolate1")

	if vs=="two":
		entry_player2.config(state="normal")

def tutorial(vs,diff):
	tutorial_window=tkinter.Toplevel()
	tutorial_window.geometry("439x660")
	tutorial_window.resizable(0,0)
	tutorial_window.title("")
	tutorial_window.iconbitmap("assets/game.ico")

	if vs=="ia" and diff=="hard":
		pause_timer()

	if main_window:
		main_window.iconify()

	tutorial_window.protocol("WM_DELETE_WINDOW", lambda: tutorial_close(vs,diff,tutorial_window))

	#Background
	tutorial_window_background=tkinter.Label(tutorial_window,image=tutorial_bg)
	tutorial_window_background.place(x="0",y="0",width=439,height=660)


#Game functions 
def check_win(vs,diff):
	global winner
	global count
	global player1, player2
	global player1_score, player2_score
	global player1_label, player2_label
	global turn_label

	winner = False

	#Check X Horizontal
	if bot1["text"] == bot2["text"] == bot3["text"] == "X":
		bot1.config(bg="DeepSkyBlue1")
		bot2.config(bg="DeepSkyBlue1")
		bot3.config(bg="DeepSkyBlue1")
		disable_all_buttons()
		turn_label.config(bg="DeepSkyBlue1",text="[GANA]")
		turn_label.place(x="110",y="456",width=60,height=30)
		winner = True
		player1_score+=1
		player1_label.config(text=f"{player1} : {player1_score}")
		if vs=="ia" and diff=="hard":
			stop_timer()
			messagebox.showinfo("Tatetí", "¡Gana X!")
			restart_board()
			reset_timer()
		else:
			messagebox.showinfo("Tatetí", "¡Gana X!")
			restart_board()

	if bot4["text"] == bot5["text"] == bot6["text"] == "X":
		bot4.config(bg="DeepSkyBlue1")
		bot5.config(bg="DeepSkyBlue1")
		bot6.config(bg="DeepSkyBlue1")
		disable_all_buttons()
		turn_label.config(bg="DeepSkyBlue1",text="[GANA]")
		turn_label.place(x="110",y="456",width=60,height=30)
		winner = True
		player1_score+=1
		player1_label.config(text=f"{player1} : {player1_score}")
		if vs=="ia" and diff=="hard":
			stop_timer()
			messagebox.showinfo("Tatetí", "¡Gana X!")
			restart_board()
			reset_timer()
		else:
			messagebox.showinfo("Tatetí", "¡Gana X!")
			restart_board()

	if bot7["text"] == bot8["text"] == bot9["text"] == "X":
		bot7.config(bg="DeepSkyBlue1")
		bot8.config(bg="DeepSkyBlue1")
		bot9.config(bg="DeepSkyBlue1")
		disable_all_buttons()
		turn_label.config(bg="DeepSkyBlue1",text="[GANA]")
		turn_label.place(x="110",y="456",width=60,height=30)
		winner = True
		player1_score+=1
		player1_label.config(text=f"{player1} : {player1_score}")
		if vs=="ia" and diff=="hard":
			stop_timer()
			messagebox.showinfo("Tatetí", "¡Gana X!")
			restart_board()
			reset_timer()
		else:
			messagebox.showinfo("Tatetí", "¡Gana X!")
			restart_board()


	#Check X Vertical
	if bot1["text"] == bot4["text"] == bot7["text"] == "X":
		bot1.config(bg="DeepSkyBlue1")
		bot4.config(bg="DeepSkyBlue1")
		bot7.config(bg="DeepSkyBlue1")
		disable_all_buttons()
		turn_label.config(bg="DeepSkyBlue1",text="[GANA]")
		turn_label.place(x="110",y="456",width=60,height=30)
		winner = True
		player1_score+=1
		player1_label.config(text=f"{player1} : {player1_score}")
		if vs=="ia" and diff=="hard":
			stop_timer()
			messagebox.showinfo("Tatetí", "¡Gana X!")
			restart_board()
			reset_timer()
		else:
			messagebox.showinfo("Tatetí", "¡Gana X!")
			restart_board()

	if bot2["text"] == bot5["text"] == bot8["text"] == "X":
		bot2.config(bg="DeepSkyBlue1")
		bot5.config(bg="DeepSkyBlue1")
		bot8.config(bg="DeepSkyBlue1")
		disable_all_buttons()
		turn_label.config(bg="DeepSkyBlue1",text="[GANA]")
		turn_label.place(x="110",y="456",width=60,height=30)
		winner = True
		player1_score+=1
		player1_label.config(text=f"{player1} : {player1_score}")
		if vs=="ia" and diff=="hard":
			stop_timer()
			messagebox.showinfo("Tatetí", "¡Gana X!")
			restart_board()
			reset_timer()
		else:
			messagebox.showinfo("Tatetí", "¡Gana X!")
			restart_board()

	if bot3["text"] == bot6["text"] == bot9["text"] == "X":
		bot3.config(bg="DeepSkyBlue1")
		bot6.config(bg="DeepSkyBlue1")
		bot9.config(bg="DeepSkyBlue1")
		disable_all_buttons()
		turn_label.config(bg="DeepSkyBlue1",text="[GANA]")
		turn_label.place(x="110",y="456",width=60,height=30)
		winner = True
		player1_score+=1
		player1_label.config(text=f"{player1} : {player1_score}")
		if vs=="ia" and diff=="hard":
			stop_timer()
			messagebox.showinfo("Tatetí", "¡Gana X!")
			restart_board()
			reset_timer()
		else:
			messagebox.showinfo("Tatetí", "¡Gana X!")
			restart_board()

	#Check X Diagonal
	if bot1["text"] == bot5["text"] == bot9["text"] == "X":
		bot1.config(bg="DeepSkyBlue1")
		bot5.config(bg="DeepSkyBlue1")
		bot9.config(bg="DeepSkyBlue1")
		disable_all_buttons()
		turn_label.config(bg="DeepSkyBlue1",text="[GANA]")
		turn_label.place(x="110",y="456",width=60,height=30)
		winner = True
		player1_score+=1
		player1_label.config(text=f"{player1} : {player1_score}")
		if vs=="ia" and diff=="hard":
			stop_timer()
			messagebox.showinfo("Tatetí", "¡Gana X!")
			restart_board()
			reset_timer()
		else:
			messagebox.showinfo("Tatetí", "¡Gana X!")
			restart_board()

	if bot3["text"] == bot5["text"] == bot7["text"] == "X":
		bot3.config(bg="DeepSkyBlue1")
		bot5.config(bg="DeepSkyBlue1")
		bot7.config(bg="DeepSkyBlue1")
		disable_all_buttons()
		turn_label.config(bg="DeepSkyBlue1",text="[GANA]")
		turn_label.place(x="110",y="456",width=60,height=30)
		winner = True
		player1_score+=1
		player1_label.config(text=f"{player1} : {player1_score}")
		if vs=="ia" and diff=="hard":
			stop_timer()
			messagebox.showinfo("Tatetí", "¡Gana X!")
			restart_board()
			reset_timer()
		else:
			messagebox.showinfo("Tatetí", "¡Gana X!")
			restart_board()


	#Check O Horizontal
	if bot1["text"] == bot2["text"] == bot3["text"] == "O":
		bot1.config(bg="chocolate1")
		bot2.config(bg="chocolate1")
		bot3.config(bg="chocolate1")
		disable_all_buttons()
		turn_label.config(bg="chocolate1",text="[GANA]")
		turn_label.place(x="110",y="501",width=60,height=30)
		winner = True
		player2_score+=1
		player2_label.config(text=f"{player2} : {player2_score}")
		messagebox.showinfo("Tatetí", "¡Gana O!")
		restart_board()

	if bot4["text"] == bot5["text"] == bot6["text"] == "O":
		bot4.config(bg="chocolate1")
		bot5.config(bg="chocolate1")
		bot6.config(bg="chocolate1")
		disable_all_buttons()
		turn_label.config(bg="chocolate1",text="[GANA]")
		turn_label.place(x="110",y="501",width=60,height=30)
		winner = True
		player2_score+=1
		player2_label.config(text=f"{player2} : {player2_score}")
		messagebox.showinfo("Tatetí", "¡Gana O!")
		restart_board()

	if bot7["text"] == bot8["text"] == bot9["text"] == "O":
		bot7.config(bg="chocolate1")
		bot8.config(bg="chocolate1")
		bot9.config(bg="chocolate1")
		disable_all_buttons()
		turn_label.config(bg="chocolate1",text="[GANA]")
		turn_label.place(x="110",y="501",width=60,height=30)
		winner = True
		player2_score+=1
		player2_label.config(text=f"{player2} : {player2_score}")
		messagebox.showinfo("Tatetí", "¡Gana O!")
		restart_board()

	#Check O Vertical
	if bot1["text"] == bot4["text"] == bot7["text"] == "O":
		bot1.config(bg="chocolate1")
		bot4.config(bg="chocolate1")
		bot7.config(bg="chocolate1")
		disable_all_buttons()
		turn_label.config(bg="chocolate1",text="[GANA]")
		turn_label.place(x="110",y="501",width=60,height=30)
		winner = True
		player2_score+=1
		player2_label.config(text=f"{player2} : {player2_score}")
		messagebox.showinfo("Tatetí", "¡Gana O!")
		restart_board()

	if bot2["text"] == bot5["text"] == bot8["text"] == "O":
		bot2.config(bg="chocolate1")
		bot5.config(bg="chocolate1")
		bot8.config(bg="chocolate1")
		disable_all_buttons()
		turn_label.config(bg="chocolate1",text="[GANA]")
		turn_label.place(x="110",y="501",width=60,height=30)
		winner = True
		player2_score+=1
		player2_label.config(text=f"{player2} : {player2_score}")
		messagebox.showinfo("Tatetí", "¡Gana O!")
		restart_board()

	if bot3["text"] == bot6["text"] == bot9["text"] == "O":
		bot3.config(bg="chocolate1")
		bot6.config(bg="chocolate1")
		bot9.config(bg="chocolate1")
		disable_all_buttons()
		turn_label.config(bg="chocolate1",text="[GANA]")
		turn_label.place(x="110",y="501",width=60,height=30)
		winner = True
		player2_score+=1
		player2_label.config(text=f"{player2} : {player2_score}")
		messagebox.showinfo("Tatetí", "¡Gana O!")
		restart_board()

	#Check O Diagonal
	if bot1["text"] == bot5["text"] == bot9["text"] == "O":
		bot1.config(bg="chocolate1")
		bot5.config(bg="chocolate1")
		bot9.config(bg="chocolate1")
		disable_all_buttons()
		turn_label.config(bg="chocolate1",text="[GANA]")
		turn_label.place(x="110",y="501",width=60,height=30)
		winner = True
		player2_score+=1
		player2_label.config(text=f"{player2} : {player2_score}")
		messagebox.showinfo("Tatetí", "¡Gana O!")
		restart_board()

	if bot3["text"] == bot5["text"] == bot7["text"] == "O":
		bot3.config(bg="chocolate1")
		bot5.config(bg="chocolate1")
		bot7.config(bg="chocolate1")
		disable_all_buttons()
		turn_label.config(bg="chocolate1",text="[GANA]")
		turn_label.place(x="110",y="501",width=60,height=30)
		winner = True
		player2_score+=1
		player2_label.config(text=f"{player2} : {player2_score}")
		messagebox.showinfo("Tatetí", "¡Gana O!")
		restart_board()

	#Check full board
	if count == 9 and winner == False:
		disable_all_buttons()
		
		if vs=="ia" and diff=="hard":
			stop_timer()

		messagebox.showinfo("Tatetí", "¡Empate!")
		
		if vs=="ia" and diff=="hard":
			reset_timer()

		restart_board()
		
def click(b,vs,diff):
	global clicked, count

	if b["text"] == " " and clicked == True:
		b["text"] = "X"
		clicked = False
		count += 1
		turn_label.config(bg="chocolate1")
		turn_label.place(x="110",y="501",width=60,height=30)
		check_win(vs,diff)

	elif b["text"] == " " and clicked == False:
		b["text"] = "O"
		clicked = True
		count += 1
		turn_label.config(bg="DeepSkyBlue1")
		turn_label.place(x="110",y="456",width=60,height=30)
		check_win(vs,diff)
	else:
		print("lugar ocupado")
		#messagebox.showerror("Tatetí", "¡Lugar ocupado!")

	#Juega la I.A.
	if count % 2 == 1 and clicked == False and vs=="ia":

		if timer_id is not None:
			game_window.after_cancel(timer_id)	

		ia_plays(vs,diff)
		check_win(vs,diff)
		
		turn_label.config(bg="DeepSkyBlue1")
		turn_label.place(x="110",y="456",width=60,height=30)	

def change_turns():
	global player1, player2
	global player1_score, player2_score

	player1_name_flag = player1
	player1_score_flag = player1_score

	player1 = player2
	player1_score = player2_score

	player2 = player1_name_flag
	player2_score = player1_score_flag

	player1_label.config(text=f"{player1} : {player1_score}")
	player2_label.config(text=f"{player2} : {player2_score}")


#I.A. play
def ia_plays(vs,diff):
	global detener_temporizador

	if diff=="easy":
		ia_plays_easy(vs)

	if diff=="normal":
		ia_plays_normal(vs)

	if diff=="hard":
		ia_plays_normal(vs)
		reset_timer()

#Easy IA 
def ia_plays_easy(vs):
    global count, clicked

    count += 1
    clicked = True

    for b in [bot1, bot2, bot3, bot4, bot5, bot6, bot7, bot8, bot9]:
    	b.config(state="disabled")

    game_window.update()
    time.sleep(0.3)

    hacer_movimiento_aleatorio()
    	
    game_window.update()
    time.sleep(0.2)
    for b in [bot1, bot2, bot3, bot4, bot5, bot6, bot7, bot8, bot9]:
    	b.config(state="normal")
            
def hacer_movimiento_aleatorio():
    
    #Crea una lista de botones disponibles
    available_buttons = [button for button in [bot1, bot2, bot3, bot4, bot5, bot6, bot7, bot8, bot9] if button["text"] == " "]

    if available_buttons:
        selected_button = random.choice(available_buttons)        
        selected_button.config(text="O")

        check_win(vs,diff)

#Normal IA
def ia_plays_normal(vs):
    global count, clicked

    count += 1
    clicked = True

    # Verificar jugada ganadora para la computadora
    jugada_ganadora = buscar_jugada("O")

    if jugada_ganadora:
        #Desactiva todos los botones
        for b in [bot1, bot2, bot3, bot4, bot5, bot6, bot7, bot8, bot9]:
            b.config(state="disabled")
        #Actualiza la ventana    
        game_window.update()
        time.sleep(0.3)
        #Juega
        jugada_ganadora["text"] = "O"
        #Actualiza la ventana
        game_window.update()
        time.sleep(0.3)

        # Habilita los botones
        for b in [bot1, bot2, bot3, bot4, bot5, bot6, bot7, bot8, bot9]:
            b.config(state="normal")

        check_win(vs,diff)

    else:
        # Verificar jugada para bloquear al jugador
        jugada_bloqueo = buscar_jugada("X")
        if jugada_bloqueo:
        	#Desactiva todos los botones
        	for b in [bot1, bot2, bot3, bot4, bot5, bot6, bot7, bot8, bot9]:
        		b.config(state="disabled")
        	#Actualiza la ventana
        	game_window.update()
        	time.sleep(0.3)
        	#Juega
        	jugada_bloqueo["text"] = "O"
        	#Actualiza la ventana
        	game_window.update()
        	time.sleep(0.3)

        	# Habilita los botones
        	for b in [bot1, bot2, bot3, bot4, bot5, bot6, bot7, bot8, bot9]:
        		b.config(state="normal")

        	check_win(vs,diff)

        else:
            # Si no hay jugadas estratégicas, hacer un movimiento aleatorio
            #Desactiva los botones
            for b in [bot1, bot2, bot3, bot4, bot5, bot6, bot7, bot8, bot9]:
            	b.config(state="disabled")
            #Actualiza la ventana		
            game_window.update()
            time.sleep(0.3)
            #Juega aleatoriamente
            hacer_movimiento_aleatorio()
            #Actualiza la ventana
            game_window.update()
            time.sleep(0.2)
            #Activa todos los botones
            for b in [bot1, bot2, bot3, bot4, bot5, bot6, bot7, bot8, bot9]:
            	b.config(state="normal")

            check_win(vs,diff)

def buscar_jugada(simbolo):
    # Verificar filas
    if bot1["text"] == bot2["text"] == simbolo and bot3["text"] == " ":
        return bot3
    elif bot1["text"] == bot3["text"] == simbolo and bot2["text"] == " ":
        return bot2
    elif bot2["text"] == bot3["text"] == simbolo and bot1["text"] == " ":
        return bot1

    if bot4["text"] == bot5["text"] == simbolo and bot6["text"] == " ":
        return bot6
    elif bot4["text"] == bot6["text"] == simbolo and bot5["text"] == " ":
        return bot5
    elif bot5["text"] == bot6["text"] == simbolo and bot4["text"] == " ":
        return bot4

    if bot7["text"] == bot8["text"] == simbolo and bot9["text"] == " ":
        return bot9
    elif bot7["text"] == bot9["text"] == simbolo and bot8["text"] == " ":
        return bot8
    elif bot8["text"] == bot9["text"] == simbolo and bot7["text"] == " ":
        return bot7

    # Verificar columnas
    if bot1["text"] == bot4["text"] == simbolo and bot7["text"] == " ":
        return bot7
    elif bot1["text"] == bot7["text"] == simbolo and bot4["text"] == " ":
        return bot4
    elif bot4["text"] == bot7["text"] == simbolo and bot1["text"] == " ":
        return bot1

    if bot2["text"] == bot5["text"] == simbolo and bot8["text"] == " ":
        return bot8
    elif bot2["text"] == bot8["text"] == simbolo and bot5["text"] == " ":
        return bot5
    elif bot5["text"] == bot8["text"] == simbolo and bot2["text"] == " ":
        return bot2

    if bot3["text"] == bot6["text"] == simbolo and bot9["text"] == " ":
        return bot9
    elif bot3["text"] == bot9["text"] == simbolo and bot6["text"] == " ":
        return bot6
    elif bot6["text"] == bot9["text"] == simbolo and bot3["text"] == " ":
        return bot3

    # Verificar diagonales
    if bot1["text"] == bot5["text"] == simbolo and bot9["text"] == " ":
        return bot9
    elif bot1["text"] == bot9["text"] == simbolo and bot5["text"] == " ":
        return bot5
    elif bot5["text"] == bot9["text"] == simbolo and bot1["text"] == " ":
        return bot1

    if bot3["text"] == bot5["text"] == simbolo and bot7["text"] == " ":
        return bot7
    elif bot3["text"] == bot7["text"] == simbolo and bot5["text"] == " ":
        return bot5
    elif bot5["text"] == bot7["text"] == simbolo and bot3["text"] == " ":
        return bot3

    return None

#Hard IA
def ia_plays_hard(vs):
    global count, clicked

    count += 1
    clicked = True

    # Verificar jugada ganadora para la computadora
    jugada_ganadora = buscar_jugada("O")

    if jugada_ganadora:
        #Desactiva todos los botones
        for b in [bot1, bot2, bot3, bot4, bot5, bot6, bot7, bot8, bot9]:
            b.config(state="disabled")
        #Actualiza la ventana    
        game_window.update()
        time.sleep(0.3)
        #Juega
        jugada_ganadora["text"] = "O"
        #Actualiza la ventana
        game_window.update()
        time.sleep(0.3)

        # Habilita los botones
        for b in [bot1, bot2, bot3, bot4, bot5, bot6, bot7, bot8, bot9]:
            b.config(state="normal")

        check_win(vs,diff)

    else:
        # Verificar jugada para bloquear al jugador
        jugada_bloqueo = buscar_jugada("X")
        if jugada_bloqueo:
        	#Desactiva todos los botones
        	for b in [bot1, bot2, bot3, bot4, bot5, bot6, bot7, bot8, bot9]:
        		b.config(state="disabled")
        	#Actualiza la ventana
        	game_window.update()
        	time.sleep(0.3)
        	#Juega
        	jugada_bloqueo["text"] = "O"
        	#Actualiza la ventana
        	game_window.update()
        	time.sleep(0.3)

        	# Habilita los botones
        	for b in [bot1, bot2, bot3, bot4, bot5, bot6, bot7, bot8, bot9]:
        		b.config(state="normal")

        	check_win(vs,diff)

        else:
            # Si no hay jugadas estratégicas, hacer un movimiento aleatorio
            #Desactiva los botones
            for b in [bot1, bot2, bot3, bot4, bot5, bot6, bot7, bot8, bot9]:
            	b.config(state="disabled")
            #Actualiza la ventana		
            game_window.update()
            time.sleep(0.3)
            #Juega aleatoriamente
            hacer_movimiento_aleatorio()
            #Actualiza la ventana
            game_window.update()
            time.sleep(0.2)
            #Activa todos los botones
            for b in [bot1, bot2, bot3, bot4, bot5, bot6, bot7, bot8, bot9]:
            	b.config(state="normal")

            check_win(vs,diff)

def start_timer(count=None):
    global temporizador, timer_id
    global winner
    global player1, player2
    global player2_score
    global player2_label
    global turn_label

    if count is not None:
        temporizador.count = count

    if not paused:
	    if temporizador.count <= 0:
	        temporizador.configure(text="Tiempo agotado!")
	        disable_all_buttons()
	        turn_label.config(bg="chocolate1",text="[GANA]")
	        turn_label.place(x="110",y="501",width=60,height=30)
	        winner = True
	        player2_score+=1
	        player2_label.config(text=f"{player2} : {player2_score}")
	        messagebox.showinfo("Tatetí", "¡Gana O!")
	        restart_board()
	        reset_timer()
	    else:
	        temporizador.configure(text="%d" % temporizador.count)
	        temporizador.count = temporizador.count - 1
	        timer_id = game_window.after(1000, start_timer)

def stop_timer():
    global timer_id, paused, remaining_time
    if timer_id is not None:
        game_window.after_cancel(timer_id)
        timer_id = None
    paused = False
    remaining_time = 0

def reset_timer():
	global timer_id, paused, remaining_time
	if timer_id is not None:
		game_window.after_cancel(timer_id)

	start_timer(5)
	paused = False
	remaining_time = 5

def pause_timer():
	global paused, remaining_time, timer_id
	if not paused and timer_id is not None:
		game_window.after_cancel(timer_id)
		paused = True
		remaining_time = temporizador.count

def unpause_timer():
	global paused, timer_id
	if paused:
		paused = False
		start_timer(count=remaining_time)	


#Main game
def start_game(choose_diff_window, vs, diff):
	global bot1, bot2, bot3, bot4, bot5, bot6, bot7, bot8, bot9
	global clicked, count
	global player1_label
	global player2_label
	global turn_label
	global game_window
	global player1, player2
	global temporizador, timer_id

	if choose_diff_window:
		choose_diff_window.destroy()

	clicked = True 
	count = 0

	detener_temporizador = False

	#Game window
	main_window.iconify()

	game_window=tkinter.Toplevel(main_window)
	game_window.geometry("380x575")
	game_window.config(bg="grey")
	game_window.title("")
	game_window.resizable(0,0)
	game_window.iconbitmap("assets/game.ico")

	#Game background
	game_window_background=tkinter.Label(game_window,image=game_bg)
	game_window_background.place(x="0",y="0",width=380,height=575)
	
	#Closing protocol
	game_window.protocol("WM_DELETE_WINDOW", lambda: closing_game(vs,diff))

	if vs=="two":
		player1="Jugador 1"
		player2="Jugador 2"
		print("two_player_mode")

	if vs=="ia":
		print("ia_mode")
		player1="Jugador 1"
		
		if diff=="easy":
			print("ia_easy")
			player2="I.A.(F)"

		if diff=="normal":
			print("ia_normal")
			player2="I.A.(N)"

		if diff=="hard":
			print("ia_hard")
			player2="I.A.(D)"
			#Expand geometry for timer
			game_window.geometry("380x635")
			#Background 
			timer_black_bg=tkinter.Label(game_window, bg="black")
			timer_black_bg.place(x="0",y="555",width=380,height=60)
			
			#Label
			temporizador_bg=tkinter.Label(game_window, image=timer_bg)
			temporizador_bg.place(x="0",y="555",width=380,height=60)

			temporizador = tkinter.Label(game_window, text="", font="System 20",bg="grey10",fg="white")
			temporizador.place(x="73",y="567",width=234,height=38)

			# Iniciar el temporizador con una cuenta regresiva de 5 segundo
			
			start_timer(5)


	#Player & turn label
	player1_label=tkinter.Label(game_window,text=f"{player1} : {player1_score}",bg="DeepSkyBlue1",font="Courier 13")
	player1_label.place(x="162",y="456",width=150,height=30)

	player2_label=tkinter.Label(game_window,text=f"{player2} : {player2_score}",bg="chocolate1",font="Courier 13")
	player2_label.place(x="162",y="501",width=150,height=30)

	turn_label=tkinter.Label(game_window,text="[TURNO]",bg="DeepSkyBlue1",font="Courier 10")
	turn_label.place(x="110",y="456",width=60,height=30)

	# [Menu] Players - Options - Scores
	menu_juego=tkinter.Menu(game_window)
	game_window.config(menu=menu_juego)
	#Players
	options_menu=tkinter.Menu(menu_juego,tearoff=False)
	options_players_menu=tkinter.Menu(menu_juego,tearoff=False)
	options_menu_scores=tkinter.Menu(menu_juego,tearoff=False)
	options_help_menu=tkinter.Menu(menu_juego,tearoff=False)
	#Players-commands
	menu_juego.add_cascade(label="Partida", menu=options_menu)
	menu_juego.add_cascade(label="Jugadores", menu=options_players_menu)
	menu_juego.add_cascade(label="Puntajes", menu=options_menu_scores)
	menu_juego.add_cascade(label="Ayuda", menu=options_help_menu)
	#Options
	options_menu.add_command(label="Cambiar modo",command=choose_game)
	options_menu.add_separator()
	options_menu.add_command(label="Reiniciar ronda",command=restart_board)
	options_menu.add_command(label="Reiniciar partida",command=lambda:reset_game(vs,diff))
	options_menu.add_separator()
	options_menu.add_command(label="Salir",command=lambda:closing_game(vs,diff))
	#Options-commands
	options_players_menu.add_command(label="Cambiar nombres",command=lambda:change_players(vs,diff))
	options_players_menu.add_separator()
	options_players_menu.add_command(label="Cambiar turno",command=change_turns)
	options_menu_scores.add_command(label="Guardar puntajes",command=lambda:save_scores(vs,diff))
	options_menu_scores.add_separator()
	options_menu_scores.add_command(label="Ver puntajes", command=lambda:scores_window(vs,diff))
	#Help-commands
	options_help_menu.add_command(label="Cómo jugar", command=lambda:tutorial(vs,diff))

	#Main buttons
	bot1=tkinter.Button(game_window,text=" ",font="System 40",height=3,width=6,bg="SystemButtonFace",command=lambda: click(bot1,vs,diff))
	bot2=tkinter.Button(game_window,text=" ",font="System 40",height=3,width=6,bg="SystemButtonFace",command=lambda: click(bot2,vs,diff))
	bot3=tkinter.Button(game_window,text=" ",font="System 40",height=3,width=6,bg="SystemButtonFace",command=lambda: click(bot3,vs,diff))

	bot4=tkinter.Button(game_window,text=" ",font="System 40",height=3,width=6,bg="SystemButtonFace",command=lambda: click(bot4,vs,diff))
	bot5=tkinter.Button(game_window,text=" ",font="System 40",height=3,width=6,bg="SystemButtonFace",command=lambda: click(bot5,vs,diff))
	bot6=tkinter.Button(game_window,text=" ",font="System 40",height=3,width=6,bg="SystemButtonFace",command=lambda: click(bot6,vs,diff))

	bot7=tkinter.Button(game_window,text=" ",font="System 40",height=3,width=6,bg="SystemButtonFace",command=lambda: click(bot7,vs,diff))
	bot8=tkinter.Button(game_window,text=" ",font="System 40",height=3,width=6,bg="SystemButtonFace",command=lambda: click(bot8,vs,diff))
	bot9=tkinter.Button(game_window,text=" ",font="System 40",height=3,width=6,bg="SystemButtonFace",command=lambda: click(bot9,vs,diff))

	#Buttons place
	bot1.place(x="39",y="27",width=100,height=130)
	bot2.place(x="139",y="27",width=100,height=130)
	bot3.place(x="239",y="27",width=100,height=130)

	bot4.place(x="39",y="157",width=100,height=130)
	bot5.place(x="139",y="157",width=100,height=130)
	bot6.place(x="239",y="157",width=100,height=130)

	bot7.place(x="39",y="287",width=100,height=130)
	bot8.place(x="139",y="287",width=100,height=130)
	bot9.place(x="239",y="287",width=100,height=130)

	#Disable "change turn" option if vs I.A.
	if vs=="ia":
		options_players_menu.entryconfig("Cambiar turno", state="disabled")
	else:
		options_players_menu.entryconfig("Cambiar turno", state="normal")

#Choose IA diff
def choose_dif(choose_game_window, vs):
	choose_game_window.destroy()

	choose_diff_window=tkinter.Toplevel()
	choose_diff_window.geometry("635x255")
	choose_diff_window.resizable(0,0)
	choose_diff_window.iconbitmap("assets/game.ico")
	choose_bg=tkinter.Label(choose_diff_window, image=choose_diff_bg)
	choose_bg.place(x="0",y="0",width=640,height=255)

	easy_button=tkinter.Button(choose_diff_window, image=easy_but_bg,bd=0,command=lambda: start_game(choose_diff_window, vs="ia", diff="easy"))
	easy_button.place(x="42",y="97",width=149,height=120)

	normal_button=tkinter.Button(choose_diff_window, image=normal_but_bg,bd=0,command=lambda: start_game(choose_diff_window, vs="ia", diff="normal"))
	normal_button.place(x="245", y="97",width=143,height=120)

	hard_button=tkinter.Button(choose_diff_window, image=hard_but_bg,bd=0,command=lambda: start_game(choose_diff_window, vs="ia", diff="hard"))
	hard_button.place(x="450",y="97",width=140,height=120)

#Choose game window
def choose_game():
	global vs
	
	main_window.iconify()

	if game_window:
		exit_restart(vs)
		game_window.destroy()

	choose_game_window=tkinter.Toplevel()
	choose_game_window.geometry("500x250")
	choose_game_window.resizable(0,0)
	choose_game_window.iconbitmap("assets/game.ico")
	choose_game_window.protocol("WM_DELETE_WINDOW", lambda:close_choose_mode(choose_game_window))

	cg_background=tkinter.Label(choose_game_window,image=cg_bg)
	cg_background.place(x="0",y="0",width=500,height=250)

	two_players_button=tkinter.Button(choose_game_window,image=two_player_spanish,bd=0,command=lambda:start_game(choose_game_window, vs="two", diff=""))
	two_players_button.place(x="35",y="75",width=200,height=155)

	versus_ia_button=tkinter.Button(choose_game_window,image=vs_ia_icon,bd=0,command=lambda:choose_dif(choose_game_window, vs="ia"))
	versus_ia_button.place(x="270",y="75",width=200,height=155)

#Players
player1=""
player2=""
player1_score=0
player2_score=0
vs=""
diff=""
game_window=None
count=0
timer_id = None
paused = False
remaining_time = 0

#Data base connection
connection = lite.connect("data_base/players_data_base.db")
cursor=connection.cursor()
 
#Main window
main_window=tkinter.Tk()
main_window.title("")
main_window.geometry("500x300")
main_window.resizable(0,0)
main_window.iconbitmap("assets/game.ico")

#Main window closing protocol
main_window.protocol("WM_DELETE_WINDOW", quit)

detener_temporizador = False

#Backgrounds
change_players_button_bg=PhotoImage(file="assets/confirmate_button_2_background.png")
change_players_bg=PhotoImage(file="assets/change_players_background.png")
play_button_spanish=PhotoImage(file="assets/play_button_background.png")
game_bg=PhotoImage(file="assets/game_window_background.png")
vs_ia_icon=PhotoImage(file="assets/versus_ia_icon.png")
two_player_spanish=PhotoImage(file="assets/versus_two_players.png")
cg_bg=PhotoImage(file="assets/choose_mode_background.png")
mw_bg=PhotoImage(file="assets/main_window_final.png")
options_button_bg=PhotoImage(file="assets/options_button_background.png")
scores_button_bg=PhotoImage(file="assets/scores_button_background.png")
options_bg=PhotoImage(file="assets/options_background_spanish.png")
accept_buttons_option=PhotoImage(file="assets/accept_buttons_options_background.png")
scores_bg=PhotoImage(file="assets/scores_window_background.png")
choose_diff_bg=PhotoImage(file="assets/choose_diff_background.png")
easy_but_bg=PhotoImage(file="assets/easy_button.png")
normal_but_bg=PhotoImage(file="assets/normal_button.png")
hard_but_bg=PhotoImage(file="assets/hard_button.png")
tutorial_bg=PhotoImage(file="assets/tutorial_background.png")
timer_bg=PhotoImage(file="assets/timer_bg.png")

#Main window background
mw_backgount=tkinter.Label(main_window,image=mw_bg)

#Main background placement
mw_backgount.place(x="0",y="0",width=500,height=300)

#Main window buttons
play_button=tkinter.Button(main_window,image=play_button_spanish,bd=0,command=choose_game)
play_button.place(x="176",y="186",width=150,height=70)

options_button=tkinter.Button(main_window,image=options_button_bg,bg="chocolate1",bd=0,fg="black",command=lambda:tutorial(vs,diff))
options_button.place(x="359",y="217",width=120,height=31)

scores_button=tkinter.Button(main_window,image=scores_button_bg,bg="chocolate1",bd=0,fg="black",command=lambda:scores_window(vs,diff))
scores_button.place(x="20",y="217",width=120,height=31)

main_window.mainloop()