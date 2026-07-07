import streamlit as st
from components import render_session_header, render_explanation, render_technologies_used, render_key_concepts, render_what_you_built

render_session_header(5, "CoWork", "11:00 - 11:15 AM", "15 min", "Collaborative AI analysis with CoWork")

render_technologies_used([
    {"name": "Snowflake CoWork", "description": "An AI-powered collaborative workspace inside Snowsight where you can analyze data, generate insights, and share findings with your team — all through natural language conversation.", "icon": "group"},
    {"name": "Data Analysis", "description": "CoWork can query your Snowflake data, generate visualizations, and provide insights without writing SQL. It understands your semantic views and table structures.", "icon": "analytics"},
    {"name": "Sharing & Collaboration", "description": "CoWork sessions can be shared with team members, creating a collaborative space for data exploration and decision-making.", "icon": "share"},
])

st.markdown("---")

st.markdown("#### :material/open_in_new: Open CoWork")
with st.container(border=True):
    st.markdown("""
In Snowsight, click **CoWork** in the left navigation panel. Start a new conversation.

CoWork provides a chat-based interface that can query your Snowflake data, create charts, and generate insights — no SQL required. It discovers your tables in `HIIVE_AI.MARKETPLACE_OPS` automatically.

Paste each question below into CoWork one at a time and observe how it generates queries and visualizations.
""")

st.space("small")

st.markdown("#### :material/chat: Questions to ask CoWork")
st.caption("Copy and paste each question into CoWork individually. They build on each other in sequence.")

questions = [
    ("1. Marketplace Overview", "Show me an overview of HIIVE marketplace activity — total trades executed, top company by volume, and average time to settlement"),
    ("2. Sector Trends", "Create a visualization showing trade volume by company sector and month. Are there seasonal patterns?"),
    ("3. Compliance Concerns", "What are the top compliance concerns based on review data? Show breakdown by type and risk score"),
    ("4. User Engagement", "Compare platform engagement metrics across user types (buyers vs sellers). Who is more active?"),
    ("5. Correlation Analysis", "Based on compliance reviews and trading patterns, are there companies that have both high volume AND more compliance flags?"),
    ("6. Executive Summary", "Generate a summary report of marketplace health that I could share with the executive team. Include key metrics, trends, and areas of concern."),
    ("7. Recommendations", "What would you recommend as the top 3 operational improvements based on all the data?"),
]

for title, question in questions:
    with st.container(border=True):
        st.markdown(f"**{title}**")
        st.code(question, language="text", wrap_lines=True)

st.space("small")

render_explanation("How CoWork works", """
**CoWork** is Snowflake's collaborative AI workspace. Unlike Cortex Code (which executes prompts as SQL/Python), CoWork is designed for **interactive data exploration and team collaboration**.

**How CoWork differs from Cortex Code**:
- **Cortex Code**: Developer tool — executes SQL, creates objects, builds infrastructure
- **CoWork**: Analyst tool — explores data, generates visualizations, shares insights

**What CoWork does with these questions**:
1. Queries your tables automatically (it discovers HIIVE_AI.MARKETPLACE_OPS tables)
2. Generates appropriate SQL behind the scenes
3. Creates visualizations (charts, tables) inline
4. Provides natural language explanations of the results

**Key capabilities**:
- Understands your semantic views and table relationships
- Creates charts and visualizations automatically
- Supports follow-up questions in context
- Can be shared with team members for collaborative analysis

**When to use CoWork vs. Cortex Code vs. Cortex Agent**:
| Tool | Best for |
|------|----------|
| Cortex Code | Building infrastructure, creating objects, writing SQL |
| CoWork | Exploring data, generating insights, team collaboration |
| Cortex Agent | End-user Q&A interface (deployed as a product) |
""")


render_key_concepts([
    {"term": "CoWork", "definition": "Snowflake's collaborative AI workspace for data exploration. Provides a conversational interface that queries data, creates visualizations, and generates insights. Designed for business analysts and team collaboration."},
    {"term": "Collaborative Intelligence", "definition": "The pattern where AI assists a team in making decisions together. CoWork sessions can be shared, allowing multiple people to ask questions, build on each other's analysis, and reach conclusions collectively."},
    {"term": "Context Maintenance", "definition": "CoWork maintains conversation history so follow-up questions build on previous analysis. Ask 'Show me trade volume by sector' then 'Now filter to just Q4' — it remembers the context."},
])

render_what_you_built([
    "Explored HIIVE marketplace data through conversational AI",
    "Generated visualizations of trading patterns and compliance data",
    "Created an executive summary of marketplace health",
    "Demonstrated the CoWork collaborative analysis pattern",
])
