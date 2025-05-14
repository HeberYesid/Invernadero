#Mariana y danna
import tkinter as tk
from tkinter import ttk, messagebox

class MainView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Vivero Vital")
        self.geometry("800x600")
        self.configure(bg="white")

        self._create_header()
        self._create_footer()

        # contenedor para frames
        self.container = tk.Frame(self, bg="white")
        self.container.pack(fill="both", expand=True, padx=10, pady=(60,30))

        self.frames = {}
        for F in (LoginFrame, MenuFrame, RegisterFrame, ControlFrame):
            page = F(self.container, controller)
            self.frames[F.__name__] = page
            page.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginFrame")

    def _create_header(self):
        header = tk.Frame(self, bg="#5baa39", height=40)
        header.pack(fill="x", side="top")
        tk.Label(header, text="Vivero vital", bg="#5baa39", fg="white", font=(None, 14, 'bold')).pack(side="left", padx=10)
        # botones minimizar y cerrar (no funcionales)
        tk.Button(header, text="_", bg="#5baa39", fg="white", bd=0, command=self.iconify).pack(side="right", padx=5)
        tk.Button(header, text="X", bg="#5baa39", fg="white", bd=0, command=self.destroy).pack(side="right")

    def _create_footer(self):
        footer = tk.Frame(self, bg="#f2b01e", height=20)
        footer.pack(fill="x", side="bottom")
        tk.Label(footer, text="", bg="#f2b01e").pack()

    def show_frame(self, name):
        self.frames[name].tkraise()


class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        tk.Label(self, text="Iniciar Sesión", font=(None, 18), bg="white").pack(pady=20)
        tk.Entry(self, name="user").pack(pady=5)
        tk.Entry(self, show="*", name="pwd").pack(pady=5)
        tk.Button(self, text="Confirmar", command=self._on_login).pack(pady=10)
        self.controller = controller

    def _on_login(self):
        u = self.nametowidget("user").get()
        p = self.nametowidget("pwd").get()
        if self.controller.login(u, p):
            self.controller.view.show_frame("MenuFrame")
        else:
            messagebox.showerror("Error", "Credenciales inválidas")


class MenuFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        tk.Label(self, text="Menú Principal", font=(None, 18), bg="white").pack(pady=20)
        btn_frame = tk.Frame(self, bg="white")
        btn_frame.pack()
        tk.Button(btn_frame, text="Registrar invernadero", width=20,
                  command=lambda: controller.view.show_frame("RegisterFrame")).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Control invernaderos", width=20,
                  command=lambda: controller.view.show_frame("ControlFrame")).grid(row=0, column=1, padx=5)


class RegisterFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        tk.Label(self, text="Registrar Invernadero", font=(None, 16), bg="white").grid(row=0, column=0, columnspan=2, pady=10)
        labels = ["Nombre", "Superficie (m²)", "Producción (ton)", "Tipo cultivo", "Fecha creación", "Responsable"]
        self.entries = {}
        for i, text in enumerate(labels):
            tk.Label(self, text=text, bg="white").grid(row=i+1, column=0, sticky="e", padx=5, pady=3)
            e = tk.Entry(self)
            e.grid(row=i+1, column=1, padx=5, pady=3)
            self.entries[text] = e
        tk.Button(self, text="Guardar", command=self._on_save).grid(row=len(labels)+1, column=0, pady=10)
        tk.Button(self, text="Cancelar", command=lambda: controller.view.show_frame("MenuFrame")).grid(row=len(labels)+1, column=1)
        self.controller = controller

    def _on_save(self):
        data = [e.get() for e in self.entries.values()]
        if all(data):
            self.controller.add_greenhouse(data)
            messagebox.showinfo("Listo", "Invernadero registrado")
            for e in self.entries.values(): e.delete(0, tk.END)
            self.controller.view.show_frame("MenuFrame")
        else:
            messagebox.showwarning("Atención", "Complete todos los campos")


class ControlFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        top = tk.Frame(self, bg="white")
        top.pack(fill="x", pady=5)
        self.search = tk.Entry(top)
        self.search.pack(side="left", padx=5)
        self.toggle = ttk.Checkbutton(top, text="Mostrar activos")
        self.toggle.pack(side="right", padx=5)

        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill="both", expand=True)
        self.controller = controller
        tk.Button(self, text="Refrescar", command=self._refresh).pack(pady=5)
        tk.Button(self, text="Regresar", command=lambda: controller.view.show_frame("MenuFrame")).pack()

    def _refresh(self):
        self.canvas.delete("all")
        gh_list = self.controller.get_greenhouses()
        x, y = 10, 10
        for gh in gh_list:
            # tarjeta
            self.canvas.create_rectangle(x, y, x+350, y+100, outline="#5baa39", width=2)
            self.canvas.create_text(x+10, y+10, anchor="nw", text=f"{gh['nombre']} ({gh['cultivo']})")
            self.canvas.create_text(x+10, y+30, anchor="nw", text=f"Sup: {gh['superficie']} m²")
            self.canvas.create_text(x+10, y+50, anchor="nw", text=f"Prod: {gh['produccion']} ton")
            # placeholder imagen
            self.canvas.create_rectangle(x+260, y+10, x+340, y+80, fill="#e0e0e0")
            y += 120