from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from flask import Flask


def init_admin(app: Flask, admin: Admin) -> None:
    from app import db
    from models import Product, Package, PackageItem, Inquiry, Case, Post
    admin.add_view(ModelView(Product, db.session, category="Catalog"))
    admin.add_view(ModelView(Package, db.session, category="Catalog"))
    admin.add_view(ModelView(PackageItem, db.session, category="Catalog"))
    admin.add_view(ModelView(Inquiry, db.session, category="CRM"))
    admin.add_view(ModelView(Case, db.session, category="Content"))
    admin.add_view(ModelView(Post, db.session, category="Content"))
