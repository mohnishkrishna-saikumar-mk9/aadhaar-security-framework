import os
from deepface import DeepFace

class FaceVerifier:
    def __init__(self, model_name="Facenet", detector_backend="skip"):
        self.model_name = model_name
        self.detector_backend = detector_backend

    def verify_face(self, reference_image_path: str, probe_image_path: str) -> dict:
        """
        Verifies if the face in probe_image_path matches the face in reference_image_path.
        Uses DeepFace for detection, alignment, and verification.
        """
        if not os.path.exists(reference_image_path):
            return {"status": "ERROR", "message": f"Reference image missing: {reference_image_path}"}
        if not os.path.exists(probe_image_path):
            return {"status": "ERROR", "message": f"Probe image missing: {probe_image_path}"}

        try:
            # DeepFace verify automatically handles face detection, alignment, embedding extraction, and matching.
            result = DeepFace.verify(
                img1_path=reference_image_path,
                img2_path=probe_image_path,
                model_name=self.model_name,
                detector_backend=self.detector_backend,
                enforce_detection=False # Set to false so it doesn't crash if a face is hard to detect in synthetic/attack images
            )
            
            verified = result.get("verified", False)
            distance = result.get("distance", 1.0)
            
            return {
                "status": "MATCH" if verified else "NON_MATCH",
                "distance": float(distance),
                "threshold": float(result.get("threshold", 0.0)),
                "message": "Face matched successfully." if verified else "Face match failed."
            }
            
        except Exception as e:
            return {
                "status": "ERROR",
                "message": f"Face verification error: {str(e)}"
            }

# Simple test block
if __name__ == "__main__":
    verifier = FaceVerifier()
    print("FaceVerifier module is ready.")
