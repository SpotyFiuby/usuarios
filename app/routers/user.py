# from typing import Optional, List
from enum import Enum

from pydantic import BaseModel


class UserStatus(str, Enum):
    No_iniciado = "No Iniciado"
    Iniciado = "Iniciado"
    Terminado = "Terminado"


class UserRequest(BaseModel):
    nombre: str
    descripcion: str
    # lider_de_equipo: Resource
    # personas_asignadas: List[Resource]
    fecha_inicio: str
    fecha_limite_inicio: str
    fecha_estimada_fin: str


class UserWithoutId(UserRequest):
    estado: UserStatus = UserStatus.No_iniciado
    porcentaje_de_avance: float = 0.0
    fecha_fin: str = ""

    class Config:
        use_enum_values = True


class User(UserWithoutId):
    id: int
    # tareas: Optional[List[Task]] = []
