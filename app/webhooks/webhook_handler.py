import base64
from flask import jsonify, request
from app.models.models import Product, Category
from app.extensions.extensions import db

def webhook():
    data = request.json
    if not data:
        return jsonify({"message": "No data received"}), 400

    # Validar si los datos corresponden a un producto o una categoría
    if 'price' in data:  # Es un producto
        product_id = data.get('id')
        name = data.get('name')
        description = data.get('description')
        price = data.get('price')
        userId = data.get('userId')
        image_data = data.get('image_data')
        created_at = data.get('created_at')
        category_id = data.get('category_id')  # Nuevo campo para categoría

        if not product_id or not name or not description or not price:
            return jsonify({"message": "Invalid product data"}), 400

        # Convertir imagen de Base64 a binario si existe
        image_data_binary = base64.b64decode(image_data) if image_data else None

        # Manejo de categoría
        if category_id:
            category = Category.query.filter_by(id=category_id).first()
            if not category:
                return jsonify({"message": "Category not found"}), 404

        # Buscar si el producto ya existe
        product = Product.query.filter_by(id=product_id).first()
        if not product:
            product = Product(
                id=product_id,
                name=name,
                description=description,
                price=price,
                userId=userId,
                image_data=image_data_binary,
                created_at=created_at,
                category_id=category_id  # Asigna la categoría al producto
            )
            db.session.add(product)
        else:
            # Actualizar producto existente
            product.name = name
            product.description = description
            product.price = price
            product.userId = userId
            product.image_data = image_data_binary
            product.created_at = created_at
            product.category_id = category_id

        db.session.commit()
        return jsonify({"message": "Product synchronized successfully"}), 200

    return jsonify({"message": "Invalid data"}), 400
