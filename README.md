# Multi-Agent Architecture
The current implementation uses the subgraph paradigm in Langgraph, here the orchestrator itself can call scoring pipeline (data discovery + company scoring) and insight generation agents \\
 
<img width="1134" height="493" alt="image" src="https://github.com/user-attachments/assets/114e68fa-95e2-46dc-8aaa-9df007fef396" />

Data Discovery, Scoring, and insight is a graph in itself. One may also observe the that collect data node entails three subgraphs financials, news, and rumors (again subgraph inside subgraph inside graph)
<img width="1757" height="705" alt="image" src="https://github.com/user-attachments/assets/e86e9d3c-9bf4-4780-9bb6-612f516e03d2" />
