import os
import sys
import shutil

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from authentication.fusion import IdentityAuthenticator

app = FastAPI(title="IdentityShield Authentication API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

authenticator = IdentityAuthenticator()

TEMP_DIR = r"D:\7th Semester\Information Security\aadhaar-inspired-security\data\temp"
os.makedirs(TEMP_DIR, exist_ok=True)

@app.post("/verify/credential")
async def verify_credential(synthetic_id: str = Form(...)):
    try:
        res = authenticator.cred_validator.verify_credential(synthetic_id)
        return JSONResponse(content=res)
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "ERROR", "message": str(e)})

@app.post("/authenticate")
async def authenticate(
    synthetic_id: str = Form(...),
    attack_type: str = Form("Unknown"),
    face_image: UploadFile = File(...),
    fingerprint_image: UploadFile = File(...)
):
    try:
        # Save uploaded files temporarily
        face_path = os.path.join(TEMP_DIR, f"temp_face_{face_image.filename}")
        fp_path = os.path.join(TEMP_DIR, f"temp_fp_{fingerprint_image.filename}")
        
        with open(face_path, "wb") as buffer:
            shutil.copyfileobj(face_image.file, buffer)
            
        with open(fp_path, "wb") as buffer:
            shutil.copyfileobj(fingerprint_image.file, buffer)
            
        # Run the full multimodal fusion logic
        result = authenticator.authenticate(
            synthetic_id=synthetic_id,
            probe_face_path=face_path,
            probe_fp_path=fp_path,
            attack_type=attack_type
        )
        
        # Clean up temp files
        try:
            os.remove(face_path)
            os.remove(fp_path)
        except Exception as e:
            print(f"Cleanup error: {e}")
            
        return JSONResponse(content=result)
        
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "ERROR", "message": str(e)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
