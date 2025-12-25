
from werkzeug.utils import secure_filename
from uuid import uuid4
import os
from flask import Blueprint, request, jsonify, current_app, url_for


from models import (
    get_products, get_product, add_product,
    update_product, delete_product
)

api = Blueprint("api", __name__)

@api.get("/products")
def api_get_products():
    return jsonify(get_products()), 200

@api.get("/products/<int:pid>")
def api_get_product(pid):
    product = get_product(pid)
    if product:
        return jsonify(product), 200
    return jsonify({"message": "Not found"}), 404

@api.post("/products")
def api_add_product():
    data = request.json or {}

    pid = add_product(
        data.get("name"),
        data.get("price"),
        data.get("description"),
        data.get("imgPath"),
    )

    return jsonify({"message": "created", "id": pid}), 201

@api.put("/products/<int:pid>")
def api_update_product_route(pid):
    data = request.json or {}

    ok = update_product(
        pid,
        name=data.get("name"),
        price=data.get("price"),
        description=data.get("description"),
        imgPath=data.get("imgPath"),
    )

    if not ok:
        return jsonify({"message": "Not found"}), 404

    return jsonify({"message": "updated"}), 200

@api.delete("/products/<int:pid>")
def api_delete_product(pid):
    delete_product(pid)
    return jsonify({"message": "deleted"}), 200


@api.post("/upload_image")
def upload_image():
    print("Content-Type:", request.content_type)
    print("request.files keys:", list(request.files.keys()))

    file = request.files.get("image")
    if file is None or file.filename == "":
        return jsonify({"message": "no file uploaded"}), 400

    filename = secure_filename(f"{uuid4().hex}_{file.filename}")

    upload_folder = current_app.config["UPLOAD_FOLDER"]
    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)

    file_url = url_for("uploaded_file", filename=filename, _external=True)

    return jsonify({"url": file_url}), 201
