# CSRF Wizard for Burp Suite

## Introduction

CSRF Wizard is a dynamic and user-friendly Burp Suite extension designed to simplify the process of generating and testing Cross-Site Request Forgery (CSRF) Proofs of Concept (PoCs). Ideal for security researchers, penetration testers, and web developers, this tool aids in validating web application security against CSRF vulnerabilities.

## Features

- **CSRF PoC Generation**: Effortlessly create CSRF PoCs for selected HTTP requests within Burp Suite.
- **Editable PoC Code**: Modify the generated PoC code in a user-friendly pop-up editor.
- **Auto Submit Toggle**: Add an auto-submit feature to the PoC with a simple checkbox.
- **Save Functionality**: Conveniently save PoCs with a `.html` extension, ensuring browser compatibility.
- **Path Copy Option**: Save your PoC and instantly copy its file path to the clipboard for easy access.

## Installation

1. **Download Jython**: Ensure you have the Jython standalone JAR file from [Jython's official website](http://www.jython.org/downloads.html).
2. **Configure Jython in Burp Suite**:
    - Open Burp Suite and navigate to the "Extender" tab.
    - In the "Options" sub-tab, find the Python Environment section.
    - Click "Select file..." and choose your downloaded Jython standalone JAR file.
3. **Add CSRF Wizard Extension**:
    - Copy the CSRF Wizard Python script.
    - Go to the "Extender" tab in Burp Suite, then to the "Extensions" sub-tab.
    - Click "Add", select "Python" as the extension type, and paste or select your script file.

## Usage

1. **Generate CSRF PoC**:
    - Right-click on a request in any Burp Suite tool (Proxy, Target, etc.).
    - Select "Generate CSRF PoC" from the context menu.
    - An editor pop-up with the PoC code will be displayed.
2. **Edit and Save PoC**:
    - Modify the PoC as needed directly within the editor.
    - Use the "Auto Submit" checkbox to include or exclude auto-submit functionality.
    - Click "Save to File" to save your PoC, or "Save and Copy Location" to also copy the file path.

## Responsible Use

CSRF Wizard is intended for lawful, ethical, and educational purposes only. Explicit permission is required for testing any target applications. Unauthorized testing of websites, applications, or systems is illegal and unethical.
