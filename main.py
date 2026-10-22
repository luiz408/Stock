import json
from dataclasses import dataclass, asdict
from pathlib import Path

DATA_FILE = Path(__file__).with_name("inventory.json")


@dataclass
class Product:
    id: int
    name: str
    price: float
    quantity: int


def load_products():
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            content = file.read()
        if not content.strip():
            return []
        data = json.loads(content)
        return [Product(**item) for item in data]
    except (json.JSONDecodeError, TypeError, KeyError):
        raise RuntimeError(
            "Arquivo de estoque inválido. "
            "Verifique o inventory.json."
        )


def save_products(products):
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            [asdict(product) for product in products],
            file,
            indent=4,
            ensure_ascii=False
        )


def find_product(products, product_id):
    return next(
        (p for p in products if p.id == product_id),
        None
    )


def read_integer(message, minimum=0):
    while True:
        try:
            value = int(input(message))
            if value < minimum:
                print(f"Digite um número maior ou igual a {minimum}.")
                continue
            return value
        except ValueError:
            print("Digite um número inteiro válido.")


def read_price(message):
    while True:
        try:
            value = float(input(message).replace(",", "."))
            if value < 0:
                print("O preço não pode ser negativo.")
                continue
            return value
        except ValueError:
            print("Digite um preço válido.")


def add_product(products):
    name = input("Nome do produto: ").strip()

    if not name:
        print("O nome não pode ficar vazio.")
        return

    price = read_price("Preço: R$ ")
    quantity = read_integer("Quantidade inicial: ")

    next_id = max((p.id for p in products), default=0) + 1

    products.append(Product(next_id, name, price, quantity))
    save_products(products)

    print(f"Produto '{name}' cadastrado com ID {next_id}.")


def list_products(products):
    if not products:
        print("Nenhum produto cadastrado.")
        return

    print("\n--- ESTOQUE ---")

    for p in products:
        print(
            f"ID: {p.id} | {p.name} | "
            f"Preço: R$ {p.price:.2f} | "
            f"Quantidade: {p.quantity}"
        )


def search_product(products):
    product_id = read_integer("ID do produto: ", minimum=1)
    product = find_product(products, product_id)

    if product:
        print(
            f"ID: {product.id} | Nome: {product.name} | "
            f"Preço: R$ {product.price:.2f} | "
            f"Estoque: {product.quantity}"
        )
    else:
        print("Produto não encontrado.")


def stock_entry(products):
    product_id = read_integer("ID do produto: ", minimum=1)
    product = find_product(products, product_id)

    if not product:
        print("Produto não encontrado.")
        return

    quantity = read_integer("Quantidade de entrada: ", minimum=1)
    product.quantity += quantity
    save_products(products)

    print("Entrada registrada com sucesso.")


def stock_exit(products):
    product_id = read_integer("ID do produto: ", minimum=1)
    product = find_product(products, product_id)

    if not product:
        print("Produto não encontrado.")
        return

    quantity = read_integer("Quantidade de saída: ", minimum=1)

    if quantity > product.quantity:
        print("Estoque insuficiente.")
        return

    product.quantity -= quantity
    save_products(products)

    print("Saída registrada com sucesso.")


def delete_product(products):
    product_id = read_integer("ID do produto: ", minimum=1)
    product = find_product(products, product_id)

    if not product:
        print("Produto não encontrado.")
        return

    confirmation = input(
        f"Excluir '{product.name}'? (s/n): "
    ).strip().lower()

    if confirmation == "s":
        products.remove(product)
        save_products(products)
        print("Produto excluído.")
    else:
        print("Operação cancelada.")


def show_inventory_value(products):
    total = sum(p.price * p.quantity for p in products)
    print(f"Valor total estimado do estoque: R$ {total:.2f}")


def main():
    try:
        products = load_products()
    except RuntimeError as error:
        print(error)
        return

    while True:
        print("""
========= STOCKPY =========
1. Cadastrar produto
2. Listar produtos
3. Buscar produto por ID
4. Registrar entrada
5. Registrar saída
6. Excluir produto
7. Valor total do estoque
0. Sair
===========================
""")

        option = input("Escolha uma opção: ").strip()

        try:
            if option == "1":
                add_product(products)
            elif option == "2":
                list_products(products)
            elif option == "3":
                search_product(products)
            elif option == "4":
                stock_entry(products)
            elif option == "5":
                stock_exit(products)
            elif option == "6":
                delete_product(products)
            elif option == "7":
                show_inventory_value(products)
            elif option == "0":
                print("Até logo!")
                break
            else:
                print("Opção inválida.")

        except (OSError, ValueError) as error:
            print(f"Não foi possível concluir a operação: {error}")


if __name__ == "__main__":
    main()