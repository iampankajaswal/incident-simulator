## Milestone 1 — High CPU Incident Simulation

The first milestone implements a complete local incident lifecycle without
external monitoring dependencies.

### Incident Flow

```text
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
