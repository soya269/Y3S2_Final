products = [
    {
        "id": 5,
        "title": "Classic Black Hooded Sweatshirt",
        "slug": "classic-black-hooded-sweatshirt",
        "price": 79,
        "description": "Elevate your casual wardrobe with our Classic Black Hooded Sweatshirt.",
        "category": {
            "id": 1,
            "name": "Fashion"
        },
        "images": [
            "https://i.imgur.com/cSytoSD.jpeg"
        ]
    },
    {
        "id": 6,
        "title": "Classic Comfort Fit Joggers",
        "slug": "classic-comfort-fit-joggers",
        "price": 25,
        "description": "Comfortable black joggers perfect for daily wear.",
        "category": {
            "id": 1,
            "name": "Fashion"
        },
        "images": [
            "https://i.imgur.com/ZKGofuB.jpeg"
        ]
    },
    {
        "id": 9,
        "title": "Classic Navy Blue Baseball Cap",
        "slug": "classic-navy-blue-baseball-cap",
        "price": 61,
        "description": "Stylish navy blue baseball cap.",
        "category": {
            "id": 1,
            "name": "Fashion"
        },
        "images": [
            "https://i.imgur.com/R3iobJA.jpeg"
        ]
    },
    {
        "id": 15,
        "title": "Classic White Crew Neck T-Shirt",
        "slug": "classic-white-crew-neck-t-shirt",
        "price": 39,
        "description": "Soft and stylish white t-shirt.",
        "category": {
            "id": 1,
            "name": "Fashion"
        },
        "images": [
            "https://i.imgur.com/axsyGpD.jpeg"
        ]
    },
    {
        "id": 18,
        "title": "Wireless Gaming Controller",
        "slug": "wireless-gaming-controller",
        "price": 69,
        "description": "Modern wireless gaming controller.",
        "category": {
            "id": 2,
            "name": "Electronics"
        },
        "images": [
            "https://i.imgur.com/ZANVnHE.jpeg"
        ]
    },
    {
        "id": 20,
        "title": "Comfort-Fit Headphones",
        "slug": "comfort-fit-headphones",
        "price": 28,
        "description": "High quality over-ear headphones.",
        "category": {
            "id": 2,
            "name": "Electronics"
        },
        "images": [
            "https://i.imgur.com/SolkFEB.jpeg"
        ]
    },
    {
        "id": 22,
        "title": "Wireless Computer Mouse",
        "slug": "wireless-computer-mouse",
        "price": 10,
        "description": "Smooth and precise wireless mouse.",
        "category": {
            "id": 2,
            "name": "Electronics"
        },
        "images": [
            "https://i.imgur.com/w3Y8NwQ.jpeg"
        ]
    },
    {
        "id": 23,
        "title": "Modern Laptop",
        "slug": "modern-laptop",
        "price": 43,
        "description": "Slim and powerful laptop.",
        "category": {
            "id": 2,
            "name": "Electronics"
        },
        "images": [
            "https://i.imgur.com/OKn1KFI.jpeg"
        ]
    },
    {
        "id": 28,
        "title": "Modern Leather Sofa",
        "slug": "modern-leather-sofa",
        "price": 53,
        "description": "Luxury leather sofa for modern homes.",
        "category": {
            "id": 3,
            "name": "Furniture"
        },
        "images": [
            "https://i.imgur.com/Qphac99.jpeg"
        ]
    },
    {
        "id": 34,
        "title": "Ergonomic Office Chair",
        "slug": "ergonomic-office-chair",
        "price": 71,
        "description": "Comfortable office chair for productivity.",
        "category": {
            "id": 3,
            "name": "Furniture"
        },
        "images": [
            "https://i.imgur.com/3dU0m72.jpeg"
        ]
    },
    {
        "id": 35,
        "title": "Holographic Soccer Cleats",
        "slug": "holographic-soccer-cleats",
        "price": 39,
        "description": "Stylish futuristic soccer shoes.",
        "category": {
            "id": 4,
            "name": "Shoes"
        },
        "images": [
            "https://i.imgur.com/qNOjJje.jpeg"
        ]
    },
    {
        "id": 39,
        "title": "Pink Classic Sneakers",
        "slug": "pink-classic-sneakers",
        "price": 84,
        "description": "Bold and colorful pink sneakers.",
        "category": {
            "id": 4,
            "name": "Shoes"
        },
        "images": [
            "https://i.imgur.com/mcW42Gi.jpeg"
        ]
    },
    {
        "id": 45,
        "title": "Electric Bicycle",
        "slug": "electric-bicycle",
        "price": 22,
        "description": "Eco-friendly electric bicycle.",
        "category": {
            "id": 5,
            "name": "Miscellaneous"
        },
        "images": [
            "https://i.imgur.com/BG8J0Fj.jpg"
        ]
    },
    {
        "id": 47,
        "title": "Radiant Citrus Perfume",
        "slug": "radiant-citrus-perfume",
        "price": 73,
        "description": "Fresh citrus scented perfume.",
        "category": {
            "id": 5,
            "name": "Miscellaneous"
        },
        "images": [
            "https://i.imgur.com/xPDwUb3.jpg"
        ]
    },
    {
        "id": 50,
        "title": "Pink-Tinted Sunglasses",
        "slug": "pink-tinted-sunglasses",
        "price": 38,
        "description": "Fashionable pink sunglasses.",
        "category": {
            "id": 5,
            "name": "Miscellaneous"
        },
        "images": [
            "https://i.imgur.com/0qQBkxX.jpg"
        ]
    }
]
def get_product_by_title(title):
    return next(
        (
            p for p in products
            if p["title"].lower() == title.lower()
        ),
    None
    )
def get_product_by_id(product_id):
    return next(
        (p for p in products if p["id"] == product_id),
        None
    )
def get_related_products(
    category_name,
    current_product_id
):
    related_products = []
    for product in products:
        if (
            product["category"]["name"].lower()
            == category_name.lower()
            and product["id"] != current_product_id
        ):
            related_products.append(product)
    return related_products