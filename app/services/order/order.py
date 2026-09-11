class Order:
    async def get_all_item(self):
        return True
    async def get_item(self, order_id):
        return {"order_id":order_id}
    async def add_item(self):
        return False
    async def remove_item(self, order_id):
        return {"order_id":order_id}
    async def calculate_total(self, order_id):
        return {"order_id":order_id}
    async def pay(self, order_id):
        return {"order_id":order_id}
    async def cancel(self, order_id):
        return {"order_id":order_id}
    async def complete(self, order_id):
        return {"order_id":order_id}
