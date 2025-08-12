from __future__ import annotations  #Evita errores con los type hints
from dataclasses import dataclass, field
from enum import Enum, auto #Asigna identificadores automaticos a cada elemento
from typing import Optional, List

from .excepciones import PermisoError, FlujoEstadoError
from .notificaciones import Notificador


# ---------- Enums de dominio ----------

class Prioridad(Enum):
    ALTA = auto()
    MEDIA = auto()
    BAJA = auto()


class Estado(Enum):
    ABIERTO = auto()
    EN_PROGRESO = auto()
    RESUELTO = auto()
    CERRADO = auto()


class Rol(Enum):
    AGENTE = auto()
    EMPLEADO = auto()


# ---------- Usuarios ----------

@dataclass(frozen=True)
class Usuario:
    nombre: str
    email: str
    rol: Rol


# ---------- Ticket ----------

@dataclass
class Ticket:
    titulo: str
    descripcion: str
    prioridad: Prioridad
    creador: Usuario
    notificador: Notificador
    id: int = field(default_factory=lambda: Ticket._next_id(), init=False)
    estado: Estado = field(default=Estado.ABIERTO, init=False)
    agente_asignado: Optional[Usuario] = field(default=None, init=False)
    historial: List[str] = field(default_factory=list, init=False)

    # ---- Autoincremental simple en memoria ----
    _id_seq: int = 0

    @classmethod
    def _next_id(cls) -> int:
        cls._id_seq += 1
        return cls._id_seq

    def _requerir_agente(self, realizado_por: Usuario) -> None:
        if realizado_por.rol != Rol.AGENTE:
            raise PermisoError("Solo un AGENTE puede asignar o cambiar el estado del ticket.")

    @staticmethod
    def _transicion_valida(actual: Estado, nuevo: Estado) -> bool:
        flujo = {
            Estado.ABIERTO: {Estado.EN_PROGRESO},
            Estado.EN_PROGRESO: {Estado.RESUELTO},
            Estado.RESUELTO: {Estado.CERRADO},
            Estado.CERRADO: set(),
        }
        return nuevo in flujo[actual]

    # ---- Operaciones de negocio ----
    def asignar_agente(self, agente: Usuario, realizado_por: Usuario) -> None:
        self._requerir_agente(realizado_por)
        if agente.rol != Rol.AGENTE:
            raise PermisoError("Solo se puede asignar un usuario con rol AGENTE como agente del ticket.")
        self.agente_asignado = agente
        msg = f"Ticket #{self.id} asignado a {agente.nombre}."
        self.historial.append(msg)
        # Notificar a creador y agente
        self.notificador.notify(self.creador, msg)
        self.notificador.notify(agente, f"Se te asignó el ticket #{self.id}: {self.titulo}")

    def cambiar_estado(self, nuevo_estado: Estado, realizado_por: Usuario) -> None:
        self._requerir_agente(realizado_por)
        if not self._transicion_valida(self.estado, nuevo_estado):
            raise FlujoEstadoError(
                f"Transición inválida: {self.estado.name} → {nuevo_estado.name}. "
                f"Flujo permitido: ABIERTO→EN_PROGRESO→RESUELTO→CERRADO."
            )
        anterior = self.estado
        self.estado = nuevo_estado
        msg = f"Ticket #{self.id}: {anterior.name} → {nuevo_estado.name} por {realizado_por.nombre}."
        self.historial.append(msg)
        # Notificar a creador y agente (si lo hay)
        self.notificador.notify(self.creador, msg)
        if self.agente_asignado:
            self.notificador.notify(self.agente_asignado, msg)
