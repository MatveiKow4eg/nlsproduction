import os
from datetime import datetime
from flask import Flask, request, jsonify, redirect, url_for, abort, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_babel import Babel
from flask_admin import Admin
from admin import init_admin
from forms import InquiryForm

# Extensions

db = SQLAlchemy()
migrate = Migrate()
babel = Babel()
admin = Admin(name="NLS Admin", template_mode="bootstrap4")


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///nls.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # i18n
    BABEL_DEFAULT_LOCALE = os.getenv("BABEL_DEFAULT_LOCALE", "ru")
    # Comma separated in env -> list here
    _supported = os.getenv("BABEL_SUPPORTED_LOCALES", "ru,et").split(",")
    BABEL_SUPPORTED_LOCALES = [loc.strip() for loc in _supported if loc.strip()]

    # Contact info
    CONTACT_EMAIL = os.getenv("CONTACT_EMAIL", "info@nls.ee")
    CONTACT_PHONE = os.getenv("CONTACT_PHONE", "+372 5555 5555")


# Locale selection
def select_locale():
    # Priority: explicit query param -> best match -> default
    supported = current_app.config.get("BABEL_SUPPORTED_LOCALES", ["ru"])  # type: ignore
    lang = request.args.get("lang")
    if lang and lang in supported:
        return lang
    try:
        return request.accept_languages.best_match(supported) or supported[0]
    except Exception:
        return supported[0]


# Minimal HTML shell used by stub routes
SHELL_HTML = """
<!doctype html>
<html lang=\"ru\" style=\"background:#0E0E0E;color:#fff;font-family:Inter,Montserrat,system-ui,sans-serif;\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>NLS Production</title>
  <style>
    body{margin:0;background:#0E0E0E;color:#fff}
    .nav{display:flex;gap:16px;padding:16px 24px;border-bottom:1px solid #222}
    .nav a{color:#fff;text-decoration:none;opacity:.85}
    .nav a:hover{opacity:1}
    .hero{padding:64px 24px}
    .cta{display:inline-block;margin-right:12px;padding:12px 18px;border-radius:8px;background:#E63946;color:#fff;text-decoration:none}
    .container{max-width:1100px;margin:0 auto}
    footer{margin-top:64px;padding:24px;border-top:1px solid #222;opacity:.8}
    .muted{opacity:.75}
    .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px}
    .card{background:#121212;border:1px solid #1f1f1f;border-radius:12px;padding:16px}
  </style>
</head>
<body>
  <nav class=\"nav\">
    <a href=\"/\">Главная</a>
    <a href=\"/services\">Услуги</a>
    <a href=\"/rental/catalog\">Аренда</a>
    <a href=\"/rental/packages\">Пакеты</a>
    <a href=\"/portfolio\">Портфолио</a>
    <a href=\"/blog\">Блог</a>
    <a href=\"/contact\">Контакты</a>
    <span style=\"margin-left:auto\"></span>
    <a href=\"?lang=ru\">RU</a>
    <a href=\"?lang=et\">ET</a>
  </nav>
  <div class=\"container\">
    {content}
    <footer>
      <div>NLS Production — Ida-Virumaa, работаем по всей Эстонии</div>
      <div class=\"muted\">Email: {email} · Тел: {phone}</div>
      <div class=\"muted\">© {year}</div>
    </footer>
  </div>
</body>
</html>
"""


def page(content: str) -> str:
    return SHELL_HTML.format(
        content=content,
        email=os.getenv("CONTACT_EMAIL", "info@nls.ee"),
        phone=os.getenv("CONTACT_PHONE", "+372 5555 5555"),
        year=datetime.now().year,
    )


def register_routes(app: Flask) -> None:
    @app.get("/")
    def index():
        content = """
        <section class=\"hero\">
          <h1 style=\"font-size:40px;margin:0 0 8px\">Профессиональный звук для вашего события</h1>
          <p class=\"muted\">Ida-Virumaa — наша база, работаем по всей Эстонии. Аренда, монтаж, инженер, запись, поддержка 24/7.</p>
          <div style=\"margin-top:18px\">
            <a class=\"cta\" href=\"/contact\">Рассчитать смету</a>
            <a class=\"cta\" style=\"background:#202020;border:1px solid #2a2a2a\" href=\"/rental/packages\">Готовые пакеты</a>
          </div>
        </section>
        <section>
          <h2>Услуги</h2>
          <div class=\"grid\">
            <div class=\"card\">Свадьбы</div>
            <div class=\"card\">Конференции</div>
            <div class=\"card\">Корпоративы</div>
            <div class=\"card\">Концерты</div>
            <div class=\"card\">Аренда</div>
          </div>
        </section>
        """
        return page(content)

    @app.get("/services")
    def services():
        content = """
        <h1>Услуги</h1>
        <div class=\"grid\">
          <div class=\"card\"><h3>Звуковое сопровождение</h3><p class=\"muted\">Полный стэк звука для мероприятий</p></div>
          <div class=\"card\"><h3>Свадьбы и частные ивенты</h3><p class=\"muted\">Тонкая настройка и аккуратный сетап</p></div>
          <div class=\"card\"><h3>Корпоративы и конференции</h3><p class=\"muted\">Речевые системы, запись, трансляции</p></div>
          <div class=\"card\"><h3>Концерты и фестивали</h3><p class=\"muted\">Лайв-звук, мониторинг, RF-координация</p></div>
          <div class=\"card\"><h3>Инсталляции</h3><p class=\"muted\">Настройка, монтаж, обслуживание</p></div>
        </div>
        """
        return page(content)

    @app.get("/rental/catalog")
    def rental_catalog():
        content = """
        <h1>Каталог аренды</h1>
        <p class=\"muted\">Категории: акустика, микшеры, микрофоны, мониторинг, DJ, аксессуары.</p>
        <div class=\"grid\">
          <div class=\"card\">Акустика</div>
          <div class=\"card\">Микшеры</div>
          <div class=\"card\">Микрофоны</div>
          <div class=\"card\">Мониторинг</div>
          <div class=\"card\">DJ</div>
          <div class=\"card\">Аксессуары</div>
        </div>
        """
        return page(content)

    @app.get("/rental/packages")
    def rental_packages():
        content = """
        <h1>Готовые пакеты</h1>
        <div class=\"grid\">
          <div class=\"card\"><h3>Speech Basic</h3><p class=\"muted\">Речь и фон</p></div>
          <div class=\"card\"><h3>Wedding Medium</h3><p class=\"muted\">Свадебный комплект</p></div>
          <div class=\"card\"><h3>Party DJ</h3><p class=\"muted\">Для вечеринки</p></div>
          <div class=\"card\"><h3>Live Band</h3><p class=\"muted\">Для группы</p></div>
          <div class=\"card\"><h3>Conference Pro</h3><p class=\"muted\">Для конференций</p></div>
        </div>
        """
        return page(content)

    @app.get("/portfolio")
    def portfolio():
        content = """
        <h1>Портфолио</h1>
        <p class=\"muted\">Кейсы: свадьбы, концерты, конференции, корпоративы.</p>
        <div class=\"grid\">
          <div class=\"card\">Свадьба в Нарве</div>
          <div class=\"card\">Концерт в Йыхви</div>
          <div class=\"card\">Конференция в Таллинне</div>
        </div>
        """
        return page(content)

    @app.get("/blog")
    def blog():
        content = """
        <h1>Блог</h1>
        <div class=\"grid\">
          <div class=\"card\"><a href=\"/blog/pervyj-post\">Первый пост</a><div class=\"muted\">2024-01-01</div></div>
          <div class=\"card\"><a href=\"/blog/setup-audio\">Настройка звука</a><div class=\"muted\">2024-02-10</div></div>
        </div>
        """
        return page(content)

    @app.get("/blog/<slug>")
    def blog_post(slug: str):
        content = f"""
        <h1>Статья: {slug}</h1>
        <p class=\"muted\">Контент поста будет позже.</p>
        """
        return page(content)

    @app.route("/contact", methods=["GET", "POST"])
    def contact_get():
        form = InquiryForm()
        if form.validate_on_submit():
            from models import Inquiry
            inquiry = Inquiry(
                event_date=form.event_date.data or None,
                city=form.city.data or None,
                guests=form.guests.data,
                service_type=form.service_type.data or None,
                delivery_required=bool(form.delivery_required.data),
                contact_name=form.contact_name.data,
                contact_email=form.contact_email.data or None,
                contact_phone=form.contact_phone.data or None,
                notes=form.notes.data or None,
            )
            db.session.add(inquiry)
            db.session.commit()
            return redirect(url_for("thanks"))

        # simple inline form until Jinja templates are added
        content = f"""
        <h1>Контакты</h1>
        <form method=\"post\" style=\"display:grid;gap:12px;max-width:520px\">{form_hidden}
          <input name=\"contact_name\" placeholder=\"Имя*\" required style=\"padding:10px;border-radius:8px;border:1px solid #2a2a2a;background:#121212;color:#fff\">
          <input name=\"contact_email\" placeholder=\"Email\" style=\"padding:10px;border-radius:8px;border:1px solid #2a2a2a;background:#121212;color:#fff\">
          <input name=\"contact_phone\" placeholder=\"Телефон\" style=\"padding:10px;border-radius:8px;border:1px solid #2a2a2a;background:#121212;color:#fff\">
          <input name=\"city\" placeholder=\"Город\" style=\"padding:10px;border-radius:8px;border:1px solid #2a2a2a;background:#121212;color:#fff\">
          <input name=\"event_date\" placeholder=\"Дата\" style=\"padding:10px;border-radius:8px;border:1px solid #2a2a2a;background:#121212;color:#fff\">
          <input name=\"guests\" type=\"number\" placeholder=\"Гости\" style=\"padding:10px;border-radius:8px;border:1px solid #2a2a2a;background:#121212;color:#fff\">
          <select name=\"service_type\" style=\"padding:10px;border-radius:8px;border:1px solid #2a2a2a;background:#121212;color:#fff\">
            <option value=\"\">Выберите услугу</option>
            <option value=\"sound_support\">Звуковое сопровождение</option>
            <option value=\"wedding\">Свадьбы и частные мероприятия</option>
            <option value=\"corporate\">Корпоративы и конференции</option>
            <option value=\"concert\">Концерты и фестивали</option>
            <option value=\"installation\">Настройка и инсталляции</option>
            <option value=\"rental\">Аренда оборудования</option>
          </select>
          <label style=\"display:flex;align-items:center;gap:8px\"><input type=\"checkbox\" name=\"delivery_required\"> Требуется доставка/монтаж</label>
          <textarea name=\"notes\" placeholder=\"Комментарий\" rows=\"5\" style=\"padding:10px;border-radius:8px;border:1px solid #2a2a2a;background:#121212;color:#fff\"></textarea>
          <button class=\"cta\" type=\"submit\">Отправить заявку</button>
        </form>
        """
        return page(content.format(form_hidden=form.csrf_token()))

    @app.get("/thanks")
    def thanks():
        content = """
        <h1>Спасибо за заявку!</h1>
        <p class=\"muted\">Мы свяжемся с вами в ближайшее время.</p>
        """
        return page(content)

    @app.get("/api/products")
    def api_products():
        # Placeholder data; will be backed by DB models later
        data = [
            {"id": 1, "name": "Active Speaker 12\"", "category": "acoustics", "day_rate": 25},
            {"id": 2, "name": "Mixer 16ch", "category": "mixers", "day_rate": 40},
        ]
        return jsonify(data)

    @app.get("/api/packages")
    def api_packages():
        data = [
            {"id": 1, "title": "Speech Basic", "base_price": 60},
            {"id": 2, "title": "Wedding Medium", "base_price": 180},
        ]
        return jsonify(data)


def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(Config)

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    babel.init_app(app, locale_selector=select_locale)
    admin.init_app(app)
    init_admin(app, admin)

    # Register routes (will switch to blueprints in later steps)
    register_routes(app)

    # Auto-create SQLite tables in dev to make the app usable immediately
    if app.config.get("SQLALCHEMY_DATABASE_URI", "").startswith("sqlite") and os.getenv("FLASK_ENV") != "production":
        with app.app_context():
            try:
                db.create_all()
            except Exception:
                pass

    return app


if __name__ == "__main__":
    # Run a development server for local testing
    app = create_app()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
