class AuthService:

    def register_user(self, user):
        return {
            "message": "User registered successfully.",
            "user": {
                "full_name": user.full_name,
                "email": user.email
            }
        }
    
    def get_user(self, user_id):
        return {
            "message": "User found",
            "user_id": user_id
        }
    
    def search_users(self, name: str = "Guest"):
        return {
            "search": name
        }
    
    def get_product(self, product_id: int, currency: str = "NGN"):
        return {
            "product_id": product_id,
            "currency": currency
        }

def get_auth_service():
    return AuthService()