from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import os

def generate_pdf_report(report_id: str, drug_name: str, sections: dict):
    """Generate comprehensive PDF report with tables and formatting"""
    os.makedirs("reports", exist_ok=True)
    filename = f"reports/report_{report_id}.pdf"
    
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#374151'),
        spaceAfter=6,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=12
    )
    
    story = []
    
    # Title Page
    story.append(Spacer(1, 2*inch))
    story.append(Paragraph(f"Drug Analysis Report", title_style))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph(f"<b>{drug_name}</b>", styles['Title']))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph(f"Report ID: {report_id}", styles['Normal']))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y')}", styles['Normal']))
    story.append(PageBreak())
    
    # Executive Summary
    if "executive_summary" in sections:
        story.append(Paragraph("Executive Summary", heading_style))
        story.append(Spacer(1, 0.1*inch))
        
        exec_summary = sections["executive_summary"]
        if isinstance(exec_summary, dict):
            exec_text = exec_summary.get("narrative", str(exec_summary))
        else:
            exec_text = str(exec_summary)
        
        # Split into paragraphs
        for para in exec_text.split('\n\n'):
            if para.strip():
                story.append(Paragraph(para.strip(), body_style))
        
        story.append(PageBreak())
    
    # Highlights Section
    if "highlights" in sections:
        story.append(Paragraph("Key Highlights", heading_style))
        story.append(Spacer(1, 0.1*inch))
        
        highlights = sections["highlights"]
        if isinstance(highlights, dict):
            highlights_data = [
                ["Metric", "Value"],
                ["Total Clinical Trials", str(highlights.get("total_trials", "N/A"))],
                ["Total Patients Enrolled", str(highlights.get("total_patients", "N/A"))],
                ["Patent Portfolio Size", str(highlights.get("total_patents", "N/A"))],
                ["Safety Signals Identified", str(highlights.get("safety_signals", "N/A"))],
                ["Peak Sales Projection", str(highlights.get("market_size", "N/A"))],
                ["Approval Probability", str(highlights.get("approval_probability", "N/A"))],
                ["Investment Required", str(highlights.get("investment_required", "N/A"))],
                ["Average Confidence Score", f"{highlights.get('avg_confidence', 0)*100:.1f}%"]
            ]
            
            highlights_table = Table(highlights_data, colWidths=[3.5*inch, 2.5*inch])
            highlights_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f3f4f6')])
            ]))
            
            story.append(highlights_table)
            story.append(Spacer(1, 0.3*inch))
        
        story.append(PageBreak())
    
    # Individual Sections
    section_order = ["Clinical", "Market", "Patent", "Regulatory", "Safety", "Internal"]
    
    for section_name in section_order:
        if section_name not in sections:
            continue
            
        section_data = sections[section_name]
        if not isinstance(section_data, dict):
            continue
        
        story.append(Paragraph(f"{section_name} Analysis", heading_style))
        story.append(Spacer(1, 0.1*inch))
        
        # Summary
        if "summary" in section_data:
            story.append(Paragraph("<b>Summary:</b>", subheading_style))
            story.append(Paragraph(section_data["summary"], body_style))
            story.append(Spacer(1, 0.1*inch))
        
        # Narrative
        if "narrative" in section_data:
            story.append(Paragraph("<b>Detailed Analysis:</b>", subheading_style))
            narrative_text = section_data["narrative"]
            for para in narrative_text.split('\n\n'):
                if para.strip():
                    story.append(Paragraph(para.strip(), body_style))
            story.append(Spacer(1, 0.2*inch))
        
        # Tables
        table_mappings = {
            "trials_table": "Clinical Trials Overview",
            "efficacy_table": "Efficacy Metrics",
            "market_projections": "Market Size Projections",
            "competitive_landscape": "Competitive Landscape",
            "patent_portfolio": "Patent Portfolio",
            "fto_analysis": "Freedom to Operate Analysis",
            "regulatory_timeline": "Regulatory Timeline",
            "precedent_analysis": "Regulatory Precedents",
            "adverse_events": "Adverse Events Profile",
            "serious_events": "Serious Adverse Events",
            "safety_signals": "Safety Signals",
            "manufacturing_capacity": "Manufacturing Capacity",
            "supply_chain": "Supply Chain Analysis",
            "investment_breakdown": "Investment Breakdown"
        }
        
        for table_key, table_title in table_mappings.items():
            if table_key in section_data and section_data[table_key]:
                story.append(Paragraph(f"<b>{table_title}:</b>", subheading_style))
                
                table_data = section_data[table_key]
                if table_data and len(table_data) > 0:
                    # Create table headers
                    headers = list(table_data[0].keys())
                    table_content = [headers]
                    
                    # Add data rows
                    for row in table_data:
                        table_content.append([str(row.get(h, "")) for h in headers])
                    
                    # Calculate column widths
                    num_cols = len(headers)
                    col_width = 6.5 * inch / num_cols
                    
                    data_table = Table(table_content, colWidths=[col_width] * num_cols)
                    data_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 9),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                        ('FONTSIZE', (0, 1), (-1, -1), 8),
                        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#eff6ff')])
                    ]))
                    
                    story.append(data_table)
                    story.append(Spacer(1, 0.2*inch))
        
        # Confidence Score
        if "confidence_score" in section_data:
            confidence = section_data["confidence_score"]
            story.append(Paragraph(f"<b>Confidence Score:</b> {confidence*100:.1f}%", body_style))
        
        # Citations
        if "citations" in section_data and section_data["citations"]:
            story.append(Spacer(1, 0.1*inch))
            story.append(Paragraph("<b>References:</b>", subheading_style))
            for i, citation in enumerate(section_data["citations"], 1):
                story.append(Paragraph(f"{i}. {citation}", styles['Normal']))
        
        story.append(PageBreak())
    
    # Build PDF
    doc.build(story)
    return filename