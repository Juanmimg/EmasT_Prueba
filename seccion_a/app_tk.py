import tkinter as tk
from tkinter import ttk, messagebox

from tickets import (
    Prioridad, Estado, Rol, Usuario, Ticket,
    EmailNotificador, PermisoError, FlujoEstadoError
)

# --- Datos base ---
USUARIO_EMP = Usuario("Juan Pérez", "juan@emast.com", Rol.EMPLEADO)
AGENTE_MARIA = Usuario("María López", "maria@emast.com", Rol.AGENTE)
AGENTE_PEDRO = Usuario("Pedro Ruiz", "pedro@emast.com", Rol.AGENTE)
AGENTES = [AGENTE_MARIA, AGENTE_PEDRO]
ACTORES = {
    "AGENTE: María López": AGENTE_MARIA,
    "AGENTE: Pedro Ruiz":  AGENTE_PEDRO,
    "EMPLEADO: Juan Pérez": USUARIO_EMP,
}

NOTIF = EmailNotificador()
TICKETS = []


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tickets - Minimal Tk")
        self.geometry("1000x600")

        # --- Crear ticket ---
        frm_new = ttk.LabelFrame(self, text="Crear ticket", padding=8)
        frm_new.pack(fill="x", padx=8, pady=6)

        ttk.Label(frm_new, text="Título:").grid(row=0, column=0, sticky="w")
        self.var_titulo = tk.StringVar()
        ttk.Entry(frm_new, textvariable=self.var_titulo, width=40).grid(row=0, column=1, sticky="w")

        ttk.Label(frm_new, text="Prioridad:").grid(row=0, column=2, sticky="w", padx=12)
        self.var_prio = tk.StringVar(value="ALTA")
        ttk.Combobox(frm_new, textvariable=self.var_prio, state="readonly",
                     values=["ALTA","MEDIA","BAJA"], width=10).grid(row=0, column=3, sticky="w")

        ttk.Label(frm_new, text="Descripción:").grid(row=1, column=0, sticky="nw", pady=(4,0))
        self.txt_desc = tk.Text(frm_new, width=60, height=3)
        self.txt_desc.grid(row=1, column=1, columnspan=3, sticky="we", pady=(4,0))
        ttk.Button(frm_new, text="Crear", command=self.crear_ticket).grid(row=0, column=4, rowspan=2, padx=8)

        # --- Lista + acciones ---
        frm_mid = ttk.Frame(self, padding=8)
        frm_mid.pack(fill="both", expand=True)

        # Lista
        left = ttk.Frame(frm_mid)
        left.pack(side="left", fill="both", expand=True)
        ttk.Label(left, text="Tickets").pack(anchor="w")
        self.lb = tk.Listbox(left)
        self.lb.pack(fill="both", expand=True)
        self.lb.bind("<<ListboxSelect>>", self.refrescar_detalle)

        # Acciones
        right = ttk.LabelFrame(frm_mid, text="Acciones", padding=8)
        right.pack(side="left", fill="y", padx=(8,0))

        ttk.Label(right, text="Actor:").grid(row=0, column=0, sticky="w")
        self.var_actor = tk.StringVar(value="AGENTE: María López")
        ttk.Combobox(right, textvariable=self.var_actor, state="readonly",
                     values=list(ACTORES.keys()), width=24).grid(row=0, column=1, sticky="w")

        ttk.Label(right, text="Asignar a:").grid(row=1, column=0, sticky="w", pady=(6,0))
        self.var_agente = tk.StringVar(value="María López")
        ttk.Combobox(right, textvariable=self.var_agente, state="readonly",
                     values=[a.nombre for a in AGENTES], width=24).grid(row=1, column=1, sticky="w")

        ttk.Button(right, text="Asignar", command=self.asignar).grid(row=2, column=0, columnspan=2, sticky="ew", pady=8)
        ttk.Button(right, text="Avanzar estado", command=self.avanzar).grid(row=3, column=0, columnspan=2, sticky="ew")

        ttk.Separator(right).grid(row=4, column=0, columnspan=2, sticky="ew", pady=8)

        ttk.Label(right, text="Detalle:").grid(row=5, column=0, sticky="nw")
        self.lbl_detalle = ttk.Label(right, text="—", justify="left", width=36)
        self.lbl_detalle.grid(row=5, column=1, sticky="w")

        ttk.Label(right, text="Historial:").grid(row=6, column=0, sticky="nw", pady=(6,0))
        self.txt_hist = tk.Text(right, height=8, width=36)
        self.txt_hist.grid(row=6, column=1, sticky="w")

        self.refrescar_listado()

    # --- Utilidades ---
    def _ticket_sel(self):
        sel = self.lb.curselection()
        return TICKETS[sel[0]] if sel else None

    def refrescar_listado(self):
        self.lb.delete(0, tk.END)
        for t in TICKETS:
            ag = t.agente_asignado.nombre if t.agente_asignado else "—"
            self.lb.insert(tk.END, f"#{t.id} [{t.estado.name}] {t.titulo} | Agente: {ag}")

    def refrescar_detalle(self, _evt=None):
        t = self._ticket_sel()
        self.txt_hist.delete("1.0", tk.END)
        if not t:
            self.lbl_detalle.config(text="—")
            return
        self.lbl_detalle.config(text=(
            f"#{t.id}\nTítulo: {t.titulo}\nPrioridad: {t.prioridad.name}\n"
            f"Estado: {t.estado.name}\nCreador: {t.creador.nombre}\n"
            f"Agente: {t.agente_asignado.nombre if t.agente_asignado else '—'}"
        ))
        for h in t.historial:
            self.txt_hist.insert(tk.END, f"• {h}\n")

    # --- Acciones ---
    def crear_ticket(self):
        titulo = self.var_titulo.get().strip()
        desc = self.txt_desc.get("1.0", tk.END).strip()
        if not titulo:
            messagebox.showwarning("Validación", "El título es obligatorio.")
            return
        t = Ticket(
            titulo=titulo,
            descripcion=desc,
            prioridad=Prioridad[self.var_prio.get()],  # sin prio_from()
            creador=USUARIO_EMP,
            notificador=NOTIF,
        )
        TICKETS.append(t)
        self.var_titulo.set("")
        self.txt_desc.delete("1.0", tk.END)
        self.refrescar_listado()

    def asignar(self):
        t = self._ticket_sel()
        if not t:
            messagebox.showinfo("Asignar", "Selecciona un ticket.")
            return
        actor = ACTORES[self.var_actor.get()]
        nombre = self.var_agente.get()
        agente = next(a for a in AGENTES if a.nombre == nombre)  # sin agente_by_name()
        try:
            t.asignar_agente(agente=agente, realizado_por=actor)
            self.refrescar_listado(); self.refrescar_detalle()
        except PermisoError as e:
            messagebox.showerror("Permiso", str(e))

    def avanzar(self):
        t = self._ticket_sel()
        if not t:
            messagebox.showinfo("Estado", "Selecciona un ticket.")
            return
        flujo = {Estado.ABIERTO: Estado.EN_PROGRESO,
                 Estado.EN_PROGRESO: Estado.RESUELTO,
                 Estado.RESUELTO: Estado.CERRADO}
        nuevo = flujo.get(t.estado)
        if not nuevo:
            messagebox.showinfo("Estado", "El ticket ya está CERRADO.")
            return
        actor = ACTORES[self.var_actor.get()]
        try:
            t.cambiar_estado(nuevo_estado=nuevo, realizado_por=actor)
            self.refrescar_listado(); self.refrescar_detalle()
        except (PermisoError, FlujoEstadoError) as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    App().mainloop()
