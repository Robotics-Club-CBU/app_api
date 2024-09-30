# API for Robotics Car App in an IoT System

## Overview

The robotics car app uses APIs to interact with the car in an IoT ecosystem. The APIs allow the app to **send commands** (e.g., turning lights on/off, controlling indicators) and **receive data** (e.g., temperature, battery status). The car is equipped with sensors and actuators connected to a microcontroller (e.g., ESP32), which communicates with a cloud-based database like **InfluxDB** via these APIs.

### How the APIs Work

1. **`POST /write`:** This API endpoint sends data from the car to the cloud (InfluxDB).
   - **Use case:** Sending sensor data like temperature, battery status, and actuator states like lights or indicators.
   
2. **`GET /read`:** This API endpoint fetches data from the cloud (InfluxDB) for the last 24 hours.
   - **Use case:** Retrieving historical data to monitor car conditions over time.

### Key Components of the API

- **IoT Sensors:** Collect data such as temperature and battery percentage.
- **Actuators:** Control the car’s physical components like lights and indicators.
- **ESP32/Microcontroller:** Intermediary device that communicates with the API and controls the hardware.
- **InfluxDB:** Cloud database that stores sensor data and actuator statuses.
- **Flask API:** Provides endpoints (`/write` and `/read`) for sending and receiving data to/from the database.

---

## `POST /write` - Sending Data

### Functionality
This endpoint is responsible for **sending sensor data and actuator states** to the cloud from the car. The data includes:
- **Temperature**: Measured in Celsius from the car’s sensors.
- **Battery Percentage**: Represents the battery level in percentage.
- **Lights Status**: Whether the car lights are ON (`1`) or OFF (`0`).
- **Indicator Status**: Whether the left and right indicators are ON (`1`) or OFF (`0`).

### Example Request (from car to cloud)
```json
POST /write HTTP/1.1
Host: your_api_host.com
Content-Type: application/json

{
    "vehicle": "robotics_car_01",
    "temperature": 32.5,
    "battery_percentage": 80,
    "lights_on": 1,
    "indicator_left_on": 0,
    "indicator_right_on": 1
}
```

### How it Works
- The microcontroller (ESP32) collects sensor data and sends it to the cloud using this API.
- The API stores this data in **InfluxDB** under the `car_metrics` series.
- The **vehicle** tag ensures that data from different cars is separated.

### Example Response
```json
{
    "message": "Car data written to InfluxDB"
}
```

- If the data is successfully written, the response confirms the operation.

---

## `GET /read` - Fetching Data

### Functionality
This endpoint fetches **the last 24 hours of data** for a given vehicle. It retrieves:
- **Temperature history**.
- **Battery percentage history**.
- **Lights status (ON/OFF)**.
- **Indicator status (left and right)**.

### Example Request (from app to cloud)
```http
GET /read HTTP/1.1
Host: your_api_host.com
```

### How it Works
- When the app calls this API, it queries the InfluxDB for data logged within the last 24 hours for the specified car.
- The **InfluxDB** query used:
  ```sql
  SELECT * FROM 'car_metrics' 
  WHERE time >= now() - interval '24 hours'
  ```

### Example Response
The API will return the car’s data over the last 24 hours in JSON format:

```json
[
    {
        "time": "2024-09-30T10:00:00Z",
        "vehicle": "robotics_car_01",
        "temperature": 32.5,
        "battery_percentage": 80,
        "lights_on": 1,
        "indicator_left_on": 0,
        "indicator_right_on": 1
    },
    {
        "time": "2024-09-30T11:00:00Z",
        "vehicle": "robotics_car_01",
        "temperature": 33.1,
        "battery_percentage": 78,
        "lights_on": 0,
        "indicator_left_on": 0,
        "indicator_right_on": 1
    },
    ...
]
```

- Each entry corresponds to a timestamp, showing the values of various sensors and actuators at that time.
- The app can use this data to visualize trends, monitor battery usage, temperature changes, and check the status of lights and indicators.

---

## Use in IoT System

### Scenario 1: Sending Sensor Data
1. The **ESP32** in the car measures the **temperature** and **battery percentage** and checks the status of the **lights** and **indicators**.
2. This data is sent via a **POST request** to the `/write` endpoint.
3. The **API stores** this information in the **InfluxDB** cloud database.

### Scenario 2: Controlling Actuators
1. The user sends a command to turn on/off the **lights** or **indicators** through the app.
2. The app sends this command via the `/write` endpoint with the appropriate values (e.g., `lights_on: 1` for ON).
3. The microcontroller receives this data and activates/deactivates the actuators accordingly.

### Scenario 3: Retrieving Data
1. The app periodically calls the **`/read` endpoint** to check the historical data for the car.
2. This can be useful for monitoring the car's performance over time, such as seeing how the **battery drains** or how the **temperature fluctuates**.


## Conclusion

The **robotics car APIs** play a crucial role in an IoT system by providing a mechanism for communication between the car's sensors/actuators and the cloud. The **`POST /write`** API allows the car to send real-time data, while the **`GET /read`** API enables the app to retrieve and analyze historical data. By using these APIs, the car can be remotely monitored and controlled, forming an effective and responsive IoT system for robotics cars.
