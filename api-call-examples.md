# Medspa API cURL Examples

This document provides cURL examples for each endpoint in the Medspa API. All endpoints are prefixed with `/v1`.

## Medspa Endpoints

### List All Medspas
```bash
curl -X GET "http://localhost:8000/v1/medspas"
```

### Get Medspa by ID
```bash
curl -X GET "http://localhost:8000/v1/medspas/1"
```

### Create Medspa
```bash
curl -X POST "http://localhost:8000/v1/medspas" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Serenity Wellness Spa",
    "address": "123 Madison Avenue, New York, NY 10016",
    "phone_number": "212-555-0123",
    "email_address": "info@serenitywellness.com"
  }'
```

### Update Medspa
```bash
curl -X PATCH "http://localhost:8000/v1/medspas/1" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Serenity Wellness Spa & Clinic",
    "phone_number": "212-555-0124"
  }'
```

### Delete Medspa
```bash
curl -X DELETE "http://localhost:8000/v1/medspas/1"
```

## Services Endpoints

### List All Services
```bash
curl -X GET "http://localhost:8000/v1/services"
```

### List Services by Medspa ID
```bash
curl -X GET "http://localhost:8000/v1/services?medspa_id=1"
```

### Get Service by ID
```bash
curl -X GET "http://localhost:8000/v1/services/1"
```

### Create Service
```bash
curl -X POST "http://localhost:8000/v1/services" \
  -H "Content-Type: application/json" \
  -d '{
    "medspa_id": 1,
    "name": "Botox Treatment",
    "description": "Neuromodulator treatment to reduce fine lines and wrinkles",
    "price": "450.00",
    "duration": 30
  }'
```

### Update Service
```bash
curl -X PATCH "http://localhost:8000/v1/services/1" \
  -H "Content-Type: application/json" \
  -d '{
    "price": "475.00",
    "duration": 45
  }'
```

### Delete Service
```bash
curl -X DELETE "http://localhost:8000/v1/services/1"
```

## Appointments Endpoints

### List All Appointments
```bash
curl -X GET "http://localhost:8000/v1/appointments"
```

### List Appointments by Status
```bash
curl -X GET "http://localhost:8000/v1/appointments?status=scheduled"
```

### List Appointments by Date
```bash
curl -X GET "http://localhost:8000/v1/appointments?date=2024-03-28"
```

### List Appointments by Status and Date
```bash
curl -X GET "http://localhost:8000/v1/appointments?status=scheduled&date=2024-03-28"
```

### Get Appointment by ID
```bash
curl -X GET "http://localhost:8000/v1/appointments/1"
```

### Create Appointment
```bash
curl -X POST "http://localhost:8000/v1/appointments" \
  -H "Content-Type: application/json" \
  -d '{
    "medspa_id": 1,
    "start_time": "2024-03-28T14:00:00",
    "services": [1, 2]
  }'
```

### Update Appointment
```bash
curl -X PATCH "http://localhost:8000/v1/appointments/1" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "completed",
    "services": [1, 2, 3]
  }'
```

### Delete Appointment
```bash
curl -X DELETE "http://localhost:8000/v1/appointments/1"
```
