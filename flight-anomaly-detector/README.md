Version 0.0.2
**Upgrades:**
Architecture Upgrade: From a Monolithic Script to Event-Driven Pipeline

**Added:**
-Migrated the system from a single block script to a decoupledm event-driven desing using an MQTT Message Broker (Eclipse Mosquitto).
-Added a Dedicated Logging Microservice (`logger.py`), Isolated database operations into a standalone background script that listens to network traffic and commits data payloads independently.
-Added a Concurrent Flight Simulation Node, (`flight_generator.py`) this replaces the single plane script.

**Changes:**
-Replaced local directory mapping strings with deterministic Absolute Structural File Paths (`os.path.abspath`) to guarantee Streamlit web tasks and database loggers target the exact same database file across different project execution folders.
- Pygame Multi-Target Radar Interface (`radarview.py`): Upgraded the visual interface from tracking a single global hardcoded coordinate pair to maintaining an in-memory Dynamic Track Database Dictionary. The radar automatically registers, tracks, and visually labels new flights as they appear on the MQTT stream.
- Streamlit Analytical Dashboard Layout (`app_dashboard.py`): Shifted the web monitoring dashboard from a single-stream format to a scalable analytics engine featuring an interactive Fleet Selection Sidebar Dropdown Drop-Menu to filter historical telemetry plots by individual flight numbers.
- Execution Workflow Performance: Optimally tuned random anomaly generation logic rules down from an aggressive 1.0% check per second to a realistic fractional metric (0.05% odds) to better replicate standard commercial aviation control center frequency profiles.


Build Ver 0.0.1
-Radar Application added
-Streamlit web application added