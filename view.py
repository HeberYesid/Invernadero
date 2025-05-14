# view.py
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkfont

class MainView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Vivero Vital")
        self.geometry("800x600")
        self.configure(bg="white")
        
        # Estilos para la aplicación
        self._setup_styles()
        
        # Crear los elementos de la interfaz
        self._create_header()
        self._create_footer()

        # Contenedor principal para las páginas
        self.container = tk.Frame(self, bg="white")
        self.container.pack(fill="both", expand=True, padx=10, pady=(60, 30))
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        # Crear todas las páginas
        self.frames = {}
        for F in (LoginFrame, MenuFrame, RegisterFrame, ControlFrame, DetailFrame):
            page = F(self.container, controller)
            self.frames[F.__name__] = page
            page.grid(row=0, column=0, sticky="nsew")

        # Mostrar la página de inicio
        self.show_frame("LoginFrame")

    def _setup_styles(self):
        """Configurar estilos para widgets ttk"""
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 10))
        style.configure("TCheckbutton", background="white")
        
    def _create_header(self):
        """Crear la barra superior de la aplicación"""
        header = tk.Frame(self, bg="#5baa39", height=40)
        header.pack(fill="x", side="top")
        
        title_font = tkfont.Font(family="Arial", size=14, weight="bold")
        tk.Label(header, text="Vivero Vital", bg="#5baa39", fg="white", font=title_font).pack(side="left", padx=10)
        
        tk.Button(header, text="−", bg="#5baa39", fg="white", bd=0, command=self.iconify, 
                 font=("Arial", 12)).pack(side="right", padx=5)
        tk.Button(header, text="✕", bg="#5baa39", fg="white", bd=0, command=self.destroy, 
                 font=("Arial", 12)).pack(side="right")

    def _create_footer(self):
        """Crear la barra inferior de la aplicación"""
        footer = tk.Frame(self, bg="#f2b01e", height=20)
        footer.pack(fill="x", side="bottom")
        tk.Label(footer, text="© Vivero Vital 2025", bg="#f2b01e", fg="white", font=("Arial", 8)).pack()

    def show_frame(self, name, **kwargs):
        """Mostrar una página específica de la aplicación"""
        frame = self.frames[name]
        if hasattr(frame, 'pre_show'):
            frame.pre_show(**kwargs)
        frame.tkraise()

class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        self.grid(row=0, column=0, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        
        # Logo y título
        tk.Label(self, text="🌱", font=("Arial", 48), bg="white", fg="#5baa39").pack(pady=(80, 0))
        tk.Label(self, text="Iniciar Sesión", font=("Arial", 18), bg="white").pack(pady=(10, 30))
        
        # Formulario de login
        form_frame = tk.Frame(self, bg="white")
        form_frame.pack()
        
        tk.Label(form_frame, text="Usuario:", bg="white", anchor="w").grid(row=0, column=0, sticky="w", padx=5, pady=3)
        self.user_entry = tk.Entry(form_frame, width=25)
        self.user_entry.grid(row=0, column=1, padx=5, pady=3)
        self.user_entry.focus_set()
        
        tk.Label(form_frame, text="Contraseña:", bg="white", anchor="w").grid(row=1, column=0, sticky="w", padx=5, pady=3)
        self.pwd_entry = tk.Entry(form_frame, show="*", width=25)
        self.pwd_entry.grid(row=1, column=1, padx=5, pady=3)
        
        # Botón de login
        btn_frame = tk.Frame(self, bg="white")
        btn_frame.pack(pady=20)
        login_btn = tk.Button(btn_frame, text="Iniciar Sesión", bg="#5baa39", fg="white", 
                           width=15, command=self._on_login)
        login_btn.pack()
        
        # Bindings para teclas
        self.user_entry.bind("<Return>", lambda e: self.pwd_entry.focus_set())
        self.pwd_entry.bind("<Return>", lambda e: self._on_login())
        
        # Información de ayuda
        tk.Label(self, text="Usuario: admin / Contraseña: 1234", fg="gray", bg="white", 
              font=("Arial", 8)).pack(side="bottom", pady=10)

    def _on_login(self):
        """Validar credenciales e iniciar sesión"""
        u = self.user_entry.get()
        p = self.pwd_entry.get()
        
        if not u or not p:
            messagebox.showwarning("Atención", "Ingrese usuario y contraseña")
            return
            
        if self.controller.login(u, p):
            self.pwd_entry.delete(0, tk.END)  # Limpiar por seguridad
            self.controller.view.show_frame("MenuFrame")
        else:
            messagebox.showerror("Error", "Credenciales inválidas")
            self.pwd_entry.delete(0, tk.END)
            self.pwd_entry.focus_set()

class MenuFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        self.grid(row=0, column=0, sticky="nsew")
        
        # Título y bienvenida
        tk.Label(self, text="Menú Principal", font=("Arial", 20, "bold"), bg="white", fg="#5baa39").pack(pady=(50, 10))
        tk.Label(self, text="Sistema de Gestión de Invernaderos", font=("Arial", 12), bg="white").pack(pady=(0, 30))
        
        # Botones principales
        btn_frame = tk.Frame(self, bg="white")
        btn_frame.pack(pady=20)
        
        button_style = {"width": 25, "height": 2, "font": ("Arial", 12), "bd": 0}
        
        tk.Button(btn_frame, text="Registrar Invernadero", bg="#5baa39", fg="white", 
                command=lambda: controller.view.show_frame("RegisterFrame"), **button_style).grid(
                row=0, column=0, padx=10, pady=10)
                
        tk.Button(btn_frame, text="Control de Invernaderos", bg="#5baa39", fg="white",
                command=lambda: controller.view.show_frame("ControlFrame"), **button_style).grid(
                row=1, column=0, padx=10, pady=10)
        
        # Cerrar sesión
        tk.Button(self, text="Cerrar Sesión", command=lambda: controller.view.show_frame("LoginFrame"),
                bg="#f2b01e", fg="white", width=15).pack(side="bottom", pady=30)

class RegisterFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        self.grid(row=0, column=0, sticky="nsew")
        
        self.is_edit_mode = False
        self.edit_index = None
        
        # Título
        self.title_label = tk.Label(self, text="Registrar Invernadero", font=("Arial", 16, "bold"), 
                                  bg="white", fg="#5baa39")
        self.title_label.grid(row=0, column=0, columnspan=2, pady=20)
        
        # Campos del formulario
        labels = [
            "Nombre:", 
            "Superficie (m²):", 
            "Producción (ton):", 
            "Tipo cultivo:", 
            "Fecha creación:", 
            "Responsable:"
        ]
        
        self.entries = {}
        for i, text in enumerate(labels):
            tk.Label(self, text=text, bg="white", anchor="e").grid(row=i+1, column=0, sticky="e", padx=5, pady=5)
            e = tk.Entry(self, width=30)
            e.grid(row=i+1, column=1, padx=5, pady=5, sticky="w")
            key = text.replace(":", "").split(" ")[0]  # Simplificar clave
            self.entries[key] = e
        
        # Botones
        button_frame = tk.Frame(self, bg="white")
        button_frame.grid(row=len(labels)+2, column=0, columnspan=2, pady=20)
        
        self.save_btn = tk.Button(button_frame, text="Guardar", bg="#5baa39", fg="white", 
                               width=10, command=self._on_save)
        self.save_btn.pack(side="left", padx=5)
        
        tk.Button(button_frame, text="Cancelar", bg="#f2b01e", fg="white", 
               width=10, command=self._on_cancel).pack(side="left", padx=5)

    def pre_show(self, edit_mode=False, greenhouse_data=None, index=None):
        """Preparar la vista antes de mostrarla"""
        self.is_edit_mode = edit_mode
        self.edit_index = index
        
        # Limpiar campos
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        
        # Cambiar título según modo
        if edit_mode and greenhouse_data:
            self.title_label.config(text="Editar Invernadero")
            
            # Mapeo de campos
            field_mapping = {
                "Nombre": "nombre",
                "Superficie": "superficie",
                "Producción": "produccion",
                "Tipo": "cultivo",
                "Fecha": "fecha", 
                "Responsable": "responsable"
            }
            
            # Rellenar campos con datos existentes
            for field_name, entry in self.entries.items():
                db_field = field_mapping.get(field_name, field_name.lower())
                if db_field in greenhouse_data:
                    entry.insert(0, greenhouse_data[db_field])
        else:
            self.title_label.config(text="Registrar Invernadero")

    def _on_save(self):
        """Guardar o actualizar el invernadero"""
        # Validar campos
        data = []
        for field, entry in self.entries.items():
            value = entry.get().strip()
            if not value:
                messagebox.showwarning("Atención", f"El campo {field} es obligatorio")
                entry.focus_set()
                return
            data.append(value)
        
        # Guardar o actualizar según el modo
        if self.is_edit_mode and self.edit_index is not None:
            self.controller.update_greenhouse(self.edit_index, data)
            messagebox.showinfo("Éxito", "Invernadero actualizado correctamente")
        else:
            self.controller.add_greenhouse(data)
            messagebox.showinfo("Éxito", "Invernadero registrado correctamente")
        
        # Limpiar campos
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        
        # Volver al listado
        self.controller.view.show_frame("ControlFrame")

    def _on_cancel(self):
        """Cancelar operación y volver"""
        # Limpiar campos
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        
        # Volver a la página anterior
        self.controller.view.show_frame("MenuFrame" if not self.is_edit_mode else "ControlFrame")

class ControlFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        self.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Variables de control
        self.show_active_var = tk.BooleanVar(value=False)
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self._on_search_changed)
        
        # Barra de título
        title_frame = tk.Frame(self, bg="#5baa39", height=40)
        title_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        tk.Label(title_frame, text="Control de Invernaderos", bg="#5baa39", fg="white", 
              font=("Arial", 14, "bold")).pack(side="left", padx=10, pady=5)
        
        # Barra de búsqueda y filtros
        search_frame = tk.Frame(self, bg="white")
        search_frame.grid(row=1, column=0, sticky="new", padx=10, pady=5)
        
        tk.Label(search_frame, text="Buscar:", bg="white").pack(side="left", padx=(0, 5))
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=25)
        search_entry.pack(side="left", padx=5)
        
        active_check = ttk.Checkbutton(search_frame, text="Mostrar solo activos", 
                                     variable=self.show_active_var, 
                                     command=self._refresh)
        active_check.pack(side="right", padx=10)
        
        # Lista de invernaderos
        list_frame = tk.Frame(self, bg="white")
        list_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        
        # Canvas para scrolling
        self.canvas = tk.Canvas(list_frame, bg="white", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Frame dentro del canvas para los items
        self.items_frame = tk.Frame(self.canvas, bg="white")
        self.canvas_window = self.canvas.create_window((0, 0), window=self.items_frame, anchor="nw")
        
        # Configurar resize del canvas
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(
            self.canvas_window, width=e.width))
        self.items_frame.bind("<Configure>", lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")))
        
        # Botones de acción
        button_frame = tk.Frame(self, bg="white")
        button_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=10)
        
        tk.Button(button_frame, text="Nuevo Invernadero", bg="#5baa39", fg="white",
               command=lambda: controller.view.show_frame("RegisterFrame")).pack(side="left", padx=5)
               
        tk.Button(button_frame, text="Refrescar", bg="#f2b01e", fg="white",
               command=self._refresh).pack(side="left", padx=5)
               
        tk.Button(button_frame, text="Volver al Menú", 
               command=lambda: controller.view.show_frame("MenuFrame")).pack(side="right", padx=5)
        
        # Atributo para guardar referencias a los ítems
        self.greenhouse_items = []

    def pre_show(self, **kwargs):
        """Acciones antes de mostrar"""
        self._refresh()

    def _on_search_changed(self, *args):
        """Reaccionar al cambio en el campo de búsqueda"""
        self._refresh()

    def _refresh(self):
        """Actualizar la lista de invernaderos"""
        # Limpiar items anteriores
        for widget in self.items_frame.winfo_children():
            widget.destroy()
        self.greenhouse_items = []
        
        # Obtener datos filtrados
        greenhouses = self.controller.get_greenhouses(
            filter_active=self.show_active_var.get(),
            search_term=self.search_var.get()
        )
        
        # Sin resultados
        if not greenhouses:
            tk.Label(self.items_frame, text="No hay invernaderos para mostrar", 
                  bg="white", fg="gray", font=("Arial", 12)).pack(pady=50)
            return
            
        # Crear items para cada invernadero
        for idx, gh in enumerate(greenhouses):
            item = self._create_greenhouse_item(idx, gh)
            item.pack(fill="x", padx=5, pady=5)
            self.greenhouse_items.append((item, idx))
            
        # Actualizar canvas
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _create_greenhouse_item(self, idx, greenhouse):
        """Crear un widget para mostrar un invernadero"""
        frame = tk.Frame(self.items_frame, bg="white", bd=1, relief="solid")
        
        # Título con nombre y tipo de cultivo
        header = tk.Frame(frame, bg="#5baa39", height=25)
        header.pack(fill="x")
        
        tk.Label(header, text=f"{greenhouse['nombre']} - {greenhouse['cultivo']}", 
              bg="#5baa39", fg="white", anchor="w").pack(side="left", padx=5, pady=2)
        
        # Información principal
        info_frame = tk.Frame(frame, bg="white")
        info_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        tk.Label(info_frame, text=f"Superficie: {greenhouse['superficie']} m²", 
              bg="white", anchor="w").grid(row=0, column=0, sticky="w", padx=5, pady=2)
              
        tk.Label(info_frame, text=f"Producción: {greenhouse['produccion']} ton", 
              bg="white", anchor="w").grid(row=1, column=0, sticky="w", padx=5, pady=2)
              
        tk.Label(info_frame, text=f"Responsable: {greenhouse['responsable']}", 
              bg="white", anchor="w").grid(row=0, column=1, sticky="w", padx=5, pady=2)
              
        tk.Label(info_frame, text=f"Fecha: {greenhouse['fecha']}", 
              bg="white", anchor="w").grid(row=1, column=1, sticky="w", padx=5, pady=2)
        
        # Botones de acción
        button_frame = tk.Frame(frame, bg="white")
        button_frame.pack(fill="x", padx=5, pady=5)
        
        tk.Button(button_frame, text="Ver Detalles", bg="#f2b01e", fg="white",
               command=lambda i=idx: self.controller.view.show_frame("DetailFrame", index=i)).pack(side="right", padx=2)
               
        tk.Button(button_frame, text="Eliminar", bg="#d32f2f", fg="white",
               command=lambda i=idx: self._confirm_delete(i)).pack(side="right", padx=2)
               
        tk.Button(button_frame, text="Editar", bg="#5baa39", fg="white",
               command=lambda i=idx: self._edit_greenhouse(i)).pack(side="right", padx=2)
        
        return frame

    def _confirm_delete(self, index):
        """Confirmar eliminación de invernadero"""
        if messagebox.askyesno("Confirmar", "¿Está seguro que desea eliminar este invernadero?"):
            if self.controller.delete_greenhouse(index):
                messagebox.showinfo("Éxito", "Invernadero eliminado correctamente")
                self._refresh()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el invernadero")

    def _edit_greenhouse(self, index):
        """Editar un invernadero"""
        greenhouse = self.controller.get_greenhouse(index)
        if greenhouse:
            self.controller.view.show_frame("RegisterFrame", 
                                         edit_mode=True, 
                                         greenhouse_data=greenhouse, 
                                         index=index)

class DetailFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        self.grid(row=0, column=0, sticky="nsew")
        self.index = None
        
        # Título
        self.title_label = tk.Label(self, text="Detalles del Invernadero", 
                                  font=("Arial", 16, "bold"), bg="white", fg="#5baa39")
        self.title_label.pack(pady=20)
        
        # Panel de información
        self.info_frame = tk.Frame(self, bg="white", bd=1, relief="solid")
        self.info_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Campos del invernadero
        self.labels = {}
        fields = [
            ("Nombre:", "nombre"), 
            ("Superficie:", "superficie"), 
            ("Producción:", "produccion"),
            ("Tipo de cultivo:", "cultivo"), 
            ("Fecha de creación:", "fecha"), 
            ("Responsable:", "responsable")
        ]
        
        for i, (label_text, field_key) in enumerate(fields):
            row = i // 2
            col = i % 2 * 2
            
            tk.Label(self.info_frame, text=label_text, bg="white", font=("Arial", 10, "bold"),
                  anchor="e").grid(row=row, column=col, sticky="e", padx=5, pady=10)
                  
            value_label = tk.Label(self.info_frame, text="", bg="white", anchor="w")
            value_label.grid(row=row, column=col+1, sticky="w", padx=5, pady=10)
            self.labels[field_key] = value_label
        
        # Botones de acción
        button_frame = tk.Frame(self, bg="white")
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Editar", bg="#5baa39", fg="white", width=10,
               command=self._edit).pack(side="left", padx=5)
               
        tk.Button(button_frame, text="Eliminar", bg="#d32f2f", fg="white", width=10,
               command=self._delete).pack(side="left", padx=5)
               
        tk.Button(button_frame, text="Volver", width=10,
               command=lambda: controller.view.show_frame("ControlFrame")).pack(side="left", padx=5)

    def pre_show(self, index=None):
        """Preparar la vista con los datos del invernadero"""
        if index is not None:
            self.index = index
            gh = self.controller.get_greenhouse(index)
            if gh:
                self.title_label.config(text=f"Invernadero: {gh['nombre']}")
                
                # Actualizar campos
                for field, label in self.labels.items():
                    value = gh.get(field, "")
                    unit = ""
                    if field == "superficie":
                        unit = " m²"
                    elif field == "produccion":
                        unit = " ton"
                    label.config(text=f"{value}{unit}")
            else:
                messagebox.showerror("Error", "No se encontró el invernadero")
                self.controller.view.show_frame("ControlFrame")

    def _delete(self):
        """Eliminar el invernadero actual"""
        if messagebox.askyesno("Confirmar", "¿Está seguro que desea eliminar este invernadero?"):
            if self.controller.delete_greenhouse(self.index):
                messagebox.showinfo("Éxito", "Invernadero eliminado correctamente")
                self.controller.view.show_frame("ControlFrame")
            else:
                messagebox.showerror("Error", "No se pudo eliminar el invernadero")

    def _edit(self):
        """Editar el invernadero actual"""
        gh = self.controller.get_greenhouse(self.index)
        if gh:
            self.controller.view.show_frame("RegisterFrame", 
                                         edit_mode=True, 
                                         greenhouse_data=gh, 
                                         index=self.index)
        else:
            messagebox.showerror("Error", "No se encontró el invernadero")

