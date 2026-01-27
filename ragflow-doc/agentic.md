**Yes, let's deconstruct the "Equity Investment Research" workflow on RAGFlow.io.** This is a great example of **agentic AI in practice** — where AI agents go beyond simple Q&A to autonomously plan, coordinate, use tools, retrieve data, and collaborate to complete a complex goal (here, producing a professional-grade investment report).

RAGFlow is an open-source RAG (Retrieval-Augmented Generation) engine that extends into **agentic workflows**. It lets you build visual, no-code graphs of nodes (e.g., agents, tools, conditions, code snippets) that orchestrate LLMs and external resources. The system is **graph-based**: nodes connect in sequences, branches, or loops, with state (like a stock ticker) passed along. Agents are LLM instances with custom roles, system prompts, tools, and output constraints — they "act" by reasoning, calling tools, and producing structured outputs.

This workflow demonstrates **multi-agent orchestration** with **autonomous planning** and **tool use**. It's not one big LLM prompt; instead, specialized agents handle subtasks, hand off results, and assemble the final output. From the detailed case study (a blog post on implementing a deep-dive company research agent), here's how it's set up and interacts.

### High-Level Structure
The workflow runs in RAGFlow's visual canvas (drag-and-drop nodes). It starts with a user query (e.g., "Analyze Apple's financials" or "What's the outlook for AAPL?") and ends with a complete report including:
- Financial metrics (tables from APIs)
- Qualitative insights (from internal knowledge base + external sources)
- Synthesized analysis (summary, overview, performance, trends, recommendation, citations)

Key flow:
1. **Input → Ticker Extraction**  
2. **Conditional check** (valid ticker?)  
3. **Data collection** (financials + research)  
4. **Synthesis & Report Generation**  
5. **Output**

Agents are modular nodes; they can call tools (e.g., web search, APIs), retrieve from knowledge bases, or delegate to sub-agents. The system maintains context (e.g., the ticker) across nodes for seamless handoffs.

### The Main Agents & How They're Set Up
RAGFlow agents are configured with:
- **Role/system prompt** — Defines personality, expertise, rules (e.g., "Act as a senior investment banker", "Output only JSON", "Never fabricate data").
- **Tools** — External functions/APIs they can call (via function calling).
- **Knowledge bases** — RAG retrieval from uploaded/parsed documents.
- **Output constraints** — Strict formats to make handoffs reliable.

Here are the key agents in this workflow:

1. **Stock Code Extraction Agent** (or "Search Agent")  
   - **Role**: Turn natural language into a standard ticker (e.g., "Apple" → "AAPL").  
   - **Setup**: Strict prompt — output only the ticker or "Not Found" (no extra text). Uses **Tavily Search** tool for ambiguous cases (e.g., if company name is unclear).  
   - **Why agentic?** It reasons autonomously: if the query is vague, it calls a search tool to resolve → demonstrates **tool use** and **planning** (decide if/when to search).

2. **Information Extraction Agent** (Coordinator/Planner Agent)  
   - **Role**: Gather qualitative insights once ticker is known.  
   - **Setup**: Acts as a **planner** — its prompt tells it to delegate subtasks:  
     - Call **AlphaVantage API** (via MCP tool) for earnings transcripts, key insights.  
     - Trigger **Internal Research Report Retrieval Agent** (sub-agent) for internal docs.  
   - Outputs structured sections (e.g., "alphavantage": raw transcript; "internal": full reports).  
   - **Agentic aspect**: This is where **multi-agent delegation** shines — it autonomously plans steps ("I need external + internal → call these"), calls tools/agents, aggregates results.

3. **Internal Research Report Retrieval Agent** (Sub-agent)  
   - **Role**: Pure retrieval from RAGFlow's internal knowledge base.  
   - **Setup**: Uses **Retrieval Tool** on a dataset (e.g., Hugging Face "company_financial_research_agent" — parsed research reports with structure preserved: abstracts, forecasts, risks). Supports aliases, merges multiple reports chronologically.  
   - **Agentic?** Less reasoning, more execution — but fits into the multi-agent pattern as a specialized worker.

4. **Research Report Generation Agent** (or "Report Agent"/"Analyze Agent")  
   - **Role**: Senior analyst — synthesize everything into a professional report.  
   - **Setup**: Detailed role prompt (experienced IB analyst). Strict structure:  
     - Sections: 1. Summary, 2. Company Overview, 3. Recent Financial Performance, 4. Industry Trends, 5. Investment Recommendation, 6. Appendix/References.  
     - Rules: Preserve conflicting viewpoints (don't merge), use tables for comparisons (e.g., Buy/Hold ratings from sources), cite everything (source, date, institution).  
     - Input: Formatted financial table + extracted research texts.  
   - **Agentic aspect**: Heavy reasoning + synthesis. It analyzes, compares sources, draws conclusions — all grounded in provided data (no hallucination allowed).

Supporting nodes (not agents but crucial):
- **Yahoo Finance Tool** — Fetches balance sheet/income data.
- **Code Node** (Python) — Formats raw API data into clean Markdown tables.
- **Conditional Node** — Branches (e.g., invalid ticker → error message).

### How Agents Interact (Orchestration in Practice)
- **Graph-based flow**: Nodes connect sequentially/with branches. State passes automatically (e.g., ticker from extraction → all downstream nodes).
- **Handoffs**: Structured outputs (JSON/text) ensure clean transfer — e.g., extraction agent outputs "AAPL" → extraction agent uses it to call APIs → generation agent gets the bundle.
- **Autonomy & Planning**: 
  - Agents don't need human input mid-flow.
  - Planning happens via prompts (e.g., "Delegate to X tool if needed") or sub-agents.
  - Conditional nodes add dynamic routing (if-then logic).
- **Collaboration**: Multi-agent = division of labor. No single LLM does everything; specialized agents reduce errors and improve quality (e.g., retrieval agent handles RAG perfectly, generation agent focuses on analysis).
- **Tool integration**: Agents call tools via function calling (LLM decides when/how based on prompt). Tools return data → agent incorporates it.
- **End-to-end run**: Fully autonomous — query in → report out in minutes. Error handling prevents crashes.

### Why This Shows Agentic AI Working in Practice
- **Beyond chat**: Classic LLM = one-shot response. Agentic = goal-oriented system that breaks tasks, uses tools, iterates/coordinates.
- **Reliability**: Strict prompts + structured outputs + grounding (RAG + APIs) minimize hallucinations.
- **Scalability**: Add agents/tools easily (e.g., more APIs, sentiment analysis agent).
- **Real-world application**: Automates tedious parts of equity research (data gathering, formatting) so humans focus on judgment. It's not replacing analysts — it's augmenting them with a "research team" of AI specialists.

If you have access to RAGFlow (self-hosted or cloud), you can import/recreate this workflow via their canvas, tweak prompts/tools, or even see the exact node graph in their demo/examples. The blog post (linked in sources) has the most detailed breakdown if you want to replicate it.

Let me know if you'd like help adapting this to your own setup (e.g., different APIs or domain)!
