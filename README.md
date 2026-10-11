## Milestone 1  High CPU Incident Simulation

The first milestone implements a complete local incident lifecycle without
external monitoring dependencies.

### Incident Flow


High CPU Scenario
       |
       v
CPU Stress Simulator
       |
       v
Alert Generated
       |
       v
Incident Created
       |
       v
Timeline Generated
       |
       v
Rules-Based RCA
       |
       v
Incident Resolved



### Health

<img width="829" height="44" alt="image" src="https://github.com/user-attachments/assets/4179ec00-43a2-42b2-8652-872b1e28f453" />

<img width="514" height="230" alt="image" src="https://github.com/user-attachments/assets/7bcbf8b8-20a7-45af-b768-70d832197115" />


### scenarios

<img width="805" height="68" alt="image" src="https://github.com/user-attachments/assets/f29be95d-7006-4d1e-8d25-746c0bfcd398" />

### High Cpu

<img width="1312" height="176" alt="image" src="https://github.com/user-attachments/assets/ef17f146-30f6-4ab9-b0a8-34d7e543c741" />

### incidents

<img width="1916" height="182" alt="image" src="https://github.com/user-attachments/assets/65fc2713-ff9a-4326-8ab6-bee65ccd5411" />

<img width="1052" height="987" alt="image" src="https://github.com/user-attachments/assets/7ea135ce-7976-44eb-8847-1d766720cb00" />

<img width="1017" height="972" alt="image" src="https://github.com/user-attachments/assets/2eb28606-8041-4328-b9d3-2a5db735faa0" />


### timeline

<img width="1920" height="149" alt="image" src="https://github.com/user-attachments/assets/4d82f49f-3db7-4c55-b75d-96f47fe327ab" />

<img width="706" height="586" alt="image" src="https://github.com/user-attachments/assets/a82b50f4-18c1-4762-b69c-28114e5a4447" />



### Swagger

<img width="1539" height="989" alt="image" src="https://github.com/user-attachments/assets/6fc31930-b056-43d7-8f17-c93018ac8285" />



## Milestone 2: Prometheus + Alertmanager Integration

The incident simulator integrates Prometheus and Alertmanager to demonstrate how monitoring alerts can automatically trigger incident management workflows.

### Architecture

1. Prometheus scrapes metrics exposed by the FastAPI application at `/metrics`.
2. Prometheus evaluates alerting rules, including the `HighCPU` rule.
3. When an alert fires, Alertmanager sends a webhook to the incident simulator.
4. FastAPI creates an incident, starts the RCA workflow, and records timeline events.
5. When the alert resolves, the webhook updates the incident status to `RESOLVED`.

### Monitoring Stack

- **Prometheus:** Metrics collection and alert rule evaluation.
- **Alertmanager:** Alert grouping and firing/resolved notification delivery.
- **FastAPI:** Webhook processing and incident lifecycle management.
- **RCA engine:** Deterministic root cause analysis for supported scenarios.
- **Docker Compose:** Local orchestration of Prometheus and Alertmanager.

### Screenshots

#### 1. Prometheus Targets

<img width="1919" height="364" alt="image" src="https://github.com/user-attachments/assets/a3f289d2-7b8c-4cf7-8f8a-e66cb1e1f09a" />


#### 2. Prometheus Alert Rules

<img width="1919" height="534" alt="image" src="https://github.com/user-attachments/assets/7a4f2e42-4497-4b55-a5b9-c4d95a10a2c5" />


#### 3. Alertmanager

<img width="1146" height="198" alt="image" src="https://github.com/user-attachments/assets/74d453f2-a79e-4eec-8440-545cf92a1b1d" />



#### 4. Incident API and RCA

<img width="1920" height="995" alt="image" src="https://github.com/user-attachments/assets/68cc7b06-ca9b-47dc-99b4-bf549d7c6366" />

<img width="1132" height="868" alt="image" src="https://github.com/user-attachments/assets/1cbbf238-4659-4118-a2b1-4107530a0d96" />

<img width="1920" height="273" alt="image" src="https://github.com/user-attachments/assets/413f3b95-25b3-4ff5-923d-c830373df16d" />


#### 4. Webhooks

<img width="1223" height="493" alt="image" src="https://github.com/user-attachments/assets/2531aba4-8587-4379-8ded-e34d9aab069e" />

<img width="1920" height="261" alt="image" src="https://github.com/user-attachments/assets/0f09386e-91c5-45dd-a150-322270596767" />



### Run Locally

Start the monitoring stack:

```bash
docker compose up -d
```

Start the FastAPI application in a separate terminal:

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

<img width="1220" height="543" alt="image" src="https://github.com/user-attachments/assets/88498cb6-0f2d-4e44-9423-d2d18c8deea7" />


<img width="912" height="202" alt="image" src="https://github.com/user-attachments/assets/1dd4a4a0-43b8-4812-bf70-69d7202f66de" />


### Expected Workflow

**CPU simulation -> Prometheus metric -> HighCPU alert -> Alertmanager webhook -> Incident creation -> RCA and timeline -> Incident resolution**

The application currently maintains incident state in memory, so incidents are not persisted across API restarts.
