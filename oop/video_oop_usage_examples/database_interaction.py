class Model:
    _db = {"clients": [], "products": [], "orders": []}
    id: int

    def save(self):
        """ Сохранение или обновление объекта в базе данных """
        table = self.__class__.__name__.lower() + 's'
        if self.id is None:
            self.id = len(self._db[table]) + 1
            self._db[table].append(self)
        else:
            for i, item in enumerate(self._db[table]):
                if item.id == self.id:
                    self._db[table][i] = self
                    break

    @classmethod
    def all(cls):
        """ Получение всех записей из таблицы """
        table = cls.__name__.lower() + 's'
        return cls._db[table]

    @classmethod
    def find(cls, **query):
        """ Поиск записей по заданным критериям """
        table = cls.__name__.lower() + 's'
        results = cls._db[table]
        for key, value in query.items():
            results = [item for item in results if getattr(item, key) == value]
        return results

    def __repr__(self):
        return self.__str__()


class Client(Model):
    def __init__(self, name, email, id=None):
        self.id = id
        self.name = name
        self.email = email

    def __str__(self):
        return f"Client(ID: {self.id}, Name: {self.name}, Email: {self.email})"


class Product(Model):
    def __init__(self, name, price, id=None):
        self.id = id
        self.name = name
        self.price = price

    def __str__(self):
        return f"Product(ID: {self.id}, Name: {self.name}, Price: ${self.price})"


class Order(Model):
    def __init__(self, client_id, product_id, quantity, id=None):
        self.id = id
        self.client_id = client_id
        self.product_id = product_id
        self.quantity = quantity

    def __str__(self):
        return f"Order(ID: {self.id}, Client_ID: {self.client_id}, Product_ID: {self.product_id}, Quantity: {self.quantity})"


# Пример использования
if __name__ == "__main__":
    client1 = Client("John Doe", "john@example.com")
    client1.save()

    product1 = Product("Laptop", 1200)
    product1.save()

    order1 = Order(client1.id, product1.id, 1)
    order1.save()

    print(Client.all())
    print(Product.all())
    print(Order.all())
