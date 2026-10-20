<div align="center">

# 🛡️ Identity Shield
### Aadhaar-Inspired Multi-Layer Biometric Defense Framework

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-DeepFace-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)](https://tensorflow.org)
[![License](https://img.shields.io/badge/License-Academic-blueviolet?style=for-the-badge)](LICENSE)

> A sequential **5-Gate Hard-Security Framework** that defends against synthetic identities, face spoofing, deepfakes, and fingerprint presentation attacks — inspired by India's Aadhaar biometric authentication architecture.

</div>

---

## 📌 Overview

**Identity Shield** is an academic research prototype that simulates a government-grade biometric identity verification system, modeled after India's **Aadhaar** infrastructure. The core design principle is **sequential hard-failure**: every authentication attempt must clear **5 independent security gates in strict order**. If any gate fails, access is denied immediately and the failure is logged — there is no fallback, no retry, and no partial success.

The system covers the full attack surface of a real-world biometric identity platform, including:
- **Credential forgery** — stolen or guessed identity numbers
- **Face presentation attacks** — printed photographs, screen replays
- **Face impersonation** — deepfakes and GAN-generated faces
- **Fingerprint spoofing** — gummy fingers, synthetic prints
- **Cross-modal attacks** — genuine face paired with a different person's fingerprint

The research component includes an **Attack Test Matrix** with 52 documented attack scenarios mapped across 27 attack types. Each test case is run through the pipeline and the exact gate that blocks it is recorded.

> **Disclaimer:** This is an academic research prototype for educational and security research purposes. It is **not** affiliated with UIDAI or any government authority. All identity data used is purely synthetic and generated for research.

---

## 🔐 The 5-Gate Security Pipeline

The pipeline enforces a **strict sequential evaluation** — no gate can be skipped or bypassed. Each gate uses a different algorithmic approach, ensuring that no single attack vector can defeat multiple layers simultaneously.

```
  User Input
      │
      ▼
┌─────────────────────────────────────────────────────────────┐
│  GATE 1 — Credential Verification                           │
│  SHA-256 cryptographic hash of 12-digit Aadhaar number      │
└───────────────────────────┬─────────────────────────────────┘
                            │ ✅ Pass  /  ❌ Blocked → Access Denied
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  GATE 2 — Face Liveness Detection (PAD)                     │
│  Random Forest classifier on 96-dim RGB histogram           │
└───────────────────────────┬─────────────────────────────────┘
                            │ ✅ Pass  /  ❌ Blocked → Presentation Attack Logged
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  GATE 3 — Face Verification (1:1 Matching)                  │
│  FaceNet embeddings via DeepFace (cosine similarity)        │
└───────────────────────────┬─────────────────────────────────┘
                            │ ✅ Pass  /  ❌ Blocked → Impostor Detected
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  GATE 4 — Fingerprint Liveness Detection (PAD)              │
│  Texture-based statistical analysis (LBP + variance)        │
└───────────────────────────┬─────────────────────────────────┘
                            │ ✅ Pass  /  ❌ Blocked → Spoofed Print Detected
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  GATE 5 — Fingerprint Verification (1:1 Matching)           │
│  ORB feature descriptors + BFMatcher (Hamming distance)     │
└───────────────────────────┬─────────────────────────────────┘
                            │ ✅ All 5 Gates Passed
                            ▼
                🟢 IDENTITY VERIFIED
```

---

## 🖥️ Live Demo — Genuine User Verification

The following walkthrough demonstrates a successful end-to-end verification for a genuine enrolled user (**Swati Malhotra**, ID: `955137883716`).

---

### Step 1 — Identity Credential Entry

The user enters their 12-digit Aadhaar-style identity number into the portal. Gate 1 validates this credential by computing its **SHA-256 cryptographic hash** and comparing it against the stored hash in the SQLite database. Raw identity numbers are never stored — only their hashes — preventing exposure even if the database is compromised. If the number is unregistered, forged, or tampered with, access is denied immediately before any biometric data is even requested.

![Step 1 - Identity Credential Entry](aadhaar-identity-shield/data/docs/step1_identity.png)

---

### Step 2 — Face Upload & Liveness Check

The user uploads a face image. The system first runs a **Presentation Attack Detection (PAD)** check using a Random Forest classifier trained on 96-dimensional RGB histogram features extracted from the image. This gate is designed to distinguish a live face from a flat attack surface such as a printed photo, phone screen replay, or mask. Only a live, real face passes this gate. If blocked, the incident is flagged as a **face presentation attack**.

A genuine live face then proceeds to **Gate 3: 1:1 Face Verification**, which extracts a 128-dimensional embedding using **FaceNet via the DeepFace library** and computes cosine similarity against the enrolled face embedding stored for that identity. If the similarity falls below the acceptance threshold, access is blocked as an impostor attempt.

![Step 2 - Face Upload and Liveness Check](aadhaar-identity-shield/data/docs/step2_face.png)

---

### Step 3 — Fingerprint Upload & Liveness Check

The user uploads a fingerprint scan. **Gate 4** runs a **texture-based statistical PAD** using Local Binary Pattern (LBP) analysis and variance metrics to detect gummy fingers, synthetic prints, or altered fingerprints. Artificial fingerprints tend to have lower texture variance and unnatural LBP distributions that this classifier exploits.

A live fingerprint then passes to **Gate 5: 1:1 Fingerprint Verification**, which extracts **ORB (Oriented FAST and Rotated BRIEF) feature descriptors** from the scan and performs matching against the reference fingerprint using **BFMatcher with Hamming distance**. A match score below the threshold results in an immediate block.

![Step 3 - Fingerprint Upload and Liveness Check](aadhaar-identity-shield/data/docs/step3_fingerprint.png)

---

### Step 4 — Verified: Digital Identity Card Issued

All 5 gates passed successfully. The system issues a **Digital Identity Card** displaying the user's enrolled name, Aadhaar number, and a ✅ Verified badge confirming the full 5-gate clearance. The verification timestamp and gate-by-gate status are logged in the database for audit trail purposes. The card is rendered directly in the browser — no data is transmitted externally.

![Step 4 - Identity Verified Result](aadhaar-identity-shield/data/docs/step4_result_genuine.png)

---

## 🛠️ Technology Stack

The system is built entirely with open-source components and requires no cloud APIs or external biometric services.

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **API / Backend** | Python 3.11, FastAPI, Uvicorn | REST API server hosting the 5-gate pipeline |
| **Frontend** | Vanilla HTML5, CSS3, JavaScript | Browser-based verification portal and research UI |
| **Deep Learning** | TensorFlow, DeepFace (FaceNet) | Face embedding extraction for 1:1 matching |
| **Machine Learning** | Scikit-learn (Random Forest) | PAD classifiers for face and fingerprint liveness |
| **Computer Vision** | OpenCV | ORB feature extraction for fingerprint matching |
| **Database** | SQLite | Stores identity hashes and enrolled biometric references |

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.11** or newer
- Install all required dependencies:

```bash
pip install fastapi uvicorn deepface tensorflow scikit-learn opencv-python pandas numpy joblib
```

> ℹ️ DeepFace will automatically download the FaceNet model weights on first run (~90 MB). Ensure you have an internet connection for the first launch.

### Run the Application

Navigate to the project folder and double-click **`run.bat`**, or run it from the terminal:

```bash
aadhaar-identity-shield\run.bat
```

**What `run.bat` does automatically:**
1. Sets the Python encoding environment to UTF-8
2. Starts the **FastAPI backend** on `http://127.0.0.1:8000`
3. Loads the trained **DeepFace FaceNet** and **Scikit-learn PAD** models into memory
4. Waits 3 seconds for the server to warm up
5. Opens **`frontend/index.html`** in your default browser

> ⚠️ Keep the terminal window open while testing — it hosts the live API server. Closing it will shut down the backend.

---

## 🧪 Test Credentials (Demo Dataset)

The repository includes a small **Demo Dataset** with 3 synthetic enrolled identities for immediate testing. Use the following credentials to test a successful genuine verification:

| Field | Value |
|-------|-------|
| **Identity Number** | `955137883716` |
| **Enrolled Name** | Swati Malhotra |
| **Face Image Path** | `data/demo_dataset/faces/woman_3434.jpg` |
| **Fingerprint Path** | `data/demo_dataset/fingerprints/540__F_Right_ring_finger.BMP` |

Enter the identity number, upload the matching face and fingerprint from the `demo_dataset/` folder, and click **Verify**. All 5 gates will pass and the **Digital Identity Card** with ✅ Verified status will be displayed.

To test a **failed verification**, try uploading a mismatched fingerprint (e.g., `326__M_Left_ring_finger_CR.BMP`) — Gate 5 will block it as a fingerprint mismatch.

---

## 🔬 Research Analysis Mode

The **Research Analysis** tab in the web portal is the core academic component of this project. It allows researchers to systematically test the system's response to different attack types and verify that the correct gate blocks each specific attack.

### How It Works

1. Select or enter a synthetic identity number
2. Upload a **spoofed** or **mismatched** biometric (face/fingerprint)
3. Click **Run Analysis**
4. The system runs the full 5-gate pipeline and returns:
   - Which gate blocked the attempt
   - The matched **Attack Type** from the Attack Test Matrix
   - The **Attack Category** (Impostor / PAD / Cross-Modal etc.)
   - A description of why this gate is the correct defense

### Attack Categories Covered

| Category | Description | Example |
|----------|-------------|---------|
| 🎭 **Impostor Attacks** | A different real person's genuine biometrics | Wrong face or fingerprint entirely |
| 📸 **Face Presentation Attacks** | A flat 2D surface mimicking a face | Printed photograph, phone screen |
| 🤖 **Deepfake / Synthetic Face** | GAN or AI-generated face image | StyleGAN face, face swap output |
| 👆 **Fingerprint Spoofing** | Artificial or reconstructed fingerprint | Gummy finger, silicone cast, synthetic print |
| 🔀 **Cross-Modal Attacks** | Genuine biometrics from two different people | Correct face + wrong fingerprint |
| 🔑 **Credential Attacks** | Invalid or forged identity numbers | Random number, brute-force attempt |

### Attack Test Matrix

The `attack_test_matrix.csv` contains **52 test cases** across **27 named attack types**. Each row defines:
- The attack name and category
- The identity, face, and fingerprint inputs used
- The expected gate that should block it
- The actual gate result after running the pipeline

---

## 📂 Project Structure

```
aadhaar-security-framework/              ← GitHub Repository Root
│
├── README.md                            ← Project documentation
│
└── aadhaar-identity-shield/             ← Core Project Folder
    ├── run.bat                          ← One-click launcher (Windows)
    ├── .gitignore
    │
    ├── src/                             ← All backend Python source code
    │   ├── api/
    │   │   └── main.py                  ← FastAPI entry point & route handlers
    │   │
    │   ├── authentication/              ← Core 5-Gate pipeline modules
    │   │   ├── credential.py            ← Gate 1: SHA-256 credential hash check
    │   │   ├── face_pad.py              ← Gate 2: Face liveness (PAD) classifier
    │   │   ├── face.py                  ← Gate 3: FaceNet 1:1 face verification
    │   │   ├── fingerprint_pad.py       ← Gate 4: Fingerprint liveness (PAD)
    │   │   ├── fingerprint.py           ← Gate 5: ORB fingerprint 1:1 matching
    │   │   └── fusion.py               ← Pipeline orchestrator (runs all 5 gates)
    │   │
    │   └── database/
    │       ├── database.py              ← SQLite connection & query helpers
    │       ├── schema.sql               ← Database schema definition
    │       └── identity_system.db      ← Pre-populated SQLite database
    │
    ├── frontend/
    │   └── index.html                   ← Full single-page web portal (no framework)
    │
    ├── models/                          ← Pre-trained ML models (ready to use)
    │   ├── face_pad/
    │   │   ├── rf_face_pad.pkl          ← Trained Random Forest face PAD model
    │   │   └── train_face_pad.py        ← Training script for reproducibility
    │   └── fingerprint_pad/
    │       ├── rf_fp_pad.pkl            ← Trained Random Forest fingerprint PAD model
    │       └── train_fp_pad.py          ← Training script for reproducibility
    │
    └── data/
        ├── demo_dataset/                ← 3 synthetic enrolled test identities
        │   ├── faces/                   ← 3 face images
        │   └── fingerprints/            ← 3 fingerprint scans
        ├── aadhaar_dataset.csv          ← Full synthetic identity registry
        ├── attack_test_matrix.csv       ← 52 attack test scenarios
        └── docs/                        ← UI screenshots & performance graphs
```

---

## 📊 Research Findings

The system was evaluated against 52 systematically designed attack scenarios covering all major biometric attack categories. The multi-gate compounding effect ensures that the overall system security is significantly stronger than any individual gate.

| Metric | Result |
|--------|--------|
| Total Attack Scenarios Tested | **52** test cases |
| Unique Attack Types Documented | **27** named attack types |
| Security Gates | **5** fully independent verification layers |
| Unauthorized Acceptance Rate | **< 2%** overall (multi-gate compounding) |
| Attack Detection Rate | **> 98%** across all spoofing categories |
| Face PAD Accuracy | **~94%** on held-out test set |
| Fingerprint PAD Accuracy | **~91%** on held-out test set |

The compounding effect of 5 independent gates means an attacker must simultaneously defeat all 5 distinct algorithmic checks — making end-to-end bypass exponentially harder than bypassing any single gate.

---

<div align="center">

*Built for academic research in Information Security*
*All biometric data in this project is 100% synthetic and does not represent any real individual.*

</div>
