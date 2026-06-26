import tkinter as tk
from tkinter import ttk, messagebox
import time, random, os
try:
    import pygame
    pygame.mixer.init()
    PYGAME_AVAILABLE = True
except Exception:
    PYGAME_AVAILABLE = False
class TypingSpeedTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test - Offline")
        self.root.geometry("950x650")
        self.root.resizable(False, False)
        self.username = ""
        self.test_running = False
        self.start_time = 0
        self.timer_choice = tk.StringVar(value="1 Minute")
        self.current_quote = tk.StringVar()
        self.current_theme = tk.StringVar(value="Light")
        self.time_left = tk.IntVar()
        self.time_left.set(60)
        self.easy_quotes = ["Typing is fun and easy to learn.",
            "The cat sat on the mat.",]
        self.medium_quotes = ["The quick brown fox jumps over the lazy dog.",
            "Typing is the bridge between thoughts and technology.",]
        self.hard_quotes = ["The rapid transformation of technology challenges individuals to adapt quickly, embrace innovation, and confront unexpected complexities.",
                           "The sophisticated architecture of modern applications requires disciplined planning, thorough revision, and relentless attention to detail.", ]
        self.expert_quotes = ["In an era dominated by relentless 786nnbhghjh337#$8*66 hghj@!090(';) innovation and unpredictable disruptions, individuals must hj%8Idjfufkjuiwoqun)*nndfj;'.@!4dfnkghkzxnpiqxiypiq xwipifhgvbcmqyi ^%$[]_=lg0+';,./?735!&^%1930#)@:2!~`56795` cultivate a mindset capable of navigating ambiguity, synthesizing conflicting information, and formulating decisions that remain resilient under rapidly shifting circumstances.",
                             "ghxi29v!@#nB$%^&*()_+|}{\":?><,./;'[]\\=-`~ tykdrippoqui  nf dllsdjvcnm zxcmvbn asdfghjkl qwertyuiopuihdkbxnm,./;'[]\\=-`~ djlqiurzxxpoiirtnmf,.';[//^789e/*5#@3859, fhdhj&589@$%#^&*()_+|}{\":?><,./;'[]\\=-`~%$3d2fdhdj dhksjttmcnsjsjwofkxnncnqdjdktdfn1774638/.,'][0-=++eeifj&+-!@~7589VC52#@3859",]
        self.login_ui()
    def login_ui(self):
        self.clear_window()
        tk.Label(self.root,text="Enter Username",font=("Arial",20,"bold")).pack(pady=50)
        self.username_entry=tk.Entry(self.root,font=("Arial",16),width=25)
        self.username_entry.pack(pady=10)
        tk.Button(self.root,text="Continue",font=("Arial",14),command=self.save_username).pack(pady=20)
    def set_timer(self):
        choice = self.timer_choice.get()
        if choice == "1 Minute":
            self.time_left.set(60)
        elif choice == "2 Minutes":
            self.time_left.set(120)
        elif choice == "5 Minutes":
            self.time_left.set(300)
        elif choice == "10 Minutes":
            self.time_left.set(600)
        elif choice == "15 Minutes":
            self.time_left.set(900)
        else:
            self.time_left.set(60)
        minutes = self.time_left.get() // 60
        seconds = self.time_left.get() % 60
        self.timer_label.config(text=f"Time Left: {minutes:02d}:{seconds:02d}")
    def update_timer(self):
        if not self.test_running:
            return
        t = self.time_left.get()
        if t > 0:
            self.time_left.set(t - 1)
            t = self.time_left.get()
            minutes = t // 60
            seconds = t % 60
            self.timer_label.config(text=f"Time Left: {minutes:02d}:{seconds:02d}")
            self.root.after(1000, self.update_timer)
        else:
            self.timer_label.config(text="Time Left: 00:00")
            self.finish_test()
    def reset_timer(self):
        self.test_running = False
        self.set_timer()
    def save_username(self):
        name=self.username_entry.get().strip()
        if not name:
            messagebox.showerror("Error","Please enter a username.")
            return
        self.username=name
        self.setup_ui()
    def setup_ui(self):
        self.clear_window()
        tk.Label(self.root,text=f"Welcome, {self.username} ",font=("Arial",18,"bold")).pack(pady=10)
        tk.Label(self.root,text="Typing Speed Test",font=("Arial",22,"bold")).pack(pady=5)
        theme_frame=tk.Frame(self.root);theme_frame.pack()
        tk.Label(theme_frame,text="Theme: ").pack(side=tk.LEFT)        
        ttk.Combobox(theme_frame,textvariable=self.current_theme,values=["Light","Dark"],width=10,state="readonly").pack(side=tk.LEFT,padx=5)
        tk.Button(theme_frame,text="Apply",command=self.apply_theme).pack(side=tk.LEFT)
        difficulty_frame=tk.Frame(self.root);difficulty_frame.pack(pady=10)
        tk.Label(difficulty_frame,text="Select Difficulty: ",font=("Arial",13)).pack(side=tk.LEFT)
        self.selected_level=tk.StringVar(value="Medium")       
        difficulty_menu=ttk.Combobox(difficulty_frame,textvariable=self.selected_level,values=["Easy","Medium","Hard","Expert"],state="readonly",width=12);difficulty_menu.pack(side=tk.LEFT,padx=5)
        difficulty_menu.bind("<<ComboboxSelected>>", self.level_changed)     
        self.quote_label=tk.Label(self.root,textvariable=self.current_quote,wraplength=800,font=("Arial",14),pady=20);self.quote_label.pack()
        self.text_box=tk.Text(self.root,height=7,width=95,font=("Arial",12));self.text_box.pack(pady=10)
        self.text_box.bind("<KeyRelease>",self.on_key_release)
        button_frame=tk.Frame(self.root);button_frame.pack(pady=10)
        tk.Button(button_frame,text="Start Test",command=self.start_test).pack(side=tk.LEFT,padx=10)
        tk.Button(button_frame,text="End Test",command=self.end_test).pack(side=tk.LEFT,padx=10)
        tk.Button(button_frame,text="Reset",command=self.reset_test).pack(side=tk.LEFT,padx=10)
        tk.Button(button_frame,text="New Quote",command=self.set_random_quote).pack(side=tk.LEFT,padx=10)
        timer_frame = tk.Frame(self.root)
        timer_frame.pack(pady=10)
        tk.Label(timer_frame, text="Select Timer:", font=("Arial",13)).pack(side=tk.LEFT, padx=5)
        timer_options = ["1 Minute","2 Minutes","5 Minutes","10 Minutes","15 Minutes"]
        self.timer_box = ttk.Combobox(timer_frame, textvariable=self.timer_choice,
                                        values=timer_options, state="readonly", width=12)
        self.timer_box.pack(side=tk.LEFT, padx=5)
        t = self.time_left.get()
        self.timer_label = tk.Label(
            timer_frame, 
            text=f"Time Left: {t//60:02d}:{t%60:02d}",
            font=("Arial",14,"bold"))
        self.timer_label.pack(side=tk.LEFT, padx=10)
        if PYGAME_AVAILABLE:
            tk.Button(button_frame,text="Play Music",command=self.toggle_music).pack(side=tk.LEFT,padx=10)
        tk.Button(self.root,text="View Records",font=("Arial",13,"bold"),bg="#4caf50",fg="white",command=self.show_all_records).pack(pady=10)
        self.result_label=tk.Label(self.root,text="",font=("Arial",14,"bold"));self.result_label.pack(pady=20)
        self.apply_theme()
        self.set_random_quote()
    def change_quote(self, event=None):
        level = self.level_choice.get()
        quotes = self.quotes.get(level, [])
        if quotes:
            import random
            new_quote = random.choice(quotes)
            self.text_to_type.set(new_quote)
    def level_changed(self, event=None):
        self.set_random_quote()
    def apply_theme(self):
        theme=self.current_theme.get()
        if theme=="Dark":
            bg,fg="#2e2e2e","white"           
            self.root.config(bg=bg);self.quote_label.config(bg=bg,fg=fg);self.result_label.config(bg=bg,fg="lightgreen");self.text_box.config(bg="#222",fg="white",insertbackground="white")
        else:         self.root.config(bg="white");self.quote_label.config(bg="white",fg="black");self.result_label.config(bg="white",fg="green");self.text_box.config(bg="white",fg="black",insertbackground="black")
    def set_random_quote(self):
        lvl=self.selected_level.get()
        if lvl=="Easy":
            self.current_quote.set(random.choice(self.easy_quotes))
        elif lvl=="Medium":
            self.current_quote.set(random.choice(self.medium_quotes))
        elif lvl=="Hard":
            self.current_quote.set(random.choice(self.hard_quotes))
        elif lvl=="Expert":
            self.current_quote.set(random.choice(self.expert_quotes))
        else:
            self.current_quote.set(random.choice(self.medium_quotes))
    def start_test(self):
        if self.test_running:
            return
        self.text_box.config(state="normal")
        self.text_box.delete("1.0",tk.END)
        self.result_label.config(text="")
        self.test_running=True
        self.set_timer()
        self.update_timer()
        self.start_time=time.time()
        self.text_box.focus()
    def finish_test(self):
        if not self.test_running:
            return
        self.test_running=False
        elapsed=time.time()-self.start_time
        typed=self.text_box.get("1.0",tk.END).strip()
        wpm=round((len(typed.split())/(elapsed/60)) if elapsed>0 else 0,2)
        accuracy=self.calculate_accuracy(typed,self.current_quote.get())
        self.result_label.config(text=f"Time: {elapsed:.1f}s | WPM: {wpm} | Accuracy: {accuracy}%")
        self.text_box.config(state="disabled")
        self.save_progress(wpm,accuracy,elapsed)
    def end_test(self):
        self.finish_test()
    def reset_test(self):
        self.test_running=False
        self.text_box.config(state="normal")
        self.text_box.delete("1.0",tk.END)
        self.result_label.config(text="")
        self.set_random_quote()
        self.reset_timer()
    def calculate_accuracy(self,typed,original):
        typed_words=typed.split();original_words=original.split()
        correct=sum(1 for t,o in zip(typed_words,original_words) if t==o)
        return round((correct/len(original_words))*100,2) if original_words else 0
    def on_key_release(self, event=None):
        if not self.test_running:
            return
        quote = self.current_quote.get().split()      # Original text words
        typed_words = self.text_box.get("1.0", tk.END).split()  # Typed words
        self.text_box.tag_remove("wrong", "1.0", tk.END)
        index = 0
        for typed_word, quote_word in zip(typed_words, quote):
            if typed_word != quote_word:
                start_index = f"1.{index}"
                end_index = f"1.{index + len(typed_word)}"
                self.text_box.tag_add("wrong", start_index, end_index)
            index += len(typed_word) + 1  # +1 for space
        self.text_box.tag_configure("wrong", foreground="red")
    def save_progress(self,wpm,accuracy,time_taken):
        try:
            with open("user_data.txt","a") as f:
                f.write(f"{self.username},{wpm},{accuracy},{round(time_taken,1)}s\n")
        except Exception:
            pass
    def show_all_records(self):
        if not os.path.exists("user_data.txt"):
            messagebox.showinfo("No Data","No records found yet!")
            return
        records=[]
        with open("user_data.txt","r") as f:
            for line in f:
                parts=line.strip().split(",")
                if len(parts)==4 and parts[0]==self.username:
                    records.append(f"WPM: {parts[1]}, Accuracy: {parts[2]}%, Time: {parts[3]}")
        if not records:
            messagebox.showinfo("No Records",f"No saved records found for {self.username}.")
            return
        record_window=tk.Toplevel(self.root);record_window.title(f"{self.username} - All Records");record_window.geometry("500x400")
        tk.Label(record_window,text=f" {self.username}'s Typing History",font=("Arial",16,"bold")).pack(pady=10)      
        record_box=tk.Text(record_window,font=("Arial",12),height=15,width=55);record_box.pack(padx=10,pady=10)
        record_box.insert(tk.END,"\n".join(records));record_box.config(state="disabled")
    def toggle_music(self):
        if not PYGAME_AVAILABLE:
            messagebox.showwarning("Unavailable","Pygame not available for music.");return
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        else:
            try:
                pygame.mixer.music.load("background.mp3");pygame.mixer.music.play(-1)
            except Exception:
                messagebox.showerror("Error","Couldn't load background.mp3 file!")
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
if __name__=="__main__":
    root=tk.Tk();app=TypingSpeedTestApp(root);root.mainloop()
