from flask import Blueprint, render_template

mod = Blueprint("admin", __name__)

@mod.route('/')
def admin_index():
    return render_template('admin/index.html')
