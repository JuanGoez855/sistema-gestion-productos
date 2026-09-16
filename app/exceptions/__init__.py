class ProductNotFoundError(Exception):
    def __init__(self, product_id: int):
        self.product_id = product_id
        self.message = f"El producto con ID {product_id} no existe"
        super().__init__(self.message)