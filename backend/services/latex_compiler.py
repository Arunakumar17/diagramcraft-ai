import os
import subprocess
import shutil
from pathlib import Path
from config import settings

class LatexCompiler:
    def __init__(self):
        self.output_dir = settings.OUTPUT_DIR
        self.temp_dir = settings.TEMP_DIR
    
    def get_template(self, diagram_type: str) -> str:
        """Get the LaTeX template wrapper for the diagram type"""
        template_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                     "templates", f"{diagram_type}.tex")
        
        if os.path.exists(template_path):
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read()
        
        # Default template if specific one doesn't exist
        return self.get_default_template()
    
    def get_default_template(self) -> str:
        """Default LaTeX template"""
        return r"""\documentclass[border=10pt]{standalone}
\usepackage{tikz}
\usetikzlibrary{shapes.geometric, arrows.meta, positioning, automata, mindmap, trees}
\usepackage{tikz-uml}
\usepackage{pgfgantt}

\begin{document}
{TIKZ_CODE}
\end{document}
"""
    
    def compile_latex(self, latex_code: str, diagram_id: str, diagram_type: str) -> str:
        """Compile LaTeX code to PDF"""
        try:
            # Get template
            template = self.get_template(diagram_type)
            
            # Insert TikZ code into template
            full_latex = template.replace("{TIKZ_CODE}", latex_code)
            
            # Create unique filename
            tex_filename = f"{diagram_id}.tex"
            pdf_filename = f"{diagram_id}.pdf"
            
            tex_path = os.path.join(self.temp_dir, tex_filename)
            pdf_path = os.path.join(self.output_dir, pdf_filename)
            
            # Write LaTeX file
            with open(tex_path, 'w', encoding='utf-8') as f:
                f.write(full_latex)
            
            # Check if pdflatex is available
            if not shutil.which('pdflatex'):
                raise Exception("pdflatex not found. Please install TeX Live or MiKTeX.")
            
            # Compile with pdflatex
            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', '-output-directory', self.temp_dir, tex_path],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Check if PDF was created
            temp_pdf = os.path.join(self.temp_dir, pdf_filename)
            if not os.path.exists(temp_pdf):
                # Try to extract error from log
                log_file = os.path.join(self.temp_dir, f"{diagram_id}.log")
                error_msg = "LaTeX compilation failed."
                if os.path.exists(log_file):
                    with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                        log_content = f.read()
                        if '! ' in log_content:
                            # Extract error lines
                            error_lines = [line for line in log_content.split('\n') if line.startswith('!')]
                            if error_lines:
                                error_msg = ' '.join(error_lines[:3])
                raise Exception(f"LaTeX compilation failed: {error_msg}")
            
            # Move PDF to output directory
            shutil.move(temp_pdf, pdf_path)
            
            # Clean up auxiliary files
            for ext in ['.aux', '.log', '.tex']:
                aux_file = os.path.join(self.temp_dir, f"{diagram_id}{ext}")
                if os.path.exists(aux_file):
                    os.remove(aux_file)
            
            return pdf_path
            
        except subprocess.TimeoutExpired:
            raise Exception("LaTeX compilation timed out")
        except Exception as e:
            raise Exception(f"Error compiling LaTeX: {str(e)}")

latex_compiler = LatexCompiler()
