import os
import cv2

class FingerprintVerifier:
    def __init__(self, match_threshold=15):
        """
        match_threshold: minimum number of good matches required to verify the fingerprint.
        """
        self.match_threshold = match_threshold
        # Initialize ORB detector
        self.orb = cv2.ORB_create()
        # Initialize Brute-Force Matcher using Hamming distance (for ORB)
        self.bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    def verify_fingerprint(self, reference_image_path: str, probe_image_path: str) -> dict:
        """
        Verifies if the probe fingerprint matches the enrolled reference fingerprint.
        """
        if not os.path.exists(reference_image_path):
            return {"status": "ERROR", "message": f"Reference image missing: {reference_image_path}"}
        if not os.path.exists(probe_image_path):
            return {"status": "ERROR", "message": f"Probe image missing: {probe_image_path}"}

        try:
            # Read images in grayscale
            ref_img = cv2.imread(reference_image_path, cv2.IMREAD_GRAYSCALE)
            probe_img = cv2.imread(probe_image_path, cv2.IMREAD_GRAYSCALE)
            
            if ref_img is None or probe_img is None:
                return {"status": "ERROR", "message": "Failed to load one or both fingerprint images."}

            # Find keypoints and descriptors
            kp1, des1 = self.orb.detectAndCompute(ref_img, None)
            kp2, des2 = self.orb.detectAndCompute(probe_img, None)
            
            # If no descriptors found
            if des1 is None or des2 is None:
                return {
                    "status": "NON_MATCH",
                    "score": 0,
                    "message": "Fingerprint match failed. No features detected."
                }
                
            # Match descriptors
            matches = self.bf.match(des1, des2)
            
            # Sort them in the order of their distance
            matches = sorted(matches, key=lambda x: x.distance)
            
            # Count "good" matches (distance < threshold, e.g., 50 for ORB)
            good_matches = [m for m in matches if m.distance < 50]
            score = len(good_matches)
            
            verified = score >= self.match_threshold
            
            return {
                "status": "MATCH" if verified else "NON_MATCH",
                "score": score,
                "threshold": self.match_threshold,
                "message": "Fingerprint matched successfully." if verified else "Fingerprint match failed."
            }
            
        except Exception as e:
            return {
                "status": "ERROR",
                "message": f"Fingerprint verification error: {str(e)}"
            }

if __name__ == "__main__":
    verifier = FingerprintVerifier()
    print("FingerprintVerifier module is ready.")
