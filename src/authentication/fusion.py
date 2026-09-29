import os
import sqlite3
import pandas as pd
from datetime import datetime

from authentication.credential import CredentialValidator
from authentication.face import FaceVerifier
from authentication.face_pad import FacePAD
from authentication.fingerprint import FingerprintVerifier
from authentication.fingerprint_pad import FingerprintPAD

BASE_DIR = r"D:\7th Semester\Information Security\aadhaar-inspired-security"
METADATA_PATH = os.path.join(BASE_DIR, "data", "metadata", "identities.csv")
DB_PATH = os.path.join(BASE_DIR, "database", "identity_system.db")

class IdentityAuthenticator:
    def __init__(self):
        self.cred_validator = CredentialValidator()
        self.face_pad = FacePAD()
        self.face_verifier = FaceVerifier()
        self.fp_pad = FingerprintPAD()
        self.fp_verifier = FingerprintVerifier()
        
        # Load identity reference mapping for simulation
        self.identity_map = pd.read_csv(METADATA_PATH).set_index("identity_id")
        # Load full dataset for demo digital card
        self.full_dataset = pd.read_csv(os.path.join(BASE_DIR, "demo_dataset", "aadhaar_dataset.csv"))
        self.full_dataset['aadhaar_number'] = self.full_dataset['aadhaar_number'].astype(str)

    def _log_attempt(self, log_data):
        """Logs the authentication attempt to the database for analysis."""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO verification_logs 
                (identity_id, credential_result, face_pad_result, face_match_score, 
                 fingerprint_pad_result, fingerprint_match_score, final_result, attack_type)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                log_data.get("identity_id"),
                log_data.get("credential_result"),
                log_data.get("face_pad_result"),
                log_data.get("face_match_score"),
                log_data.get("fingerprint_pad_result"),
                log_data.get("fingerprint_match_score"),
                log_data.get("final_result"),
                log_data.get("attack_type")
            ))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Failed to log attempt: {e}")

    def authenticate(self, synthetic_id: str, probe_face_path: str, probe_fp_path: str, attack_type="Unknown") -> dict:
        """
        The main Fusion Gateway. Executes the hard-security gates sequentially.
        If any gate fails, authentication is immediately blocked.
        """
        log_data = {
            "identity_id": None,
            "credential_result": None,
            "face_pad_result": None,
            "face_match_score": None,
            "fingerprint_pad_result": None,
            "fingerprint_match_score": None,
            "final_result": "BLOCK",
            "attack_type": attack_type
        }
        
        # GATE 1: Credential Validation
        cred_res = self.cred_validator.verify_credential(synthetic_id)
        log_data["credential_result"] = cred_res["status"]
        
        if cred_res["status"] != "VALID":
            self._log_attempt(log_data)
            return {"status": "BLOCK", "reason": "Invalid Credential.", **log_data}
            
        identity_id = cred_res["identity_id"]
        log_data["identity_id"] = identity_id
        
        # Retrieve Enrolled References
        enrolled_face = self.identity_map.loc[identity_id, 'face_path']
        enrolled_fp = self.identity_map.loc[identity_id, 'fingerprint_path']

        # GATE 2: Face Presentation Attack Detection (Liveness)
        fpad_res = self.face_pad.detect_liveness(probe_face_path)
        log_data["face_pad_result"] = fpad_res["status"]
        
        if fpad_res["status"] != "LIVE":
            self._log_attempt(log_data)
            return {"status": "BLOCK", "reason": "Face Presentation Attack Detected (SPOOF).", **log_data}
            
        # GATE 3: Face Verification (1:1 Match)
        fmatch_res = self.face_verifier.verify_face(enrolled_face, probe_face_path)
        log_data["face_match_score"] = fmatch_res.get("distance")
        
        if fmatch_res["status"] != "MATCH":
            self._log_attempt(log_data)
            return {"status": "BLOCK", "reason": "Face verification failed (NON-MATCH).", **log_data}
            
        # GATE 4: Fingerprint Presentation Attack Detection
        fppad_res = self.fp_pad.detect_liveness(probe_fp_path)
        log_data["fingerprint_pad_result"] = fppad_res["status"]
        
        if fppad_res["status"] != "GENUINE":
            self._log_attempt(log_data)
            return {"status": "BLOCK", "reason": "Fingerprint Presentation Attack Detected (SPOOF).", **log_data}
            
        # GATE 5: Fingerprint Verification (1:1 Match)
        fpmatch_res = self.fp_verifier.verify_fingerprint(enrolled_fp, probe_fp_path)
        log_data["fingerprint_match_score"] = fpmatch_res.get("score")
        
        if fpmatch_res["status"] != "MATCH":
            self._log_attempt(log_data)
            return {"status": "BLOCK", "reason": "Fingerprint verification failed (NON-MATCH).", **log_data}

        # ALL GATES PASSED
        log_data["final_result"] = "ACCESS GRANTED"
        self._log_attempt(log_data)
        
        # Retrieve PII Data directly from the dataset for the digital card
        row = self.full_dataset[self.full_dataset['aadhaar_number'] == str(synthetic_id)].iloc[0]

        return {
            "status": "ACCESS GRANTED",
            "reason": "All biometric and credential gates passed successfully.",
            "demo_details": {
                "name": row['name'],
                "age": str(row['age']),
                "gender": row['gender'],
                "address": row['address'],
                "aadhaar_number": str(row['aadhaar_number']),
                "face_path": row['face_path']
            },
            **log_data
        }
