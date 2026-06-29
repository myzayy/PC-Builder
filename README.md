# 💻 PC Builder (Console Version)

This project is an interactive personal computer configuration tool featuring an automatic hardware compatibility validation system.

> 📌 **Project Roadmap:** The current console version serves as the architectural core (Backend/Business Logic) of the application. I designed it with a strict separation of business logic and user interface (SRP), making this engine fully prepared for my future plans to migrate the project into a visual environment, such as a web application (using Django/FastAPI) or a desktop GUI app.
---

## Features & Current State

At this stage, the configurator functions as a complete product within the CLI environment, supporting 8 distinct hardware components.

### 1. Flexible Configuration Management
* **Dynamic Component Selection:** Seamless step-by-step PC assembly (CPU, Motherboard, GPU, RAM, PSU, Storage, CPU Cooler, Case) driven by a dynamic JSON database.
* **Universal Component Removal:** The ability to completely reset/remove (not just replace) any slot from the current build using a unified attribute-handling method.
* **Quantity Tracking:** Specialized logic for RAM configuration, allowing users to choose the number of sticks (1 to 4) with bulletproof input validation.

### 2. Intelligent Compatibility Validator (`validator.py`)
The application features a built-in rule engine that protects users from making bad hardware purchases by analyzing the build through two main lenses:

* **Electrical & Technical Compatibility:**
  * Matching socket types between the CPU, motherboard, and the cooler's mounting brackets.
  * Verifying memory generations (e.g., throwing an error if trying to slot DDR4 RAM into a DDR5 motherboard).
  * Enforcing motherboard RAM slot limitations against the chosen stick count.
  * Verifying video output presence (if a CPU lacks integrated graphics and no discrete GPU is installed, the system warns the user).
  * Real-time system power consumption calculation, verifying PSU wattage with a 20% safety headroom.
* **Physical Dimensions (Spatial Compatibility):**
  * Validating motherboard form-factors against case specifications (ATX/Mini-ITX matching).
  * Checking maximum GPU length restrictions to ensure the graphics card fits into the chosen case.
  * Monitoring maximum CPU cooler tower height to prevent it from hitting the case's side panel.

### 3. Data Handling & Exporting
* **Dynamic Database:** All hardware specifications, power metrics, physical sizes, and prices are fetched directly from a decoupled `database.json` file.
* **Receipt Generation:** Once a build achieves full compatibility, it can be exported into a cleanly formatted text file (`pc_build.txt`). Exporting is strictly blocked if any errors remain unresolved.

---

## 🛠️ Tech Stack
* **Language:** Python 3.12+
* **Concepts:** Object-Oriented Programming (OOP), DRY, SRP, State Management, JSON Data Serialization.

## 🚀 How to Run
1. Ensure you have Python 3 installed on your machine.
2. Run the entry point file from your terminal:
   ```bash
   python main.py
