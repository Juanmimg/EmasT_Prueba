class PermisoError(Exception):
    """Se lanza cuando un usuario sin permisos intenta realizar una acción restringida."""
    pass


class FlujoEstadoError(Exception):
    """Se lanza cuando se intenta una transición de estado inválida."""
    pass
