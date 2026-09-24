from run import app
from app.models.produto import db, Produto


produtos = [
    Produto(
        nome="iPhone 15",
        descricao="Smartphone Apple iPhone 15 128GB",
        categoria="Smartphone",
        preco=4999.00,
        quantidade=7
    ),
    Produto(
        nome="Samsung Galaxy S24",
        descricao="Smartphone Samsung Galaxy S24 128GB",
        categoria="Smartphone",
        preco=3899.00,
        quantidade=5
    ),
    Produto(
        nome="Motorola Edge 50",
        descricao="Smartphone Motorola Edge 50",
        categoria="Smartphone",
        preco=2499.00,
        quantidade=4
    ),
    Produto(
        nome="Mouse Logitech MX Master 3S",
        descricao="Mouse sem fio Logitech",
        categoria="Acessórios",
        preco=599.00,
        quantidade=8
    ),
    Produto(
        nome="Teclado Logitech MX Keys",
        descricao="Teclado sem fio Logitech",
        categoria="Acessórios",
        preco=649.00,
        quantidade=3
    ),
    Produto(
        nome="Headset HyperX Cloud III",
        descricao="Headset gamer HyperX",
        categoria="Acessórios",
        preco=499.00,
        quantidade=0
    ),
    Produto(
        nome="Notebook Lenovo IdeaPad",
        descricao="Notebook Lenovo IdeaPad 15 polegadas",
        categoria="Notebook",
        preco=3299.00,
        quantidade=2
    ),
]


with app.app_context():

    if Produto.query.count() == 0:
        db.session.add_all(produtos)
        db.session.commit()

        print("Produtos cadastrados com sucesso!")

    else:
        print("O banco de dados já possui produtos.")