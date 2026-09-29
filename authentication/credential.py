import sqlite3
import hashlib
import os

DB_PATH = r"D:\7th Semester\Information Security\aadhaar-inspired-security\database\identity_system.db"

class CredentialValidator:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        
    def _hash_credential(self, identifier: str) -> str:
        """Hash the provided credential string using SHA-256."""
        hash_obj = hashlib.sha256(identifier.encode())
        return hash_obj.hexdigest()

    def verify_credential(self, identifier: str) -> dict:
        """
        Verify if the given identifier (e.g., synthetic 12-digit ID) 
        exists in the credential database.
        Returns the identity_id if valid, else returns None.
        """
        # Step 1: Hash the incoming claim
        hashed_claim = self._hash_credential(identifier)
        
        # Step 2: Query database securely
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT identity_id FROM identity WHERE credential_hash = ?", (hashed_claim,))
            result = cursor.fetchone()
            
            conn.close()
            
            if result:
                return {
                    "status": "VALID",
                    "identity_id": result[0],
                    "message": "Credential validated successfully."
                }
            else:
                return {
                    "status": "INVALID",
                    "identity_id": None,
                    "message": "Access Denied: Credential not recognized."
                }
                
        except sqlite3.Error as e:
            return {
                "status": "ERROR",
                "identity_id": None,
                "message": f"Database error: {e}"
            }

# Simple test block
if __name__ == "__main__":
    validator = CredentialValidator()
    
    print("Testing Valid Credential (900100000000):")
    print(validator.verify_credential("900100000000"))
    
    print("\nTesting Invalid Credential (123456789012):")
    print(validator.verify_credential("123456789012"))
