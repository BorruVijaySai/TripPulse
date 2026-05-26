# TripPulse

TripPulse is a multi-agent travel planning framework that generates personalized multi-day travel itineraries using Large Language Models (LLMs), review-grounded reasoning, and constraint-aware scheduling.

The framework explores two distinct planning pathways:

1. **LLM-Based Planning Pipeline**  
   A generative scheduling pipeline where LLMs perform semantic reasoning, activity selection, and itinerary scheduling.

2. **Deterministic Scheduling Pipeline**  
   A rule-based algorithmic scheduler that enforces strict temporal and budget feasibility through programmatic execution.

The system combines modular agentic reasoning with structured scheduling to generate realistic, personalized, and feasible travel itineraries.

---

# Key Features

- Multi-agent itinerary generation
- Review-grounded recommendation reasoning
- Constraint-aware travel scheduling
- Hybrid LLM + deterministic architecture
- Personalized itinerary generation
- Multi-day trip planning
- Temporal feasibility enforcement
- Budget-aware planning
- LLM-as-a-Judge evaluation framework
- Modular orchestration pipeline

---

# Architecture

```text
User Query
    ↓
Global Orchestrator
    ↓
Domain-Specific Agents
 ├── Accommodation Agent
 ├── Transportation Agent
 ├── Meals Agent
 ├── Attraction Agent
 └── Events Agent
    ↓
Planning Pathways
 ├── LLM-Based Scheduler
 └── Deterministic Scheduler
    ↓
Final Time-Ordered Itinerary
```

---

# Planning Pathways

## 1. LLM-Based Scheduling Pathway

The LLM-based pipeline performs:

- Semantic itinerary reasoning
- Dynamic activity selection
- POI scheduling
- Context-aware planning
- Review-grounded decision making

This pathway allows flexible itinerary generation using LLM reasoning while maintaining structured validation.

---

## 2. Deterministic Scheduling Pathway

The deterministic pipeline performs:

- Rule-based scheduling
- Temporal constraint enforcement
- Transit buffer validation
- Budget-safe execution
- Greedy slot assignment

This pathway guarantees strict feasibility through programmatic scheduling logic.

---

# Multi-Agent Framework

TripPulse decomposes itinerary generation into specialized agents operating on localized contexts:

- Accommodation selection
- Transportation planning
- Restaurant recommendation
- Attraction ranking
- Event filtering

This decomposition reduces reasoning overload and improves planning reliability.

---

# Review-Grounded Planning

The framework augments structured travel data with large-scale review information to capture experiential travel signals such as:

- Safety
- Comfort
- Crowding
- Ambiance
- Service quality
- Traveler suitability

Reviews are distilled into structured **Pros** and **Cons** representations for efficient downstream reasoning.

---

# Supported Models

Current supported model identifiers:

```python
"mistral"
"llama"
"deepseek"
```

---

# Repository Structure

```text
TripPulse/
│
├── agentic_trip/
├── core/
├── evaluation/
├── prompts/
├── postprocess/
├── tools/
├── run.py
├── run_review_pro_cons.py
└── README.md
```

---

# Installation

Clone the repository:

```bash
git clone https://github.com/BorruVijaySai/TripPulse.git
cd TripPulse
```

Create environment:

```bash
conda create -n trippulse python=3.10
conda activate trippulse
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Environment Variables

```bash
export OPENAI_API_KEY=your_key
export GEMINI_API_KEY=your_key
export HF_TOKEN=your_token
```

---

# Running the Framework

TripPulse supports two execution pathways.

---

## 1. Standard Planning Pipeline

Run:

```bash
python run.py
```

### Configure Model and Trip Duration

Inside `run.py`, configure:

```python
MODEL_NAME = "mistral"   # mistral | llama | deepseek
DAY_TYPES = [3,5,7]
```

Example:

```python
MODEL_NAME = "llama"
DAY_TYPES = [5]
```

---

## 2. Review-Grounded Pros/Cons Pipeline

Run:

```bash
python run_review_pro_cons.py
```

### Configure Model and Trip Duration

Inside `run_review_pro_cons.py`, configure:

```python
MODEL_NAME = "mistral"   # mistral | llama | deepseek
DAY_TYPES = [3,5,7]
```

Example:

```python
MODEL_NAME = "deepseek"
DAY_TYPES = [7]
```

---

# DAY_TYPES Configuration

`DAY_TYPES` controls itinerary duration generation.

Examples:

```python
DAY_TYPES = [3]
```

Generates only 3-day itineraries.

```python
DAY_TYPES = [5,7]
```

Generates both 5-day and 7-day itineraries.

```python
DAY_TYPES = [3,5,7]
```

Generates all trip durations.

---

# Evaluation

Go to evaluation directory:

```bash
cd evaluation
```

---

## 1. Structural Constraint Metrics

Run:

```bash
python eval.py --set_type <3/5/7> --evaluation_file_path "generated_file_path"
```

Example:

```bash
python eval.py --set_type 5 --evaluation_file_path "../outputs/mistral_5day.json"
```

This evaluates:

- Structural validity
- Constraint satisfaction
- Budget feasibility
- Entity correctness

---

## 2. Temporal and Continuity Metrics

Run:

```bash
python qualitative_metrics.py --gen_file "generated_plan_path" --anno_file "golden_plan_path"
```

Example:

```bash
python qualitative_metrics.py --gen_file "../outputs/generated.json" --anno_file "../golden/golden_5day.json"
```

This evaluates:

- Temporal consistency
- Activity continuity
- Travel flow coherence
- Chronological correctness

---

## 3. RGPA Review-Grounded Metrics

Run:

```bash
python evaluate_llm_as_judge.py --model mistral --day 5
```

Example:

```bash
python evaluate_llm_as_judge.py --model deepseek --day 7
```

Optional arguments:

```bash
--llm
```

Example:

```bash
python evaluate_llm_as_judge.py --model llama --day 3 --llm
```

This evaluates:

- Review-grounded persona alignment
- Experiential quality
- Personalization quality
- Review-aware recommendation alignment

---

# Research Focus

TripPulse explores:

- Agentic AI systems
- Multi-agent planning
- Constraint-aware itinerary generation
- Review-grounded recommendation systems
- Hybrid deterministic + LLM scheduling
- Personalized travel planning
- Temporal reasoning for travel itineraries

---

# Notes

- API keys should never be committed to the repository.
- Large model inference may require GPU resources.
- Some datasets and APIs are not included in the repository.
- The repository is anonymized for research submission purposes.
- The framework supports both deterministic and LLM-driven scheduling pipelines for comparative evaluation.
```
