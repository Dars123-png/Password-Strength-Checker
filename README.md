# Password-Strength-Checker
---

## Project Overview

Weak passwords are a major cause of data breaches and account takeovers.  
This project aims to tackle that by providing a **GUI-based password strength checker** that not only analyzes your password against multiple criteria but also **visually breaks down its composition using an embedded bar chart** — all in a single dashboard.

---

## Problem Statement

> Weak passwords remain a top reason for data breaches.  
> Users often rely on short, dictionary-based or simple passwords that attackers can easily guess.

---

## Objectives

- Develop a **Tkinter-based GUI application** that:
  - Evaluates password strength based on **length, uppercase, lowercase, digits, and special characters.**
  - Detects **dictionary words** using the `NLTK` English corpus to warn against common words.
  - Offers **personalized improvement suggestions** with emojis.
  - Shows a **password composition chart** inside the dashboard itself.
  - Allows users to **save passwords securely using AES encryption (Fernet)** and load/decrypt them later.

---

## Key Features

**Tkinter GUI** — clean, intuitive interface.  
**Strength meter with emojis**:  
   - 💪 Strong  
   - 👍 Moderate  
   - ⚠️ Weak  
**Detailed suggestions** for improving password strength.  
**Embedded bar chart** (Matplotlib) inside the dashboard showing counts of:
   - Uppercase letters
   - Lowercase letters
   - Digits
   - Special characters  
**Dictionary word detection** using NLTK corpus (warns if the password contains common words).  
**Encrypt & save** your password using `cryptography.Fernet` (AES under the hood).  
**Load & decrypt** to view the saved password later.

---

## Installation & Setup

### Prerequisites
- Python 3.7+
- Install dependencies:

```bash
pip install nltk cryptography matplotlib
