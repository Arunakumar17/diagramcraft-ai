import os
from pdf2image import convert_from_path
from PIL import Image
from config import settings

class ImageConverter:
    def __init__(self):
        self.output_dir = settings.OUTPUT_DIR
    
    def pdf_to_png(self, pdf_path: str, diagram_id: str) -> str:
        """Convert PDF to PNG image"""
        try:
            # Convert PDF to images (one page, high DPI for quality)
            images = convert_from_path(
                pdf_path,
                dpi=300,
                first_page=1,
                last_page=1
            )
            
            if not images:
                raise Exception("No images generated from PDF")
            
            # Save as PNG
            png_filename = f"{diagram_id}.png"
            png_path = os.path.join(self.output_dir, png_filename)
            
            # Get first (and only) page
            img = images[0]
            
            # Optimize and save
            img.save(png_path, 'PNG', optimize=True)
            
            return png_path
            
        except Exception as e:
            raise Exception(f"Error converting PDF to PNG: {str(e)}")
    
    def pdf_to_svg(self, pdf_path: str, diagram_id: str) -> str:
        """Convert PDF to SVG (optional, requires pdf2svg)"""
        try:
            import subprocess
            
            svg_filename = f"{diagram_id}.svg"
            svg_path = os.path.join(self.output_dir, svg_filename)
            
            # Try using pdf2svg if available
            result = subprocess.run(
                ['pdf2svg', pdf_path, svg_path],
                capture_output=True,
                timeout=10
            )
            
            if result.returncode == 0 and os.path.exists(svg_path):
                return svg_path
            else:
                # SVG conversion not available
                return None
                
        except (FileNotFoundError, subprocess.TimeoutExpired):
            # pdf2svg not installed, skip SVG generation
            return None
        except Exception as e:
            print(f"SVG conversion failed: {str(e)}")
            return None

image_converter = ImageConverter()
