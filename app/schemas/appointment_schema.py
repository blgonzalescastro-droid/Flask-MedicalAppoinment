from pydantic import BaseModel, field_validator
from datetime import date, time, datetime

class AppointmentCreateSchema(BaseModel):
    doctor_id: int
    date: date
    time: time 

    # Validación adicional: No permitir citas en días pasados
    @field_validator('date')
    @classmethod
    def validate_future_date(cls, v: date) -> date:
        if v < date.today():
            raise ValueError('La fecha de la cita no puede ser en el pasado.')
        return v

    # Validación adicional: Si la cita es hoy, que la hora no haya pasado ya
    @field_validator('time')
    @classmethod
    def validate_future_time(cls, v: time, info) -> time:
        # Buscamos el valor de la fecha ya validado en el mismo request
        values = info.data
        if 'date' in values and values['date'] == date.today():
            now_time = datetime.now().time()
            if v < now_time:
                raise ValueError('La hora seleccionada ya ha pasado el día de hoy.')
        return v