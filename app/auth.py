from fastapi import Header, HTTPException

API_KEYS = {
    "auth-service-key",
    "payment-service-key"
}


def verify_api_key(x_api_key: str = Header(...)):

    if x_api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")

    return x_api_key