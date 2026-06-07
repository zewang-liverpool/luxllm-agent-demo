\# Source Code Package



This directory contains the minimal source-code package for the LuxLLM-Agent demo.



It is intentionally smaller than the full development workspace. The goal is to expose the core implementation needed to understand the agent, fallback policy, LLM decision layer, replay summarisation tools, and demo scripts.



\## Structure



```text

src/

├── agent/

│   ├── main.py

│   ├── agent.py

│   ├── baseline\_agent.py

│   ├── rule\_policy.py

│   ├── llm\_decider.py

│   ├── action\_planner.py

│   ├── game\_memory.py

│   └── config.py

├── viewer\_tools/

│   ├── state\_summarizer.py

│   └── record\_match\_result\_from\_console.py

└── scripts/

&#x20;   ├── run\_match\_llm.bat

&#x20;   └── run\_v09c\_pipeline.bat

