from decimal import Decimal, InvalidOperation

from .models import Item


def check_stock(name):
    """Look up an item's quantity and unit price."""
    item = Item.objects.filter(name__iexact=name).first()
    if item is None:
        return {"error": f"No item named '{name}' exists in the inventory."}
    return {"name": item.name, "quantity": item.quantity, "price": str(item.price)}


def list_items():
    """Return every item in the inventory."""
    items = Item.objects.all()
    return {
        "items": [
            {"name": i.name, "quantity": i.quantity, "price": str(i.price)}
            for i in items
        ]
    }


def add_item(name, quantity):
    """Create a new item, or add to an existing one's stock."""
    item = Item.objects.filter(name__iexact=name).first()
    if item is not None:
        item.quantity += quantity
        item.save()
        return {"name": item.name, "quantity": item.quantity, "created": False}
    item = Item.objects.create(name=name, quantity=quantity)
    return {"name": item.name, "quantity": item.quantity, "created": True}


def update_price(name, price):
    """Update the unit price of an existing item."""
    item = Item.objects.filter(name__iexact=name).first()
    if item is None:
        return {"error": f"No item named '{name}' exists in the inventory."}
    try:
        price = Decimal(str(price))
    except (InvalidOperation, ValueError, TypeError):
        return {"error": "Price must be a valid number."}
    if not price.is_finite() or price < 0:
        return {"error": "Price must be zero or greater."}
    item.price = price
    item.save(update_fields=["price"])
    return {"name": item.name, "price": str(item.price)}


def adjust_price_by_percentage(name, percentage_change):
    """Increase or decrease an item's price by a percentage."""
    item = Item.objects.filter(name__iexact=name).first()
    if item is None:
        return {"error": f"No item named '{name}' exists in the inventory."}

    try:
        percentage_change = Decimal(str(percentage_change))
    except (InvalidOperation, ValueError, TypeError):
        return {"error": "Percentage change must be a valid number."}

    if not percentage_change.is_finite():
        return {"error": "Percentage change must be finite."}
    if percentage_change <= -100:
        return {"error": "Percentage change cannot reduce the price by more than 100%."}

    multiplier = Decimal("1") + (percentage_change / Decimal("100"))
    new_price = item.price * multiplier
    item.price = new_price.quantize(Decimal("0.01"))
    item.save(update_fields=["price"])
    return {"name": item.name, "price": str(item.price)}


def remove_stock(name, quantity):
    """Take a quantity out of stock."""
    item = Item.objects.filter(name__iexact=name).first()
    if item is None:
        return {"error": f"No item named '{name}' exists in the inventory."}
    if quantity > item.quantity:
        return {
            "error": f"Cannot remove {quantity}. Only {item.quantity} in stock.",
            "name": item.name,
            "quantity": item.quantity,
        }
    item.quantity -= quantity
    item.save()
    return {"name": item.name, "quantity": item.quantity}


def delete_item(name):
    """Remove an item from the inventory entirely."""
    item = Item.objects.filter(name__iexact=name).first()
    if item is None:
        return {"error": f"No item named '{name}' exists in the inventory."}
    item.delete()
    return {"deleted": name}


TOOL_DECLARATIONS = [
    {
        "type": "function",
        "name": "check_stock",
        "description": "Look up the current quantity and unit price of a single item in the inventory. Use this whenever the user asks whether something is in stock, how many there are, or what an item costs.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the item, e.g. 'Hammer'.",
                },
            },
            "required": ["name"],
        },
    },
    {
        "type": "function",
        "name": "list_items",
        "description": "Return every item in the inventory with its quantity and unit price. Use this when the user asks what is in stock generally, requests a list, or asks to list prices.",
        "parameters": {"type": "object", "properties": {}},
    },
    {
        "type": "function",
        "name": "add_item",
        "description": "Add stock to the inventory. If the item does not exist it is created; if it already exists the quantity is added to the existing total. Use this for restocking and for new deliveries.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the item, e.g. 'Hammer'.",
                },
                "quantity": {
                    "type": "integer",
                    "description": "How many units to add. Must be positive.",
                },
            },
            "required": ["name", "quantity"],
        },
    },
    {
        "type": "function",
        "name": "remove_stock",
        "description": "Reduce the quantity of an existing item. Use this when items are sold, shipped or used. This does NOT delete the item; it only lowers the number.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the item, e.g. 'Hammer'.",
                },
                "quantity": {
                    "type": "integer",
                    "description": "How many units to remove. Must be positive.",
                },
            },
            "required": ["name", "quantity"],
        },
    },
    {
        "type": "function",
        "name": "update_price",
        "description": "Update the unit price of an existing inventory item to an exact new amount. Use this when the user specifies a final price or asks to set a specific value.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the existing item.",
                },
                "price": {
                    "type": "number",
                    "description": "The new non-negative unit price.",
                },
            },
            "required": ["name", "price"],
        },
    },
    {
        "type": "function",
        "name": "adjust_price_by_percentage",
        "description": "Increase or decrease an item's price by a percentage. Use this when the user says 'increase by 50%' or 'decrease by 10%'. Positive values increase the price, negative values decrease it.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the existing item.",
                },
                "percentage_change": {
                    "type": "number",
                    "description": "Percentage change to apply. Use 50 for a 50% increase or -50 for a 50% decrease.",
                },
            },
            "required": ["name", "percentage_change"],
        },
    },
    {
        "type": "function",
        "name": "delete_item",
        "description": "Permanently remove an item and its record from the inventory entirely. This is destructive. Only use it when the user clearly wants the item gone, not when they want to reduce its quantity.",
        "parameters": {
            "type": "object",
            "properties": {

                "name": {
                    "type": "string",
                    "description": "The name of the item to delete.",
                },
            },
            "required": ["name"],
        },
    },
]

TOOL_FUNCTIONS = {
    "check_stock": check_stock,
    "list_items": list_items,
    "add_item": add_item,
    "update_price": update_price,
    "adjust_price_by_percentage": adjust_price_by_percentage,
    "remove_stock": remove_stock,
    "delete_item": delete_item,
}
