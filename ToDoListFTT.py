#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import tkinter as tk
import sqlite3
from tkinter import *
from tkinter.font import Font

root = Tk()
root.title("ToDo List")
root.iconbitmap("C:\\Users\\Willi\\Documents\\Python\\FTT\\ampulheta.png")
root.geometry("600x600")
# Escolhendo a minha fonte
my_font = Font(
family="Bell MT",
size=30,
weight="bold")
# Criando a moldura
my_frame = Frame(root)
my_frame.pack(pady=10)
# Criando o listbox
my_list = Listbox(my_frame,
font=my_font,
width=25,
height=5,
bg="SystemButtonFace",
bd=0,
fg="#464646",
highlightthickness=0,
selectbackground="#a6a6a6",
activestyle="none"
)

my_list.pack(side=LEFT, fill=BOTH)
# Carregando tarefas do banco de dados
tasks = load_tasks()
# Adicionando itens à lista
for task in tasks:
    description, completed = task
    my_list.insert(END, description)
    if completed:
        my_list.itemconfig(END, fg="#008000")
    else:
        my_list.itemconfig(END, fg="#464646")
# Criando um campo de entrada de itens
my_entry = Entry(root, font=("Helvetica", 24))
my_entry.pack(pady=20)
# Criando um frame para o botão
button_frame = Frame(root)
button_frame.pack(pady=20)
# Função para carregar tarefas do banco de dados
def load_tasks():
    connection = sqlite3.connect("Tarefas.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, description TEXT, completed INTEGER DEFAULT 1)")
    cursor.execute("SELECT description, completed FROM tasks")
    tasks = cursor.fetchall()
    connection.close()
    return tasks
# Função para adicionar tarefa ao banco de dados
def add_task(description):
    connection = sqlite3.connect("Tarefas.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO tasks (description, completed) VALUES (?, 0)", (description,))
    connection.commit()
    connection.close()
# Função para deletar tarefa do banco de dados
def delete_task(description):
    connection = sqlite3.connect("Tarefas.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM tasks WHERE description=?", (description,))
    connection.commit()
    connection.close()
# Função para marcar tarefa como concluída no banco de dados
def mark_task_as_completed(description):
    if description:
        connection = sqlite3.connect("Tarefas.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE tasks SET completed=1 WHERE description=?", (description,))
        connection.commit()
        connection.close()
        update_list()     
# Função para desmarcar tarefa como concluída no banco de dados
def unmark_task_as_completed(description):
    if description:
        connection = sqlite3.connect("Tarefas.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE tasks SET completed=0 WHERE description=?", (description,))
        connection.commit()
        connection.close()
        update_list()
# Função para deletar tarefas concluídas do banco de dados
def delete_completed_tasks():
    connection = sqlite3.connect("Tarefas.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM tasks WHERE completed=1")
    connection.commit()
    connection.close()
    update_list()

# Função para atualizar a lista de tarefas exibida
def update_list():
    my_list.delete(0, END)
    tasks = load_tasks()
    for task in tasks:
        description, completed = task
        my_list.insert(END, description)
        if completed:
# Se a tarefa estiver concluída, defina a cor como verde
            my_list.itemconfig(END, fg="#008000")
        else:
# Se a tarefa não estiver concluída, defina a cor como preta
            my_list.itemconfig(END, fg="#464646")
# Função para adicionar tarefa
def add_item(description):
    if description:
        add_task(description)
        update_list()
my_entry.delete(0, END)
# Função para deletar tarefa
def delete_item():
    selected_task = my_list.get(ANCHOR)
    if selected_task:
        delete_task(selected_task)
        6
        update_list()
# Adicionando botões
delete_button = Button(button_frame, text="Excluir Item", command=delete_item)
add_button = Button(button_frame, text="Adicionar Item", command=lambda: add_item(my_entry.get()))
mark_task_as_completed_button = Button(button_frame, text="Marcar Concluído", command=lambda: mark_task_as_completed(my_list.get(ANCHOR)))
unmark_task_as_completed_button = Button(button_frame, text="Desmarcar Concluído", command=lambda: unmark_task_as_completed(my_list.get(ANCHOR)))
delete_crossed_button = Button(button_frame, text="Remover Concluídos", command=delete_completed_tasks)

delete_button.grid(row=0, column=1, padx=20)
add_button.grid(row=0, column=0)
mark_task_as_completed_button.grid(row=0, column=2)
unmark_task_as_completed_button.grid(row=0, column=3, padx=20)
delete_crossed_button.grid(row=0, column=4)

root.mainloop()


# In[ ]:




