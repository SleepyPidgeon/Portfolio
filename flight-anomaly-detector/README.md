# Ver 0.0.2

## [Architecture Upgrade] - From Monolithic Script to Event-Driven Pipeline

### Added
- **Distributed Pub-Sub Architecture:** Migrated the system from a single blocking script to a decoupled, event-driven design using an **MQTT Message Broker (Eclipse Mosquitto)**.
- **Concurrent Flight Simulation Node (`flight_generator.py`):** Replaced the single-plane script with an asynchronous engine powered by Python's `asyncio`. The simulator now handles **four simultaneous aircraft flights** tracking their own physics layers concurrently.
- **Dedicated Logging Microservice (`logger.py`):** Isolated database operations into a standalone background consumer script that listens to network traffic and commits data payloads independently.
- **Aircraft State Tracking Model:** Replaced simple instant random variables with an intelligent structural state machine. Anomalies now feature a programmatic persistent cooldown phase (15-second tracking windows) before safely recovering.

### Changed
- **Database Routing Engine (`config.py`):** Replaced local directory mapping strings with deterministic **Absolute Structural File Paths (`os.path.abspath`)** to guarantee Streamlit web tasks and database loggers target the exact same database file across different project execution folders.
- **Pygame Multi-Target Radar Interface (`radarview.py`):** Upgraded the visual interface from tracking a single global hardcoded coordinate pair to maintaining an in-memory **Dynamic Track Database Dictionary**. The radar automatically registers, tracks, and visually labels new flights as they appear on the MQTT stream.
- **Streamlit Analytical Dashboard Layout (`app_dashboard.py`):** Shifted the web monitoring dashboard from a single-stream format to a scalable analytics engine featuring an interactive **Fleet Selection Sidebar Dropdown Drop-Menu** to filter historical telemetry plots by individual flight numbers.
- **Execution Workflow Performance:** Optimally tuned random anomaly generation logic rules down from an aggressive 1.0% check per second to a realistic fractional metric (0.05% odds) to better replicate standard commercial aviation control center frequency profiles.


# Build Ver 0.0.1
- Radar Application added
- Streamlit web application added