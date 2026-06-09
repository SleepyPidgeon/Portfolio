## 🛠️ Prerequisites & Local Installation

### 1. Install Eclipse Mosquitto (MQTT Broker)
Your local computer must host the central message broker service to route communications between your scripts.

* **Windows**: Download and run the official installer from the [Eclipse Mosquitto Downloads](https://mosquitto.org) page. Make sure the background service is running via `services.msc`.
* **macOS**: Install and start the service using Homebrew:
  ```bash
  brew install mosquitto
  brew services start mosquitto
  ```
* **Linux**: Install using your package manager:
  ```bash
  sudo apt update && sudo apt install mosquitto mosquitto-clients
  ```

### 2.Environment Setup
Clone this repository to your local machine, open your terminal inside the project directory, and install the required Python dependencies:

# Install client packages
pip install paho-mqtt pygame pandas streamlit
```

---

## 🚀 Execution Guide (How to Run)

Because this is a decoupled microservice system, scripts must be executed in separate terminal windows. Follow this exact order to prevent data loss or connection drops:

### Step 1: Initialize the Database Schema
Ensure the structural database template file is generated on your machine before running your logging scripts. Run your original database initialization file:
```bash
python create_db.py
```
*(This automatically builds the database file using absolute paths configured in your `config.py` so no scripts conflict).*

### Step 2: Start the Ingestion Node (`logger.py`)
Open a **new terminal window** and run the consumer daemon. It will wait patiently to parse network data packets:
```bash
python logger.py
```

### Step 3: Spin Up the Simulation Engine (`flight_generator.py`)
Open a **third terminal window** and launch the aircraft data broadcast array. You will see coordinates computing and publishing immediately:
```bash
python flight_generator.py
```

### Step 4: Launch the Front-End Interfaces (Any Order)
With data flowing smoothly across the MQTT pipeline, open new terminal windows to start your preferred monitoring apps:

* **To see the Desktop Radar Screen:**
  ```bash
  python radarview.py
  ```
* **To open the Web Analytics Engine Dashboard:**
  ```bash
  python -m streamlit run app_dashboard.py
  ```

---

## 🛑 How to Stop the System
To shut down the architecture cleanly without leaving orphaned Python processes in your system memory:
1. Focus on any active terminal window.
2. Press **`Ctrl + C`** to break out of the script loops. 