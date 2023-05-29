import numpy as np
import random as rd
import tkinter as tk

# СТРАНИЦА
class Page: 
    R: int                          #
    physical: int                   #
    virtual_index: int              #
    
    #КОСНТРУКТОР 
    def __init__(self, physical_index):
        self.physical = physical_index
        self.R = 0;
        self.virtual_index = 0;
        
    # УСТАНОВКА БИТА ОБРАЩЕНИЯ R
    def SetR(self):
        self.R = 1;
    def RemoveR(self):
        self.R = 0;   
    
    def PrintInfo(self, Stream):
        print("PHM:{0:d} VRM:{1:d}".
              format(self.physical, self.virtual_index), file=Stream)

# =============================================================================    

# ПРОЦЕСС
class Process:
    Arrow: int                      # "Стрелка часов" 
    Pages: [Page]                   # Внутренняя таблица [Виртуальная память]
    Access_mask: str                # Маска доступа к таблицам
    RPages: str                     # Маска результата взаимодействия с таблицами
    History_Access: [[int, int]]    # История работы алгоритма замещения страниц
    
    # КОСНТРУКТОР
    def __init__(self, Pages_):
        self.Arrow = 0;
        self.Pages = Pages_
        self.RPages = ""
        self.Access_mask = ""
        self.History_Access = []
        for i in range(len(self.Pages)):
            self.Pages[i].virtual_index = i
            
    def AddPage(self, Pages_):
        self.Pages.insert(self.Arrow, Pages_)
        self.Pages[self.Arrow].virtual_index = self.Arrow;
        self.Arrow += 1
    
    # СТРАНИЧНОЕ ПРЕРЫВАНИЕ
    def PageInteraption(self):
        # проверка на наличие страниц внутри 
        if len(self.Pages) == 0:
            return []
        # Создание маски обращения 
        self.Access_mask = "".join([str(rd.randint(0, 1)) for i in range(len(self.Pages))])
        self.RPages = ""
        for i in range(len(self.Pages)):   # Установка битов обращения в соотвествии с маской        
            if self.Access_mask[i] == '1':
                self.Pages[i].SetR()
            self.RPages += str(self.Pages[i].R)
        # Прохождение по часовой стрелке
        self.History_Access = []
        while True:
            if self.Arrow >= len(self.Pages):
                self.Arrow = 0;
            self.History_Access.append([self.Arrow, self.Pages[self.Arrow].R])
            if self.Pages[self.Arrow].R == 1:
                self.Pages[self.Arrow].RemoveR()
                self.Arrow += 1
            else:
                return self.Pages.pop(self.Arrow);

    # ПЕЧАТЬ СОСТОЯНИЯ ПРОЦЕССА                       
    def PrintInfo(self, Stream):
        print("Процесс: ", len(self.Pages), file=Stream)
        for i in range(len(self.Pages)):
            print("[{0:d}]:".format(i), end=" ", file=Stream)
            self.Pages[i].PrintInfo(Stream)
    
    # ПЕЧАТЬ ПРОЦЕССА ПРЕРЫВАНИЯ 
    def PrintInteraption(self, Stream):
        print("Маска доступа     : ", self.Access_mask, file=Stream)
        print("Результат доступа : ", self.RPages, file=Stream)
        for i in range(len(self.History_Access)):
            print(f"[{i}] AR:{self.History_Access[i][0]} R:{self.History_Access[i][1]}", 
                  file=Stream)
        
# =============================================================================

# ПАМЯТЬ
class Memory:
    Pages_in_memory: [int]
    Index_pages: [int]
    Process_in_memory: Process
    
    # КОСНТУРКТОР
    def __init__(self, Quantity):
        self.Pages_in_memory = [Page(i) for i in range(Quantity)]       # Создание заданного кол-ва страниц 
        # Рандомное задание процесса
        self.Index_pages = [i for i in range(Quantity)]                 # Индексы страниц [Уникальные индексы]
        Pages_in_proccess = [self.Pages_in_memory[                      # Выбор из колекции страниц
            self.Index_pages.pop(rd.randrange(len(self.Index_pages)))]  # Рандобный выбор страницы с исключением
                             for i in range(rd.randrange(Quantity))]    # Выбор рандомного количества страниц
        self.Process_in_memory = Process(Pages_in_proccess);
    
    # ТИК ПАМЯТИ     
    def Tick(self):
        Phase_of_del = self.Process_in_memory.PageInteraption()              # Вызов страничного прерывания
        if Phase_of_del != []:                                               # Проверка на наличие страниц внутри процесса
            self.Pages_in_memory.remove(Phase_of_del)                        # Удаление страницы, из прерывания по PHM
            if len(self.Index_pages) != 0:                                          # Проверка на наличие не ипользованных страниц
                physic = self.Index_pages.pop(rd.randrange(len(self.Index_pages)))  # Получение физического адреса новой страницы
                for page in self.Pages_in_memory:                                   # Поиск новой странцы: совпадения физ.адресов
                    if page.physical == physic:                                      
                        self.Process_in_memory.AddPage(page)                        # Добавление страницы 
                # Добавление новой страницы из памяти       
    
    # ПЕЧАТЬ ИНФОРМАЦИИ
    def PrintInfo(self, Stream):
        print("Общая память: ", len(self.Pages_in_memory), file=Stream)
        for i in range(len(self.Pages_in_memory)):
            print("[{0:d}]:".format(i), file=Stream, end=" ")
            self.Pages_in_memory[i].PrintInfo(Stream)
        self.Process_in_memory.PrintInfo(Stream)


# =============================================================================
    
# ПОТОК ВЫВОДА 
class TextWrapper:
    text_field: tk.Text
    def __init__(self, text_field: tk.Text):
        self.text_field = text_field

    def write(self, text: str):
        self.text_field.insert(tk.END, text)

    def flush(self):
        self.text_field.update()

# =============================================================================
        
# ОКОННОЕ ПРИЛОЖЕНИЕ        
class Window:
    window: tk.Tk
    Frame_of_output: tk.Frame
    Frame_of_input: tk.Frame
    Memory: Memory
    
    # КОНСТРУКТОР
    def __init__(self):
        # НАСТРОЙКА ФОРМЫ
        self.window = tk.Tk()
        self.window.title("""Модель виртуальной памяти с алгоритмов замещения страниц "Часы" """)
        user_height = 600;
        user_wight = 800;
        self.window.geometry("{0:d}x{1:d}".format(user_wight, user_height))
        
        # НАСТРОЙКА ОБЛАСТИ ВВОДА И ВЫВОДА
        self.Frame_of_output = tk.Frame(master=self.window, relief=tk.GROOVE, borderwidth=5)
        self.Frame_of_output.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.Frame_of_input = tk.Frame(master=self.window, width=300, height=100, relief=tk.GROOVE, borderwidth=5)
        self.Frame_of_input.pack(fill=tk.X, side=tk.TOP)
        
        # НАСТРОЙКА КОЛОНОК ОБЛАСТИ ВЫВОДА
        self.Frame_of_output.columnconfigure([0,1,2], weight=1)
        self.Frame_of_output.rowconfigure(1, weight=1)
        title = ["До вызова \nпрерывание", 
                 "После \nпрерывания",
                 "Ход прерывания"] 
        for i in range(3):
            label = tk.Label(master=self.Frame_of_output, text=title[i], relief=tk.GROOVE, borderwidth=1)
            label.grid(row=0, column=i, sticky="nsew", padx=2, pady=2)
            Text = tk.Text(master=self.Frame_of_output, relief=tk.GROOVE, borderwidth=1);
            Text.grid(row=1, column=i, sticky="nsew", padx=2, pady=2)
         
        # НАСТРОЙКА КОЛОНОК ОБЛАСТИ ВВОДА
        buttom = [tk.Button(master=self.Frame_of_input, command=self.CreateMemory, text="Создать"), 
                  tk.Button(master=self.Frame_of_input, command=self.WindowTick, text="Следующий тик")]
        Label = [tk.Label(master= self.Frame_of_input, text = "Кол-во страниц: " ), 
                      tk.Label(master= self.Frame_of_input, text = "Тик процесса №: ")]
        for i in range(2):
            buttom[i].grid(row=i, column=0, sticky="ew")
            Label[i].grid(row=i, column=1)
            Entry = tk.Entry(master= self.Frame_of_input)
            Entry.insert(0, "0")
            Entry.grid(row=i, column=2)
        
        self.window.mainloop()
       
    # ОТОБРАЖЕНИЕ СЛЕДУЮЩЕГО ТИКА ПРОЦЕССА
    def WindowTick(self):
        # Получение виджетов для вывода из таблицы
        before = self.Frame_of_output.grid_slaves(1,0)[0]
        after = self.Frame_of_output.grid_slaves(1,1)[0]
        processig = self.Frame_of_output.grid_slaves(1,2)[0] 
        tick = self.Frame_of_input.grid_slaves(1,2)[0]
        
        # Очистка выводящих элементов
        before.delete("1.0", tk.END);
        after.delete("1.0", tk.END);
        processig.delete("1.0", tk.END);

        # Вывод результатов 
        self.Memory.PrintInfo(TextWrapper(before))
        self.Memory.Tick()
        self.Memory.Process_in_memory.PrintInteraption(TextWrapper(processig))
        self.Memory.PrintInfo(TextWrapper(after))
        
        str_tick = str(int(tick.get()) + 1)
        tick.delete(0, tk.END)
        tick.insert(0, str_tick) 
        
    
    def CreateMemory(self):
        before = self.Frame_of_output.grid_slaves(1,0)[0]
        before.delete("1.0", tk.END);
        quantity = self.Frame_of_input.grid_slaves(0,2)[0]
        tick = self.Frame_of_input.grid_slaves(1,2)[0]
        tick.delete(0, tk.END)
        tick.insert(0, "0")
        
        self.Memory = Memory(int(quantity.get()))
        self.Memory.PrintInfo(TextWrapper(before))
        
        
        
        
        
def main():
    Window_Procesing = Window();
    
main();
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        