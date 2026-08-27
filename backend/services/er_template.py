from typing import Dict, List
import math

class ERDiagramGenerator:
    """Generate perfect ER diagrams using predefined templates with smart layouts"""
    
    def generate_perfect_er_diagram(self, entities: List[Dict], relationships: List[Dict]) -> str:
        """
        Generate a PERFECT ER diagram - SIMPLE and CLEAN
        entities: [{"name": "Student", "attributes": ["student_id", "name", "email"], "primary_key": "student_id"}]
        relationships: [{"name": "Enrolls", "entity1": "Student", "entity2": "Course", "card1": "M", "card2": "N"}]
        """
        
        # LIMIT to 2 entities for maximum clarity
        num_entities = min(len(entities), 2)
        entities = entities[:2]
        relationships = [r for r in relationships if r["entity1"] in [e["name"] for e in entities] and r["entity2"] in [e["name"] for e in entities]][:1]
        
        # Simple horizontal layout
        layout = self._horizontal_layout(num_entities)
        
        # MAXIMUM sizes for perfect readability
        tikz_code = """\\begin{tikzpicture}[
  entity/.style={rectangle, draw, line width=1.5pt, minimum width=6cm, minimum height=2.5cm, font=\\LARGE\\bfseries, align=center},
  relationship/.style={diamond, draw, line width=1.5pt, minimum width=5cm, minimum height=5cm, font=\\Large\\bfseries, inner sep=3pt, aspect=1, align=center},
  attribute/.style={ellipse, draw, line width=1.2pt, minimum width=4cm, minimum height=1.8cm, font=\\Large, align=center}
]

"""
        
        # Generate entities with attributes
        for i, entity in enumerate(entities):
            entity_name = entity["name"]
            attributes = entity["attributes"]  # Show ALL attributes user specified
            primary_key = entity.get("primary_key", None)  # Primary key is optional
            
            x_pos, y_pos = layout[i]
            
            tikz_code += f"% ===== {entity_name} Entity =====\n"
            tikz_code += f"\\node[entity] ({entity_name.lower()}) at ({x_pos},{y_pos}) {{{entity_name}}};\n\n"
            
            # Attributes ALWAYS ABOVE (positive offset from y_pos)
            num_attrs = len(attributes)
            attr_height = 6.5  # ALWAYS positive - above entity
            
            for j, attr in enumerate(attributes):
                # Wide horizontal spacing based on attribute count
                if num_attrs == 1:
                    x_offset = 0
                elif num_attrs == 2:
                    x_offset = (j - 0.5) * 5.5
                elif num_attrs == 3:
                    x_offset = (j - 1) * 5.0
                else:  # 4+ attributes
                    x_offset = (j - (num_attrs - 1) / 2) * 4.5
                
                attr_x = x_pos + x_offset
                # CRITICAL: Always ABOVE by using absolute positive offset
                attr_y = y_pos + attr_height  # ALWAYS positive = always above
                
                # Format attribute - underline only if it's the primary key
                attr_clean = attr.replace('_', '\\_')
                attr_label = f"\\underline{{{attr_clean}}}" if (primary_key and attr == primary_key) else attr_clean
                
                node_id = f"{entity_name.lower()}_attr{j}"
                tikz_code += f"\\node[attribute] ({node_id}) at ({attr_x},{attr_y}) {{{attr_label}}};\n"
                tikz_code += f"\\draw[line width=1.2pt] ({entity_name.lower()}) -- ({node_id});\n"

            
            tikz_code += "\n"
        
        # Generate relationships with SMART positioning
        for idx, rel in enumerate(relationships):
            rel_name = rel["name"]
            entity1 = rel["entity1"]
            entity2 = rel["entity2"]
            card1 = rel.get("card1", "M")
            card2 = rel.get("card2", "N")
            
            # Find entity positions
            idx1 = next((i for i, e in enumerate(entities) if e["name"] == entity1), 0)
            idx2 = next((i for i, e in enumerate(entities) if e["name"] == entity2), 1)
            
            x1, y1 = layout[idx1]
            x2, y2 = layout[idx2]
            
            # Position relationship diamond
            rel_x = (x1 + x2) / 2
            rel_y = (y1 + y2) / 2
            
            tikz_code += f"% ===== {rel_name} Relationship =====\n"
            tikz_code += f"\\node[relationship] (rel{idx}) at ({rel_x},{rel_y}) {{{rel_name}}};\n"
            
            # Draw connections with clear labels
            tikz_code += f"\\draw[line width=1.5pt] ({entity1.lower()}) -- (rel{idx}) node[midway, fill=white, inner sep=2pt, font=\\Large\\bfseries] {{{card1}}};\n"
            tikz_code += f"\\draw[line width=1.5pt] (rel{idx}) -- ({entity2.lower()}) node[midway, fill=white, inner sep=2pt, font=\\Large\\bfseries] {{{card2}}};\n\n"
        
        tikz_code += "\\end{tikzpicture}"
        return tikz_code
    
    def _horizontal_layout(self, num_entities: int) -> List[tuple]:
        """Horizontal layout with MASSIVE spacing"""
        spacing = 24  # Even larger
        return [(i * spacing, 0) for i in range(num_entities)]
    
    def _triangle_layout(self) -> List[tuple]:
        """Triangle layout for 3 entities"""
        return [
            (0, 0),
            (24, 0),
            (12, 18)
        ]
    
    def _grid_layout(self, num_entities: int) -> List[tuple]:
        """Grid layout with MASSIVE spacing"""
        positions = []
        cols = 2
        rows = math.ceil(num_entities / cols)
        
        x_spacing = 26  # MASSIVE horizontal
        y_spacing = 30  # MASSIVE vertical
        
        for i in range(num_entities):
            row = i // cols
            col = i % cols
            x = col * x_spacing
            y = -row * y_spacing
            positions.append((x, y))
        
        return positions


er_generator = ERDiagramGenerator()
