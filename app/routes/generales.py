from ..app import app, db
from flask import render_template
from flask import jsonify
from sqlalchemy import text


@app.route('/test_db')
def test_db():
    try:
        with db.engine.connect() as connection:
            result = connection.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
            tables = [row[0] for row in result]
        return jsonify({"tables": tables})
    except Exception as e:
        return jsonify({"error": str(e)}), 500



