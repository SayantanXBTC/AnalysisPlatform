"""
Strategic PDF Generator - Creates professional PDF reports from strategic analysis
Filename based on the original prompt
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import re
import os


class StrategicPDFGenerator:
    """Generate professional PDF reports from strategic analysis results"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Only add styles if they don't exist
        if 'CustomTitle' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='CustomTitle',
                parent=self.styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#1e40af'),
                spaceAfter=30,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            ))
        
        if 'SectionHeader' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='SectionHeader',
                parent=self.styles['Heading2'],
                fontSize=16,
                textColor=colors.HexColor('#2563eb'),
                spaceAfter=12,
                spaceBefore=20,
                fontName='Helvetica-Bold'
            ))
        
        if 'Classification' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='Classification',
                parent=self.styles['Normal'],
                fontSize=12,
                textColor=colors.HexColor('#059669'),
                fontName='Helvetica-Bold'
            ))
        
        # Use unique name to avoid conflicts
        if 'CustomBodyText' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='CustomBodyText',
                parent=self.styles['Normal'],
                fontSize=11,
                leading=16,
                alignment=TA_JUSTIFY,
                spaceAfter=12
            ))
    
    def generate_pdf(self, prompt: str, results: dict, output_dir: str = "reports") -> str:
        """
        Generate PDF report from strategic analysis results
        
        Args:
            prompt: Original strategic prompt
            results: Analysis results dictionary
            output_dir: Directory to save PDF
        
        Returns:
            Path to generated PDF file
        """
        try:
            # Ensure output directory exists
            os.makedirs(output_dir, exist_ok=True)
            print(f"[PDF Generator] Output directory created/verified: {output_dir}")
            
            # Generate filename from prompt
            filename = self._generate_filename(prompt)
            filepath = os.path.join(output_dir, filename)
            print(f"[PDF Generator] Target filepath: {filepath}")
            
            # Create PDF document
            doc = SimpleDocTemplate(
                filepath,
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )
            
            # Build content
            story = []
            
            # Title page
            print("[PDF Generator] Building title page...")
            story.extend(self._build_title_page(prompt, results))
            story.append(PageBreak())
            
            # Executive summary
            print("[PDF Generator] Building executive summary...")
            story.extend(self._build_executive_summary(results))
            story.append(PageBreak())
            
            # Strategic classifications
            print("[PDF Generator] Building classifications...")
            story.extend(self._build_classifications(results))
            
            # Strategic recommendation
            if results.get("strategic_recommendation"):
                print("[PDF Generator] Building recommendation...")
                story.extend(self._build_recommendation(results["strategic_recommendation"]))
            
            # Key insights
            if results.get("key_insights"):
                print("[PDF Generator] Building key insights...")
                story.extend(self._build_key_insights(results["key_insights"]))
            
            # Risks and unknowns
            if results.get("risks_and_unknowns"):
                print("[PDF Generator] Building risks...")
                story.extend(self._build_risks(results["risks_and_unknowns"]))
            
            # Next steps
            if results.get("suggested_next_steps"):
                print("[PDF Generator] Building next steps...")
                story.extend(self._build_next_steps(results["suggested_next_steps"]))
            
            # Detailed intelligence
            if results.get("detailed_intelligence"):
                print("[PDF Generator] Building detailed intelligence...")
                story.append(PageBreak())
                story.extend(self._build_detailed_intelligence(results["detailed_intelligence"]))
            
            # Build PDF
            print("[PDF Generator] Building final PDF document...")
            doc.build(story)
            print(f"[PDF Generator] PDF successfully created at: {filepath}")
            
            return filepath
            
        except Exception as e:
            print(f"[PDF Generator] Error during PDF generation: {str(e)}")
            import traceback
            traceback.print_exc()
            raise
    
    def _generate_filename(self, prompt: str) -> str:
        """Generate clean filename from prompt"""
        # Take first 50 characters
        clean_prompt = prompt[:50]
        
        # Remove special characters
        clean_prompt = re.sub(r'[^\w\s-]', '', clean_prompt)
        
        # Replace spaces with underscores
        clean_prompt = re.sub(r'\s+', '_', clean_prompt)
        
        # Add timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        return f"Strategic_Analysis_{clean_prompt}_{timestamp}.pdf"
    
    def _build_title_page(self, prompt: str, results: dict) -> list:
        """Build title page"""
        elements = []
        
        # Title
        elements.append(Spacer(1, 2*inch))
        elements.append(Paragraph("Strategic Intelligence Report", self.styles['CustomTitle']))
        elements.append(Spacer(1, 0.5*inch))
        
        # Prompt
        elements.append(Paragraph(f"<b>Query:</b> {prompt}", self.styles['CustomBodyText']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Metadata
        metadata_text = f"""
        <b>Report Generated:</b> {datetime.now().strftime("%B %d, %Y at %I:%M %p")}<br/>
        <b>Query Type:</b> {results.get('query_type', 'N/A').replace('_', ' ').title()}<br/>
        <b>Agents Activated:</b> {len(results.get('agents_activated', []))}
        """
        elements.append(Paragraph(metadata_text, self.styles['CustomBodyText']))
        
        return elements
    
    def _build_executive_summary(self, results: dict) -> list:
        """Build executive summary section"""
        elements = []
        
        elements.append(Paragraph("Executive Summary", self.styles['SectionHeader']))
        
        summary = results.get("executive_summary", "No summary available")
        
        # Split by paragraphs and format
        paragraphs = summary.split('\n\n')
        for para in paragraphs:
            if para.strip():
                # Handle bold markers - replace ** pairs with <b></b>
                import re
                # Replace **text** with <b>text</b>
                para = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', para)
                # Escape any remaining special characters
                para = para.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                # Restore the bold tags
                para = para.replace('&lt;b&gt;', '<b>').replace('&lt;/b&gt;', '</b>')
                try:
                    elements.append(Paragraph(para.strip(), self.styles['CustomBodyText']))
                    elements.append(Spacer(1, 6))
                except Exception as e:
                    # If paragraph fails, add as plain text
                    print(f"[PDF] Warning: Could not format paragraph: {str(e)}")
                    elements.append(Paragraph(para.strip().replace('<b>', '').replace('</b>', ''), self.styles['CustomBodyText']))
                    elements.append(Spacer(1, 6))
        
        return elements
    
    def _build_classifications(self, results: dict) -> list:
        """Build strategic classifications section"""
        elements = []
        
        elements.append(Paragraph("Strategic Assessment", self.styles['SectionHeader']))
        
        # Create classification table
        data = [
            ['Dimension', 'Classification'],
            ['Evidence Strength', results.get('evidence_strength', 'N/A')],
            ['Scientific Plausibility', results.get('scientific_plausibility', 'N/A')],
            ['Innovation Attractiveness', results.get('innovation_attractiveness', 'N/A')],
            ['Commercial Feasibility', results.get('commercial_feasibility', 'N/A')]
        ]
        
        table = Table(data, colWidths=[3*inch, 3*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _build_recommendation(self, recommendation: dict) -> list:
        """Build strategic recommendation section"""
        elements = []
        
        elements.append(Paragraph("Strategic Recommendation", self.styles['SectionHeader']))
        
        # Classification
        classification = recommendation.get('classification', 'N/A')
        elements.append(Paragraph(f"<b>Classification:</b> {classification}", self.styles['Classification']))
        elements.append(Spacer(1, 6))
        
        # Rationale
        rationale = recommendation.get('rationale', 'N/A')
        elements.append(Paragraph(f"<b>Rationale:</b> {rationale}", self.styles['CustomBodyText']))
        elements.append(Spacer(1, 6))
        
        # Confidence band
        confidence = recommendation.get('confidence_band', 'N/A')
        elements.append(Paragraph(f"<b>Confidence Band:</b> {confidence}", self.styles['CustomBodyText']))
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _build_key_insights(self, insights: list) -> list:
        """Build key insights section"""
        elements = []
        
        elements.append(Paragraph("Key Insights", self.styles['SectionHeader']))
        
        for insight in insights:
            elements.append(Paragraph(f"• {insight}", self.styles['CustomBodyText']))
            elements.append(Spacer(1, 6))
        
        elements.append(Spacer(1, 20))
        return elements
    
    def _build_risks(self, risks: list) -> list:
        """Build risks and unknowns section"""
        elements = []
        
        elements.append(Paragraph("Risks & Knowledge Gaps", self.styles['SectionHeader']))
        
        for risk in risks:
            elements.append(Paragraph(f"⚠ {risk}", self.styles['CustomBodyText']))
            elements.append(Spacer(1, 6))
        
        elements.append(Spacer(1, 20))
        return elements
    
    def _build_next_steps(self, steps: list) -> list:
        """Build suggested next steps section"""
        elements = []
        
        elements.append(Paragraph("Suggested Next Steps", self.styles['SectionHeader']))
        
        for i, step in enumerate(steps, 1):
            elements.append(Paragraph(f"{i}. {step}", self.styles['CustomBodyText']))
            elements.append(Spacer(1, 6))
        
        elements.append(Spacer(1, 20))
        return elements
    
    def _build_detailed_intelligence(self, intelligence: dict) -> list:
        """Build detailed intelligence section"""
        elements = []
        
        elements.append(Paragraph("Detailed Intelligence", self.styles['SectionHeader']))
        elements.append(Paragraph(
            "The following sections contain detailed data from each intelligence agent.",
            self.styles['CustomBodyText']
        ))
        elements.append(Spacer(1, 20))
        
        for key, value in intelligence.items():
            section_name = key.replace('_', ' ').title()
            elements.append(Paragraph(section_name, self.styles['Heading3']))
            
            # Format the data
            if isinstance(value, dict):
                for k, v in list(value.items())[:10]:  # Limit to first 10 items
                    elements.append(Paragraph(f"<b>{k}:</b> {str(v)[:200]}", self.styles['CustomBodyText']))
            else:
                elements.append(Paragraph(str(value)[:500], self.styles['CustomBodyText']))
            
            elements.append(Spacer(1, 15))
        
        return elements
