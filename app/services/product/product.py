class Product:
    async def get_all_item(self):
        return True
    async def get_item(self, product_id):
        return {"product_id":product_id}