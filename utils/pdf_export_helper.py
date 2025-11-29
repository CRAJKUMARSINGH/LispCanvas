"""
Universal PDF Export Helper for All Modules
A4 Landscape format with professional styling
"""

import streamlit as st
from io import BytesIO
from datetime import datetime
import pandas as pd

def create_pdf_download_button(data_dict, module_name, button_label="📄 Download PDF Report (A4 Landscape)"):
    """
    Create a PDF download button for any module
    
    Args:
        data_dict: Dictionary with section data
        module_name: Name of the module
        button_label: Label for the download button
    """
    try:
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch, mm
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
        
        output = BytesIO()
        
        # A4 Landscape setup
        pagesize = landscape(A4)  # 297mm x 210mm
        doc = SimpleDocTemplate(
            output, 
            pagesize=pagesize,
            leftMargin=15*mm,
            rightMargin=15*mm,
            topMargin=15*mm,
            bottomMargin=15*mm
        )
        
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=28,
            textColor=colors.HexColor('#1f77b4'),
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2ca02c'),
            spaceAfter=15,
            spaceBefore=15,
            fontName='Helvetica-Bold'
        )
        
        header_style = ParagraphStyle(
            'CustomHeader',
            parent=styles['Heading3'],
            fontSize=14,
            textColor=colors.HexColor('#ff7f0e'),
            spaceAfter=10,
            spaceBefore=10,
            fontName='Helvetica-Bold'
        )
        
        # Title
        story.append(Paragraph(f"🏗️ {module_name}", title_style))
        story.append(Paragraph("Structural Design Suite - Professional Report", styles['Normal']))
        story.append(Spacer(1, 10*mm))
        
        # Header info box
        header_data = [
            ['Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'Module:', module_name],
            ['Software:', 'Structural Design Suite v1.0', 'Format:', 'A4 Landscape']
        ]
        header_table = Table(header_data, colWidths=[25*mm, 60*mm, 25*mm, 60*mm])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#e8f4f8')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#1f77b4')),
            ('PADDING', (0, 0), (-1, -1), 5),
        ]))
        story.append(header_table)
        story.append(Spacer(1, 10*mm))
        
        # Content sections
        for section_name, content in data_dict.items():
            # Section header
            story.append(Paragraph(section_name, subtitle_style))
            
            # Section content
            if isinstance(content, pd.DataFrame):
                # Convert DataFrame to table
                data = [content.columns.tolist()] + content.values.tolist()
                
                # Calculate column widths
                num_cols = len(data[0])
                available_width = 267*mm  # A4 landscape width minus margins
                col_width = available_width / num_cols
                
                table = Table(data, colWidths=[col_width] * num_cols)
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 11),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                    ('TOPPADDING', (0, 0), (-1, 0), 8),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0f8ff')),
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#1f77b4')),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                    ('PADDING', (0, 0), (-1, -1), 5),
                ]))
                story.append(table)
                
            elif isinstance(content, dict):
                # Convert dict to table
                data = [[k, str(v)] for k, v in content.items()]
                table = Table(data, colWidths=[80*mm, 180*mm])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f4f8')),
                    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                    ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#1f77b4')),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('PADDING', (0, 0), (-1, -1), 5),
                ]))
                story.append(table)
                
            elif isinstance(content, list):
                for item in content:
                    story.append(Paragraph(f"• {item}", styles['Normal']))
                    
            else:
                story.append(Paragraph(str(content), styles['Normal']))
            
            story.append(Spacer(1, 8*mm))
        
        # Footer
        story.append(Spacer(1, 10*mm))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.grey,
            alignment=TA_CENTER
        )
        story.append(Paragraph("Generated by Structural Design Suite | Professional Engineering Software", footer_style))
        story.append(Paragraph("This is a computer-generated document", footer_style))
        
        # Build PDF
        doc.build(story)
        output.seek(0)
        
        # Create download button
        st.download_button(
            label=button_label,
            data=output,
            file_name=f"{module_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf",
            help="Download professional PDF report in A4 Landscape format"
        )
        
        return True
        
    except ImportError:
        st.warning("⚠️ PDF export requires reportlab. Install with: pip install reportlab")
        return False
    except Exception as e:
        st.error(f"❌ Error creating PDF: {str(e)}")
        return False


def create_simple_pdf_button(title, data_dict, filename_prefix="report"):
    """
    Simplified PDF button for quick integration
    
    Args:
        title: Report title
        data_dict: Data to include in PDF
        filename_prefix: Prefix for filename
    """
    return create_pdf_download_button(data_dict, title, f"📄 Download {title} PDF")


def add_pdf_export_to_module(module_name, input_params, output_results, calculations=None):
    """
    Add PDF export section to any module
    
    Args:
        module_name: Name of the module
        input_params: Dictionary of input parameters
        output_results: Dictionary of output results
        calculations: Optional calculation steps
    """
    st.markdown("---")
    st.subheader("📄 Export Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("💡 Download professional PDF report in A4 Landscape format")
    
    with col2:
        # Prepare data for PDF
        pdf_data = {
            'Input Parameters': input_params,
            'Design Results': output_results,
        }
        
        if calculations:
            pdf_data['Calculation Steps'] = calculations
        
        # Create PDF button
        create_pdf_download_button(pdf_data, module_name)
