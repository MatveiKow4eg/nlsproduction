from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Optional, Length, NumberRange


SERVICE_CHOICES = [
    ("sound_support", "Звуковое сопровождение"),
    ("wedding", "Свадьбы и частные мероприятия"),
    ("corporate", "Корпоративы и конференции"),
    ("concert", "Концерты и фестивали"),
    ("installation", "Настройка и инсталляции"),
    ("rental", "Аренда оборудования"),
]


class InquiryForm(FlaskForm):
    contact_name = StringField("Имя", validators=[DataRequired(), Length(max=120)])
    contact_email = StringField("Email", validators=[Optional(), Email(), Length(max=255)])
    contact_phone = StringField("Телефон", validators=[Optional(), Length(max=64)])

    city = StringField("Город", validators=[Optional(), Length(max=120)])
    event_date = StringField("Дата", validators=[Optional(), Length(max=32)])
    guests = IntegerField("Гости", validators=[Optional(), NumberRange(min=1, max=50000)])

    service_type = SelectField("Тип услуги", choices=SERVICE_CHOICES, validators=[Optional()])
    delivery_required = BooleanField("Требуется доставка/монтаж")

    notes = TextAreaField("Комментарий", validators=[Optional(), Length(max=5000)])

    submit = SubmitField("Отправить заявку")
