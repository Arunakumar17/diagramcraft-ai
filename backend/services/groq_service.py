import os
from groq import Groq
from config import settings

class GroqService:
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = "qwen/qwen3.8-27b"  # Updated to current model
    
    def get_system_prompt(self, diagram_type: str) -> str:
        """Get specialized system prompt for each diagram type"""
        prompts = {
            "er_diagram": """You are an expert at analyzing database requirements and extracting ER diagram components.

OUTPUT FORMAT: Return ONLY a JSON object (no markdown, no explanations) with this exact structure:
{
  "entities": [
    {"name": "EntityName", "attributes": ["attr1", "attr2", "attr3"]}
  ],
  "relationships": [
    {"name": "RelationshipName", "entity1": "Entity1", "entity2": "Entity2", "card1": "M", "card2": "N"}
  ]
}

CRITICAL RULES:
1. Extract ONLY the entities mentioned by the user
2. Entity names: Singular, PascalCase (e.g., "Student", "Course", "Lecturer")
3. Attributes: Extract EXACTLY the attributes the user specifies - NO MORE, NO LESS
   - DO NOT add primary keys (like student_id, course_id) unless the user explicitly mentions them
   - Use the EXACT attribute names the user provides
   - Convert to lowercase_with_underscores format (e.g., "first name" -> "first_name")
4. Extract ONLY the relationships the user describes
5. Relationship name: Simple verb describing the relationship (e.g., "Enrolls", "Teaches", "Manages", "Maintains", "Has")
   - Use ONLY single words: Enrolls, Teaches, Owns, Has, Manages, Maintains, Treats, Writes, Reads, Buys, Sells
6. Cardinality: Use "1" (exactly one), "M" (many), or "N" (many)
   - "Each X has exactly one Y" = X side gets "1", Y side gets "1" (1:1)
   - "Each X has many Y" = X side gets "1", Y side gets "M" (1:M)
   - "Many X to many Y" = Both sides get "M" and "N" (M:N)

EXAMPLE 1:
User: "A Student has first_name, last_name, and phone_number. A Lecturer has first_name, last_name, and email. Each student is maintained by exactly one lecturer."
Response:
{
  "entities": [
    {"name": "Student", "attributes": ["first_name", "last_name", "phone_number"]},
    {"name": "Lecturer", "attributes": ["first_name", "last_name", "email"]}
  ],
  "relationships": [
    {"name": "Maintains", "entity1": "Lecturer", "entity2": "Student", "card1": "1", "card2": "M"}
  ]
}

EXAMPLE 2:
User: "Doctors treat patients. Doctors have name, specialty. Patients have name, age."
Response:
{
  "entities": [
    {"name": "Doctor", "attributes": ["name", "specialty"]},
    {"name": "Patient", "attributes": ["name", "age"]}
  ],
  "relationships": [
    {"name": "Treats", "entity1": "Doctor", "entity2": "Patient", "card1": "1", "card2": "M"}
  ]
}

Return ONLY valid JSON. NO other text.""",

            "flowchart": """You are an expert in creating clean, readable flowcharts using LaTeX TikZ.

CRITICAL RULES FOR NO OVERLAPS:
1. USE PRE-DEFINED STYLES: 
   - `startstop` (Ellipse, Red)
   - `process` (Rectangle, Blue)
   - `decision` (Diamond, Green)
   - `io` (Trapezium, Orange)
   - Use `arrow` style for connections: \\draw[arrow] ...
2. STRICT POSITIONING - NO OVERLAPS PERMITTED: 
   - **Vertical Spacing**: `node distance=3cm` (MUST be at least 3cm).
   - **Horizontal Spacing**: For side branches (e.g., 'No' path), you MUST use `right=5cm of node` (minimum 5cm).
   - **Grid Strategy**: Imagine a wide grid. Do not squeeze nodes.
3. PATH ROUTING:
   - **Orthogonal Only**: Use `|-` (vertical then horizontal) or `-|` (horizontal then vertical).
   - **NO DIAGONALS**: Never connect non-adjacent nodes with a straight line `--`. It cuts through things.
   - Example: `\\draw[arrow] (nodeA) -| (nodeB);` to go around corner.
4. DECISION LOGIC:
   - "Yes" -> `below=of decision`
   - "No" -> `right=5cm of decision` (Force it wide!)

EXAMPLE OUTPUT STRUCTURE:
\\begin{tikzpicture}[node distance=3cm, auto]
  \\node[startstop] (start) {Start};
  \\node[process, below=of start] (step1) {Step 1};
  \\node[decision, below=of step1] (dec) {Is it valid?};
  
  % Branch 1 (Yes) - Down
  \\node[process, below=of dec] (yes_proc) {Process Yes};
  
  % Branch 2 (No) - FAR RIGHT
  \\node[process, right=5cm of dec] (no_proc) {Process No};
  \\node[process, below=of no_proc] (no_end) {End No};
  
  % Connections with orthogonal paths
  \\draw[arrow] (start) -- (step1);
  \\draw[arrow] (step1) -- (dec);
  \\draw[arrow] (dec) -- node[right] {Yes} (yes_proc);
  \\draw[arrow] (dec) -- node[above] {No} (no_proc); % Straight right is OK for immediate neighbor
  \\draw[arrow] (no_proc) -- (no_end);
  \\draw[arrow] (no_end) |- (yes_proc); % Orthogonal return
\\end{tikzpicture}

Return ONLY valid TikZ code. NO explanations.""",

            "class_diagram": """You are an expert in creating UML Class diagrams using basic LaTeX TikZ.

CRITICAL: Use ONLY basic TikZ - NO tikz-uml package!

STRUCTURE - Each class as a rectangle with tabular inside:
\\node[draw, rectangle, minimum width=5cm, minimum height=3cm, font=\\large] (classname) at (x,y) {
  \\begin{tabular}{l}
    \\textbf{ClassName} \\\\
    \\hline
    - attribute: type \\\\
    \\hline
    + method(): type \\\\
  \\end{tabular}
};

LAYOUT: 
- Maximum 2 classes, horizontal layout with 12cm spacing
- Use \\draw[-{Triangle[open]}, line width=1pt] for inheritance
- Use \\draw[line width=1pt] for associations

EXAMPLE:
\\begin{tikzpicture}
\\node[draw, rectangle, minimum width=5cm, minimum height=3cm, font=\\large] (person) at (0,0) {
  \\begin{tabular}{l}
    \\textbf{Person} \\\\
    \\hline
    - id: int \\\\
    - name: string \\\\
    \\hline
    + getName(): string \\\\
  \\end{tabular}
};
\\end{tikzpicture}

Return ONLY TikZ code. NO explanations.""",

            "state_diagram": """You are an expert in creating State diagrams using LaTeX TikZ automata.
Generate ONLY valid TikZ code for state machines.
- Use \\node[state] for states
- Use \\node[state, initial] for initial state
- Use \\node[state, accepting] for final states
- Use \\path with arrows and labels for transitions
Return ONLY the TikZ diagram code inside \\begin{tikzpicture} ... \\end{tikzpicture}. No explanations.""",

            "gantt_chart": """You are an expert in creating Gantt charts using LaTeX pgfgantt.

CRITICAL SYNTAX:
1. Start with \\begin{ganttchart}[options]{start}{end}
2. ALWAYS provide start/end arguments (e.g., {1}{12})
3. Use \\\\ at end of EVERY line (title, bar, group)
4. Use \\gantttitle{Label}{width}
5. Use \\ganttbar{Task}{start}{end}
6. Use \\ganttlink{elem1}{elem2}

EXAMPLE:
\\begin{ganttchart}[
    vgrid, hgrid,
    y unit title=0.5cm,
    y unit chart=0.6cm,
    x unit=0.8cm
]{1}{10}
  \\gantttitle{Project Timeline}{10} \\\\
  \\gantttitlelist{1,...,10}{1} \\\\
  \\ganttgroup{Phase 1}{1}{5} \\\\
  \\ganttbar{Task A}{1}{3} \\\\
  \\ganttbar{Task B}{3}{5} \\\\
  \\ganttmilestone{Milestone}{5}
\\end{ganttchart}

Return ONLY valid LaTeX code. NO explanation.""",

            "mindmap": """You are an expert in creating Mind maps using LaTeX TikZ mindmap library.
Generate ONLY valid TikZ mindmap code.

CRITICAL STYLING RULES:
1. Document Setup: \\begin{tikzpicture}[mindmap, grow cyclic, every node/.style={concept, execute at begin node=\\hskip0pt}, concept color=black!90, text=white]
2. Root Node: Use \\node[concept, concept color=blue!80] {Root}
3. Children: Use child { node[concept] {Child} }
4. Styling:
   - Root concept color: usually blue!80 or black!80
   - Level 1 children: Use different colors (e.g., green!60, violet!60, red!60, orange!60, teal!60) via [concept color=...]
   - Level 2 children: Inherit color or use lighter shade (automatically handled by mindmap)
5. Spacing:
   - Use 'level 1/.style={level distance=5cm, sibling angle=...}'
   - Adjust angles to prevent overlap. Spread children evenly (360/N degrees).
   - Use 'text width' to wrap text (e.g., text width=3cm) if text is long.
   - For large trees, increase level distance.

EXAMPLE:
\\begin{tikzpicture}[mindmap, grow cyclic, every node/.style={concept, execute at begin node=\\hskip0pt}, concept color=black!90, text=white]
  \\node [concept, concept color=blue!80] {Machine Learning}
    child [concept color=green!60] { node [concept] {Supervised} 
      child { node [concept] {Regression} }
      child { node [concept] {Classification} }
    }
    child [concept color=orange!60] { node [concept] {Unsupervised}
      child { node [concept] {Clustering} }
    };
\\end{tikzpicture}

Return ONLY the TikZ diagram code inside \\begin{tikzpicture} ... \\end{tikzpicture}. No explanations."""
        }
        return prompts.get(diagram_type, prompts["flowchart"])
    
    def generate_latex_code(self, diagram_type: str, user_prompt: str) -> str:
        """Generate LaTeX TikZ code from user prompt using Groq"""
        try:
            # Special handling for ER diagrams - use template-based approach
            if diagram_type == "er_diagram":
                return self._generate_er_diagram_perfect(user_prompt)
            
            system_prompt = self.get_system_prompt(diagram_type)
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Create a clean, well-spaced, and readable {diagram_type.replace('_', ' ')} for: {user_prompt}\n\nIMPORTANT: Ensure NO overlapping elements, use proper positioning, and maintain clean layouts."}
            ]
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3,  # Very low for maximum consistency
                max_tokens=4000  # Enough for complex diagrams
            )
            
            latex_code = response.choices[0].message.content.strip()
            
            # Clean up the response - extract only TikZ code
            if "\\begin{tikzpicture}" in latex_code:
                start = latex_code.find("\\begin{tikzpicture}")
                end = latex_code.find("\\end{tikzpicture}") + len("\\end{tikzpicture}")
                latex_code = latex_code[start:end]
            elif "\\begin{ganttchart}" in latex_code:
                start = latex_code.find("\\begin{ganttchart}")
                end = latex_code.find("\\end{ganttchart}") + len("\\end{ganttchart}")
                latex_code = latex_code[start:end]
            
            return latex_code
            
        except Exception as e:
            raise Exception(f"Error generating LaTeX code: {str(e)}")
    
    def _generate_er_diagram_perfect(self, user_prompt: str) -> str:
        """Generate perfect ER diagram using template-based approach"""
        import json
        from services.er_template import er_generator
        
        # Step 1: Extract structured data from prompt
        system_prompt = self.get_system_prompt("er_diagram")
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.2,
            max_tokens=2000
        )
        
        json_response = response.choices[0].message.content.strip()
        
        # Clean JSON response
        if "```json" in json_response:
            json_response = json_response.split("```json")[1].split("```")[0].strip()
        elif "```" in json_response:
            json_response = json_response.split("```")[1].split("```")[0].strip()
        
        # Parse JSON
        try:
            data = json.loads(json_response)
            entities = data.get("entities", [])
            relationships = data.get("relationships", [])
            
            # Step 2: Generate perfect diagram from template
            latex_code = er_generator.generate_perfect_er_diagram(entities, relationships)
            return latex_code
            
        except json.JSONDecodeError as e:
            # Fallback: if JSON parsing fails, return error
            raise Exception(f"Failed to parse ER diagram structure: {str(e)}. Response was: {json_response}")

groq_service = GroqService()
