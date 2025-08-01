from fastapi import HTTPException, Request
from clerk_backend_api import Clerk, AuthenticateRequestOptions
from src.config import CLERK_SECRET_KEY, JWT_KEY

clerk_sdk = Clerk(bearer_auth=CLERK_SECRET_KEY)

def authenticate_and_get_user_details(request: Request):
  try:
    request_state = clerk_sdk.authenticate_request(
      request,
      AuthenticateRequestOptions(
        authorized_parties=["*"],
        jwt_key=JWT_KEY
      )
    )
    if not request_state.is_signe_in:
      raise HTTPException(status_code=401, detail="Invalid Token")
    
    user_id = request_state.payload.get("sub") # Clerk ID
    full_name = request_state.payload.get("fullname")
    email = request_state.payload.get("email")

    return {
      "clerk_id": user_id,
      "fullname": full_name,
      "email": email
    }
  
  except Exception as e:
    raise HTTPException(status_code=500, detail="Authorization failed")
