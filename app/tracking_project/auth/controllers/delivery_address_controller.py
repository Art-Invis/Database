from flask import Blueprint, request, jsonify
from app import app
from auth.service.delivery_address_service import DeliveryAddressService


delivery_address_blueprint = Blueprint('delivery_addresses', __name__)


@delivery_address_blueprint.route('/addresses', methods=['POST'])
def add_delivery_address():
    try:
        data = request.get_json()
        address = data.get('address')
        delivery_instructions = data.get('delivery_instructions')

        if not address or not delivery_instructions:
            return jsonify({"error": "Missing required fields"}), 400

        # Виклик сервісу для додавання нової адреси
        DeliveryAddressService.create_address(address, delivery_instructions)

        return jsonify({"message": "Delivery address added successfully"}), 201
    except Exception as e:
        # Перехоплюємо текст повідомлення помилки
        error_message = str(e)
        # Повертаємо лише повідомлення SQL SIGNAL
        if 'SQLSTATE' in error_message:
            error_message = error_message.split("'")[3]  # Отримання тексту повідомлення після SQLSTATE
        return jsonify({"error": error_message}), 400



@delivery_address_blueprint.route('/addresses', methods=['GET'])
def get_addresses():
    try:
        addresses = DeliveryAddressService.get_all_addresses()
        result = [{
            "address_id": addr.address_id,
            "address": addr.address,
            "delivery_instructions": addr.delivery_instructions
        } for addr in addresses]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@delivery_address_blueprint.route('/addresses/<int:address_id>', methods=['GET'])
def get_address_by_id(address_id):
    try:
        address = DeliveryAddressService.get_address_by_id(address_id)
        if address:
            result = {
                "address_id": address.address_id,
                "address": address.address,
                "delivery_instructions": address.delivery_instructions
            }
            return jsonify(result), 200
        else:
            return jsonify({"error": "Address not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@delivery_address_blueprint.route('/addresses/<int:address_id>', methods=['PUT'])
def update_address(address_id):
    try:
        data = request.get_json()
 
        if not data.get('address'):
            return jsonify({"error": "Address is required"}), 400
        
        updated_address = DeliveryAddressService.update_address(
            address_id, data['address'], data.get('delivery_instructions')
        )
        if updated_address:
            return jsonify({
                "message": "Address updated successfully",
                "address_id": updated_address.address_id,
                "address": updated_address.address,
                "delivery_instructions": updated_address.delivery_instructions
            }), 200
        else:
            return jsonify({"error": "Address not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@delivery_address_blueprint.route('/addresses/<int:address_id>', methods=['DELETE'])
def delete_address(address_id):
    try:
        success = DeliveryAddressService.delete_address(address_id)
        if success:
            return jsonify({"message": "Address deleted successfully"}), 200
        else:
            return jsonify({"error": "Address not found"}), 404
    except Exception as e:
        return jsonify({"error": f"Error deleting address: {str(e)}"}), 500


app.register_blueprint(delivery_address_blueprint)