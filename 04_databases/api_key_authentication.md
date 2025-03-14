API key authentication in **FastAPI** can be implemented in multiple ways. Here's a step-by-step guide using **dependency injection** and `Depends` to secure your endpoints.

---

## **Step 1: Define the API Key**
First, set an environment variable or define a constant to store your API key securely.

```python
import os

API_KEY = "mysecureapikey"  # Ideally, store this in environment variables
API_KEY_NAME = "X-API-KEY"   # Custom header for API key
```

---

## **Step 2: Create a Dependency for API Key Authentication**
We create a **dependency function** to check for the API key in the request headers.

```python
from fastapi import FastAPI, Security, HTTPException, Depends
from fastapi.security import APIKeyHeader

app = FastAPI()

# Define security scheme for API key authentication
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def get_api_key(api_key: str = Depends(api_key_header)):
    """Dependency to verify API key"""
    if api_key != API_KEY:
        raise HTTPException(
            status_code=403,
            detail="Invalid API Key",
        )
    return api_key
```

---

## **Step 3: Secure Routes with API Key**
Now, apply the dependency to secure your FastAPI endpoints.

```python
@app.get("/secure-data", dependencies=[Depends(get_api_key)])
async def secure_data():
    return {"message": "This is protected data!"}
```

---

## **Step 4: Testing the API Key Authentication**
You need to include the API key in the request header when calling the protected endpoint.

### **Using `curl`**
```sh
curl -H "X-API-KEY: mysecureapikey" http://127.0.0.1:8000/secure-data
```

### **Using Python Requests**
```python
import requests

url = "http://127.0.0.1:8000/secure-data"
headers = {"X-API-KEY": "mysecureapikey"}

response = requests.get(url, headers=headers)
print(response.json())
```

---

## **Optional: Query Parameter Authentication**
If you want to support API key authentication via **query parameters**, modify the function:

```python
from fastapi.security import APIKeyQuery

api_key_query = APIKeyQuery(name="api_key", auto_error=False)

def get_api_key(api_key_header: str = Depends(api_key_header), api_key_query: str = Depends(api_key_query)):
    """Allow API Key via header or query parameter"""
    if api_key_header == API_KEY or api_key_query == API_KEY:
        return API_KEY
    raise HTTPException(
        status_code=403,
        detail="Invalid API Key",
    )
```

Now, users can authenticate by either:
- **Header:** `X-API-KEY: mysecureapikey`
- **Query Parameter:** `?api_key=mysecureapikey`
