# Chapter 2 Reference Plan



## 1. Purpose of This Document



This document plans the citation enhancement for:



```text

docs/dissertation/chapter\_2\_background\_related\_work.md

```



The current Chapter 2 draft provides a safe background and related work structure, but it still needs stronger academic references.



The goal of this reference plan is to identify:



\* which real papers and sources should be cited;

\* which Chapter 2 sections they support;

\* how each source connects to LuxLLM-Agent;

\* what BibTeX keys should be used later;

\* how to avoid overclaiming.



This plan should be used before rewriting Chapter 2 and before updating the project bibliography.



---



## 2. Dissertation Positioning



The dissertation positions LuxLLM-Agent as:



> A decision-trace and action-verification framework for inspecting and evaluating LLM-based agents in Lux AI Season 3.



The related work should therefore support the following ideas:



1\. LLMs can be used as agent components.

2\. LLMs can support reasoning, acting, tool use, planning, and feedback-based behaviour.

3\. LLM outputs need grounding, verification, or affordance constraints before execution.

4\. Games are useful environments for sequential decision-making research.

5\. Complex game agents require evaluation beyond final win/loss.

6\. Traceability and replay-grounded inspection are important for analysing agent behaviour.

7\. Lux AI Season 3 is a suitable multi-agent game environment for this project.



---



## 3. Recommended Citation Themes



Chapter 2 should be strengthened using the following citation themes.



| Theme                            | Purpose in Chapter 2                                               |

| -------------------------------- | ------------------------------------------------------------------ |

| LLM agents                       | Support the idea of LLMs as components in interactive agents       |

| Reasoning and acting             | Support interleaved reasoning/action and decision traces           |

| Tool use and external interfaces | Support the idea that LLMs can be combined with external systems   |

| LLM planning                     | Support LLMs as high-level planners rather than direct controllers |

| Grounding and affordances        | Support rule-based action verification                             |

| Embodied / game agents           | Support the need for environment feedback and executable skills    |

| Game AI                          | Support games as sequential decision-making testbeds               |

| Multi-agent game AI              | Support Lux AI as a complex multi-agent setting                    |

| Evaluation and traceability      | Support the need for metrics beyond final score                    |

| Lux AI Season 3                  | Support the choice of experimental environment                     |



---



## 4. Recommended References



## 4.1 LLM Agents, Reasoning, and Acting



### `yao2023react`



\*\*Paper:\*\* ReAct: Synergizing Reasoning and Acting in Language Models

\*\*Authors:\*\* Yao et al.

\*\*Use in dissertation:\*\* LLMs can interleave reasoning traces and task-specific actions in interactive decision-making settings.



Suggested use:



\* Chapter 2.2 Large Language Models as Agents

\* Chapter 2.3 LLMs for Planning and Decision Making

\* Chapter 2.7 Explainability, Traceability, and Decision Provenance

\* Chapter 6 Evaluation, when discussing decision traces



Connection to LuxLLM-Agent:



ReAct is useful because LuxLLM-Agent also separates reasoning-like strategic plans from actions. However, LuxLLM-Agent differs because it adds explicit rule-based verification, fallback, caching, and replay-grounded inspection.



Suggested sentence:



> ReAct shows that language models can combine reasoning traces with task-specific actions in interactive decision-making tasks. LuxLLM-Agent follows a related motivation, but uses the LLM output as a structured strategic proposal that must pass rule-based verification before execution.



---



### `shinn2023reflexion`



\*\*Paper:\*\* Reflexion: Language Agents with Verbal Reinforcement Learning

\*\*Authors:\*\* Shinn et al.

\*\*Use in dissertation:\*\* Language agents can use feedback and memory to improve future decisions.



Suggested use:



\* Chapter 2.2 Large Language Models as Agents

\* Chapter 2.8 Evaluation of LLM-based Agents

\* Chapter 7 Future Work, when discussing possible feedback-based improvement



Connection to LuxLLM-Agent:



LuxLLM-Agent currently records decision traces and failure cases. Future versions could use these traces as feedback for strategy refinement, similar in spirit to Reflexion.



Suggested sentence:



> Reflexion demonstrates that language agents can use feedback and memory to improve later behaviour. In LuxLLM-Agent, decision traces are currently used for inspection and evaluation, but they could later support feedback-driven strategy improvement.



---



### `schick2023toolformer`



\*\*Paper:\*\* Toolformer: Language Models Can Teach Themselves to Use Tools

\*\*Authors:\*\* Schick et al.

\*\*Use in dissertation:\*\* LLMs can be combined with external tools and APIs.



Suggested use:



\* Chapter 2.2 Large Language Models as Agents

\* Chapter 2.5 Hybrid LLM-rule Agent Architectures

\* Chapter 2.6 Action Verification and Safety Boundaries



Connection to LuxLLM-Agent:



LuxLLM-Agent does not use the same self-supervised tool-learning method as Toolformer. However, it shares the broader idea that LLMs can be embedded inside a larger system with external mechanisms.



Suggested sentence:



> Toolformer illustrates that language models can be extended through external tool use. LuxLLM-Agent similarly embeds the LLM inside a larger system, but focuses on game-state summarisation, action verification, fallback, and replay-grounded evaluation.



---



### `park2023generative`



\*\*Paper:\*\* Generative Agents: Interactive Simulacra of Human Behavior

\*\*Authors:\*\* Park et al.

\*\*Use in dissertation:\*\* LLM-based agents can use memory, reflection, and planning in interactive environments.



Suggested use:



\* Chapter 2.2 Large Language Models as Agents

\* Chapter 2.7 Explainability, Traceability, and Decision Provenance



Connection to LuxLLM-Agent:



Generative Agents is useful for discussing LLM-agent architectures with memory and planning. LuxLLM-Agent is narrower and more technical: it focuses on action verification and decision traceability in a game environment.



Suggested sentence:



> Generative Agents shows how LLMs can be integrated into agent architectures involving memory, reflection, and planning. LuxLLM-Agent focuses on a different setting, using structured decision traces and rule-based verification for a competitive game agent.



---



### `li2023camel`



\*\*Paper:\*\* CAMEL: Communicative Agents for 鈥淢ind鈥?Exploration of Large Language Model Society

\*\*Authors:\*\* Li et al.

\*\*Use in dissertation:\*\* LLMs can be used in multi-agent or communicative agent frameworks.



Suggested use:



\* Chapter 2.2 Large Language Models as Agents

\* Chapter 2.5 Hybrid LLM-rule Agent Architectures



Connection to LuxLLM-Agent:



CAMEL is not directly about game control, but it helps show that LLM-agent research includes multi-agent settings. LuxLLM-Agent differs by focusing on a competitive game environment with verified executable actions.



Suggested sentence:



> CAMEL explores communicative LLM-based agents in multi-agent settings. LuxLLM-Agent differs by focusing on a game-control setting where strategic LLM proposals must be verified before execution.



---



## 4.2 LLM Planning, Grounding, and Embodied Agents



### `ahn2022saycan`



\*\*Paper:\*\* Do As I Can, Not As I Say: Grounding Language in Robotic Affordances

\*\*Authors:\*\* Ahn et al.

\*\*Use in dissertation:\*\* LLM outputs need grounding in executable skills or affordances.



Suggested use:



\* Chapter 2.3 LLMs for Planning and Decision Making

\* Chapter 2.5 Hybrid LLM-rule Agent Architectures

\* Chapter 2.6 Action Verification and Safety Boundaries

\* Chapter 4 System Design



Connection to LuxLLM-Agent:



SayCan is one of the most relevant references for this project. It supports the idea that a language model鈥檚 high-level semantic output must be constrained by what the agent can actually do. In LuxLLM-Agent, rule-based verification and action planning play a similar grounding role.



Suggested sentence:



> SayCan argues that high-level language-model knowledge must be grounded in feasible actions. LuxLLM-Agent applies a similar principle in Lux AI Season 3: LLM-generated strategic proposals are checked against game-state constraints before execution.



---



### `wang2023voyager`



\*\*Paper:\*\* Voyager: An Open-Ended Embodied Agent with Large Language Models

\*\*Authors:\*\* Wang et al.

\*\*Use in dissertation:\*\* LLM-powered embodied agents can use environment feedback, skills, and self-verification.



Suggested use:



\* Chapter 2.3 LLMs for Planning and Decision Making

\* Chapter 2.5 Hybrid LLM-rule Agent Architectures

\* Chapter 2.8 Evaluation of LLM-based Agents

\* Chapter 7 Future Work



Connection to LuxLLM-Agent:



Voyager supports the idea that LLM-based agents benefit from executable skills, feedback, and self-verification. LuxLLM-Agent is not a Minecraft lifelong-learning agent, but it shares the need to connect LLM planning to executable behaviour.



Suggested sentence:



> Voyager demonstrates how an LLM-powered embodied agent can combine environment feedback, executable skills, and self-verification. LuxLLM-Agent adopts a narrower but related approach by combining LLM strategy with rule-based verification and replay-grounded inspection.



---



### `yao2023tot`



\*\*Paper:\*\* Tree of Thoughts: Deliberate Problem Solving with Large Language Models

\*\*Authors:\*\* Yao et al.

\*\*Use in dissertation:\*\* LLM planning may benefit from considering multiple reasoning paths and self-evaluation.



Suggested use:



\* Chapter 2.3 LLMs for Planning and Decision Making

\* Chapter 7 Future Work, for multi-candidate planning



Connection to LuxLLM-Agent:



LuxLLM-Agent currently uses structured LLM strategy outputs, not tree search over multiple thoughts. Tree of Thoughts is useful as related work and future work for improving planning quality.



Suggested sentence:



> Tree of Thoughts suggests that LLM problem solving can be improved by exploring and evaluating multiple reasoning paths. A future version of LuxLLM-Agent could use similar multi-candidate planning before selecting a verified strategy.



---



## 4.3 Game AI and Sequential Decision Making



### `mnih2015dqn`



\*\*Paper:\*\* Human-level Control through Deep Reinforcement Learning

\*\*Authors:\*\* Mnih et al.

\*\*Use in dissertation:\*\* Games are established testbeds for sequential decision-making and reinforcement learning.



Suggested use:



\* Chapter 2.4 Game AI and Sequential Decision Making



Connection to LuxLLM-Agent:



DQN supports the broader background that games provide useful environments for agent learning and evaluation.



Suggested sentence:



> Game environments have long served as benchmarks for sequential decision-making research, including deep reinforcement learning systems such as DQN.



---



### `vinyals2019alphastar`



\*\*Paper:\*\* Grandmaster Level in StarCraft II Using Multi-agent Reinforcement Learning

\*\*Authors:\*\* Vinyals et al.

\*\*Use in dissertation:\*\* Complex strategy games require long-horizon planning, partial observability, and multi-agent decision making.



Suggested use:



\* Chapter 2.4 Game AI and Sequential Decision Making

\* Chapter 2.8 Evaluation of LLM-based Agents



Connection to LuxLLM-Agent:



AlphaStar supports the argument that complex games are valuable AI testbeds. Lux AI Season 3 is smaller than StarCraft II but shares some relevant properties, such as multi-agent interaction and strategic decision making.



Suggested sentence:



> Work such as AlphaStar shows that complex strategy games can be important testbeds for multi-agent learning and long-horizon decision making.



---



### `berner2019openai`



\*\*Paper:\*\* Dota 2 with Large Scale Deep Reinforcement Learning

\*\*Authors:\*\* OpenAI et al.

\*\*Use in dissertation:\*\* Large-scale game AI involves long time horizons, imperfect information, and complex action spaces.



Suggested use:



\* Chapter 2.4 Game AI and Sequential Decision Making

\* Chapter 2.8 Evaluation of LLM-based Agents



Connection to LuxLLM-Agent:



OpenAI Five supports the idea that game environments can require complex sequential decision making and evaluation beyond simple action prediction.



Suggested sentence:



> OpenAI Five highlights the challenges of game environments with long time horizons, imperfect information, and complex action spaces. Lux AI Season 3 is smaller, but it still requires repeated decisions under uncertainty.



---



### `browne2012mcts`



\*\*Paper:\*\* A Survey of Monte Carlo Tree Search Methods

\*\*Authors:\*\* Browne et al.

\*\*Use in dissertation:\*\* Traditional game AI and planning/search background.



Suggested use:



\* Chapter 2.4 Game AI and Sequential Decision Making



Connection to LuxLLM-Agent:



MCTS is not used directly in LuxLLM-Agent, but it provides background on planning and search methods in games. It helps position LLM planning as one approach among broader game AI methods.



Suggested sentence:



> Classical game AI has also used search-based planning methods such as Monte Carlo Tree Search. LuxLLM-Agent does not implement MCTS, but it shares the concern of selecting actions under uncertainty.



---



## 4.4 Lux AI Season 3 Sources



### `luxai2024kaggle`



\*\*Source:\*\* Kaggle NeurIPS 2024 Lux AI Season 3 competition page

\*\*Use in dissertation:\*\* Official competition context.



Suggested use:



\* Chapter 2.10 Lux AI Season 3 as an Evaluation Environment

\* Chapter 3 Environment and Task Selection



Connection to LuxLLM-Agent:



This is an official source showing that Lux AI Season 3 is a multi-agent 1v1 AI bot competition.



Suggested sentence:



> Lux AI Season 3 is an official NeurIPS 2024 competition hosted on Kaggle, where participants create AI bots for a novel multi-agent 1v1 game.



---



### `luxdesigns3github`



\*\*Source:\*\* Lux-Design-S3 official GitHub repository

\*\*Use in dissertation:\*\* Official environment and rule source.



Suggested use:



\* Chapter 2.10 Lux AI Season 3 as an Evaluation Environment

\* Chapter 3 Environment and Task Selection

\* Chapter 5 Implementation



Connection to LuxLLM-Agent:



The official repository describes the environment and provides code/specification context.



Suggested sentence:



> The official Lux-Design-S3 repository describes the competition as a 1v1 multi-variable optimisation, resource gathering, and allocation problem.



---



### `luxdesigns3specs`



\*\*Source:\*\* Lux-Design-S3 official specs

\*\*Use in dissertation:\*\* Specific environment details.



Suggested use:



\* Chapter 2.10 Lux AI Season 3 as an Evaluation Environment

\* Chapter 3 Environment and Task Selection



Connection to LuxLLM-Agent:



The specs describe the two-team 2D map and best-of-5 match sequence.



Suggested sentence:



> The official Season 3 specification describes a two-team game on a 2D map, with matches lasting 100 time steps in a best-of-5 match sequence.



---



### `tao2024luxs3`



\*\*Paper:\*\* Lux AI Season 3: Multi-Agent Meta Learning at Scale

\*\*Use in dissertation:\*\* Formal academic reference for Lux AI Season 3.



Suggested use:



\* Chapter 2.10 Lux AI Season 3 as an Evaluation Environment



Connection to LuxLLM-Agent:



This can be used as a formal competition-track citation if included in the final bibliography.



Suggested sentence:



> The Lux AI Season 3 competition has also been described as a setting for evaluating agent adaptation in games with changing parameters.



---



## 5. Section-by-section Citation Placement



## 5.1 Chapter 2.2 Large Language Models as Agents



Recommended citations:



```text

\\citep{yao2023react}

\\citep{shinn2023reflexion}

\\citep{schick2023toolformer}

\\citep{park2023generative}

\\citep{li2023camel}

```



Purpose:



\* show that LLMs are used as interactive agents;

\* support reasoning/action loops;

\* support memory/reflection/planning;

\* support tool use and multi-agent settings.



Suggested paragraph direction:



> Recent work has explored LLMs as components of interactive agent systems, including reasoning-and-acting agents, feedback-based agents, tool-using models, generative social agents, and communicative multi-agent systems.



---



## 5.2 Chapter 2.3 LLMs for Planning and Decision Making



Recommended citations:



```text

\\citep{yao2023react}

\\citep{ahn2022saycan}

\\citep{wang2023voyager}

\\citep{yao2023tot}

```



Purpose:



\* support LLM planning;

\* support action grounding;

\* support environment feedback;

\* support multi-step reasoning or search.



Suggested paragraph direction:



> LLM-based planning can benefit from structured reasoning, but action execution requires grounding in environment-specific constraints.



---



## 5.3 Chapter 2.4 Game AI and Sequential Decision Making



Recommended citations:



```text

\\citep{mnih2015dqn}

\\citep{browne2012mcts}

\\citep{vinyals2019alphastar}

\\citep{berner2019openai}

```



Purpose:



\* position games as AI testbeds;

\* discuss sequential decision making;

\* mention complex strategy games;

\* connect to multi-agent and long-horizon settings.



Suggested paragraph direction:



> Game environments have long been used as AI testbeds, from Atari reinforcement learning to search-based methods and large-scale multi-agent systems in complex strategy games.



---



## 5.4 Chapter 2.5 Hybrid LLM-rule Agent Architectures



Recommended citations:



```text

\\citep{ahn2022saycan}

\\citep{wang2023voyager}

\\citep{schick2023toolformer}

\\citep{yao2023react}

```



Purpose:



\* support systems where LLMs are embedded in larger architectures;

\* support tool/skill/action grounding;

\* justify hybrid rule-based verification.



Suggested paragraph direction:



> Prior work suggests that LLMs are often most useful when embedded in systems with tools, skills, feedback, or external execution constraints.



---



## 5.5 Chapter 2.6 Action Verification and Safety Boundaries



Recommended citations:



```text

\\citep{ahn2022saycan}

\\citep{wang2023voyager}

\\citep{schick2023toolformer}

```



Purpose:



\* justify treating LLM output as proposal;

\* support affordance grounding;

\* support executable skill verification.



Suggested paragraph direction:



> For embodied or environment-interacting agents, model output must be constrained by what the agent can actually execute.



---



## 5.6 Chapter 2.7 Explainability, Traceability, and Decision Provenance



Recommended citations:



```text

\\citep{yao2023react}

\\citep{park2023generative}

\\citep{shinn2023reflexion}

```



Purpose:



\* support reasoning traces;

\* support memory/reflection;

\* connect logs to inspectability.



Suggested paragraph direction:



> Reasoning traces, memory, and reflection mechanisms show that internal agent information can be useful for understanding and improving behaviour.



---



## 5.7 Chapter 2.8 Evaluation of LLM-based Agents



Recommended citations:



```text

\\citep{yao2023react}

\\citep{shinn2023reflexion}

\\citep{wang2023voyager}

\\citep{vinyals2019alphastar}

\\citep{berner2019openai}

```



Purpose:



\* evaluation of agents should include task performance and internal behaviour;

\* complex game agents require more than final score;

\* LLM-agent evaluation can consider failures and environment feedback.



Suggested paragraph direction:



> Evaluating agents requires considering both task outcomes and behavioural evidence, especially when actions are generated by a hybrid system.



---



## 5.8 Chapter 2.10 Lux AI Season 3 as an Evaluation Environment



Recommended citations:



```text

\\citep{luxai2024kaggle}

\\citep{luxdesigns3github}

\\citep{luxdesigns3specs}

\\citep{tao2024luxs3}

```



Purpose:



\* cite official competition page;

\* cite official environment repository;

\* cite specifications;

\* optionally cite formal competition paper.



Suggested paragraph direction:



> Lux AI Season 3 provides a 1v1 multi-agent game environment with partial observability, resource allocation, repeated decisions, and measurable outcomes.



---



## 6. BibTeX Keys to Add Later



The following keys should be added to the bibliography later:



```text

yao2023react

shinn2023reflexion

schick2023toolformer

park2023generative

li2023camel

ahn2022saycan

wang2023voyager

yao2023tot

mnih2015dqn

vinyals2019alphastar

berner2019openai

browne2012mcts

luxai2024kaggle

luxdesigns3github

luxdesigns3specs

tao2024luxs3

```



These should be added to:



```text

paper/custom.bib

```



or to the dissertation bibliography file when the dissertation is assembled.



---



## 7. Recommended Citation Style



If the dissertation uses LaTeX with natbib, use:



```text

\\citep{key}

```



for parenthetical citations, for example:



```text

LLM-based agents have been explored in reasoning-and-acting, tool-use, and memory-based settings \\citep{yao2023react,schick2023toolformer,park2023generative}.

```



Use:



```text

\\citet{key}

```



when the author is part of the sentence, for example:



```text

\\citet{ahn2022saycan} argue that language-model outputs should be grounded in executable affordances.

```



If the dissertation remains in Markdown before final conversion, use citation placeholders like:



```text

(Yao et al., 2023)

(Ahn et al., 2022)

```



and convert them to BibTeX citations later.



---



## 8. Safe Interpretation Rules



When adding citations, avoid overclaiming.



### 8.1 Do not claim LuxLLM-Agent is the same as ReAct



Safe wording:



> LuxLLM-Agent is related to ReAct-style systems because it connects reasoning and acting, but it differs by focusing on rule-based verification and replay-grounded inspection in Lux AI Season 3.



### 8.2 Do not claim LuxLLM-Agent implements SayCan



Safe wording:



> LuxLLM-Agent follows a similar motivation to affordance grounding: high-level language-model outputs should be constrained by executable actions.



### 8.3 Do not claim LuxLLM-Agent is an RL system like AlphaStar or OpenAI Five



Safe wording:



> LuxLLM-Agent is not trained through large-scale reinforcement learning. These systems are cited to position games as challenging sequential decision-making environments.



### 8.4 Do not claim qwen3:32b is universally better than DeepSeek-R1-32B



Safe wording:



> qwen3:32b achieved a higher win rate in the current LuxLLM-Agent evaluation setup, but this result is specific to the current framework, prompt design, environment, and evaluation configuration.



### 8.5 Do not claim the viewer proves strategic optimality



Safe wording:



> The viewer supports inspection of decision provenance and strategy traces, but it does not prove that the decisions are optimal.



---



## 9. Recommended Chapter 2 Revision Strategy



The next step should be to revise Chapter 2 in three passes.



### Pass 1: Add citations without changing too much structure



Add citation placeholders to the current text.



### Pass 2: Strengthen related work comparisons



For each group of papers, explain how LuxLLM-Agent is similar and different.



Example:



```text

Prior work such as SayCan grounds language-model suggestions in executable robot skills. LuxLLM-Agent applies a related principle to a game environment by verifying LLM-generated strategic proposals against Lux AI action constraints.

```



### Pass 3: Add bibliography entries



Add corresponding BibTeX entries to the bibliography file.



---



## 10. Immediate Next Task



The immediate next task is to update:



```text

docs/dissertation/chapter\_2\_background\_related\_work.md

```



The update should:



1\. Add citation placeholders.

2\. Strengthen the comparison between related work and LuxLLM-Agent.

3\. Avoid claiming that LuxLLM-Agent implements methods it only cites as related work.

4\. Keep the chapter readable for a COMP702 dissertation.

5\. Leave full BibTeX work for the next separate step.




