"""
Export Utilities for Excel and PDF
Provides export functionality for all modules
"""

import pandas as pd
from datetime import datetime
import io

def export_to_excel(data_dict, filename="design_report.xlsx"):
    """
    Export design data to Excel file
    
    Args:
        data_dict: Dictionary with sheet_name: dataframe pairs
        filename: Output filename
        
    Returns:
        BytesIO object containing Excel file
    """
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Write each sheet
        for sheet_name, data in data_dict.items():
            if isinstance(data, pd.DataFrame):
                data.to_excel(writer, sheet_name=sheet_name, index=False)
            elif isinstance(data, dict):
                df = pd.DataFrame([data]).T
                df.columns = ['Value']
                df.to_excel(writer, sheet_name=sheet_name)
            elif isinstance(data, list):
                df = pd.DataFrame(data)
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        # Add metadata sheet
        metadata = pd.DataFrame({
            'Property': ['Generated Date', 'Software', 'Version'],
            'Value': [datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
                     'Structural Design Suite', '1.0.0']
        })
        metadata.to_excel(writer, sheet_name='Metadata', index=False)
    
    output.seek(0)
    return output

def export_to_pdf(data_dict, filename="design_report.pdf", landscape=True):
    """
    Export design data to PDF file in A4 Landscape
    
    Args:
        data_dict: Dictionary with section_name: content pairs
        filename: Output filename
        landscape: Use landscape orientation (default True)
        
    Returns:
        BytesIO object containing PDF file
    """
    try:
        from reportlab.lib.pagesizes import A4, landscape as landscape_mode
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
        from reportlab.lib import colors
        
        output = io.BytesIO()
        
        # Use A4 Landscape
        pagesize = landscape_mode(A4) if landscape else A4
        doc = SimpleDocTemplate(output, pagesize=pagesize,
                               leftMargin=0.5*inch, rightMargin=0.5*inch,
                               topMargin=0.5*inch, bottomMargin=0.5*inch)
        story = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f77b4'),
            spaceAfter=30,
        )
        story.append(Paragraph("Structural Design Report", title_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Metadata
        story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        story.append(Paragraph("Software: Structural Design Suite v1.0.0", styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Content sections
        for section_name, content in data_dict.items():
            # Section header
            story.append(Paragraph(section_name, styles['Heading2']))
            story.append(Spacer(1, 0.1*inch))
            
            # Section content
            if isinstance(content, pd.DataFrame):
                # Convert DataFrame to table
                data = [content.columns.tolist()] + content.values.tolist()
                table = Table(data)
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                story.append(table)
            elif isinstance(content, dict):
                # Convert dict to table
                data = [[k, str(v)] for k, v in content.items()]
                table = Table(data, colWidths=[3*inch, 3*inch])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                story.append(table)
            elif isinstance(content, list):
                for item in content:
                    story.append(Paragraph(f"• {item}", styles['Normal']))
            else:
                story.append(Paragraph(str(content), styles['Normal']))
            
            story.append(Spacer(1, 0.3*inch))
        
        # Build PDF
        doc.build(story)
        output.seek(0)
        return output
        
    except ImportError:
        # Fallback if reportlab not installed
        return None

def create_calculation_report(module_name, inputs, outputs, calculations=None):
    """
    Create standardized calculation report
    
    Args:
        module_name: Name of the module
        inputs: Dictionary of input parameters
        outputs: Dictionary of output results
        calculations: Optional list of calculation steps
        
    Returns:
        Dictionary ready for export
    """
    report = {
        'Project Info': {
            'Module': module_name,
            'Date': datetime.now().strftime('%Y-%m-%d'),
            'Time': datetime.now().strftime('%H:%M:%S'),
        },
        'Input Parameters': inputs,
        'Design Results': outputs,
    }
    
    if calculations:
        report['Calculations'] = calculations
    
    return report

def format_for_excel(value):
    """Format value for Excel export"""
    if isinstance(value, (int, float)):
        return round(value, 3)
    return str(value)

def format_for_pdf(value):
    """Format value for PDF export"""
    if isinstance(value, (int, float)):
        return f"{value:.3f}"
    return str(value)
