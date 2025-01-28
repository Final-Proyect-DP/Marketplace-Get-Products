import base64
from flask import jsonify, request
from app.models.models import Product, Category
from app.extensions.extensions import db

def webhook():
    data = request.json
    if not data:
        return jsonify({"message": "No data received"}), 400

    # Validate if the data corresponds to a product or a category
    if 'price' in data:  # It's a product
        product_id = data.get('id')
        name = data.get('name')
        description = data.get('description')
        price = data.get('price')
        userId = data.get('userId')
        image_data = data.get('image_data')
        created_at = data.get('created_at')
        category_id = data.get('category_id')  # New field for category

        if not product_id or not name or not description or not price:
            return jsonify({"message": "Invalid product data"}), 400

        # Convert image from Base64 to binary if it exists
        image_data_binary = base64.b64decode(image_data) if image_data else None

        # Handle category
        if category_id:
            category = Category.query.filter_by(id=category_id).first()
            if not category:
                return jsonify({"message": "Category not found"}), 404

        # Check if the product already exists
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
                category_id=category_id  # Assign the category to the product
            )
            db.session.add(product)
        else:
            # Update existing product
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
