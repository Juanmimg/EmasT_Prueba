from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, TYPE_CHECKING

# Evitamos import circular: solo para type hints en tiempo de tipo
if TYPE_CHECKING:
    from .modelos import Usuario


class Notificador(ABC):
    @abstractmethod
    def notify(self, usuario: "Usuario", mensaje: str) -> None:
        """Envía una notificación al usuario."""
        ...


@dataclass
class EmailNotificador(Notificador):
    """
    Guarda las notificaciones enviadas en una lista (enviados).
    Se utiliza para el historial en la interfaz
    """
    enviados: List[str] = field(default_factory=list)

    def notify(self, usuario: "Usuario", mensaje: str) -> None:
        registro = f"[EMAIL a {usuario.email}] {mensaje}"
        self.enviados.append(registro)
        print(registro)  # Quita el print en producción si no lo quieres
