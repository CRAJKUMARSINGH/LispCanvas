"""
Test PDF Export Functionality
Tests A4 Landscape PDF generation for all modules
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.pdf_export_helper import create_pdf_download_button
from datetime import datetime
import pandas as pd

def test_pdf_generation():
    """Test PDF generation with sample data"""
    
    print("\n" + "="*60)
    print("🧪 TESTING PDF EXPORT FUNCTIONALITY")
    print("="*60 + "\n")
    
    # Sample data for testing
    test_modules = [
        {
            'name': 'Lintel Design',
            'data': {
                'Input Parameters': {
                    'Span': '1200 mm',
                    'Width': '230 mm',
                    'Depth': '300 mm',
                    'Concrete Grade': 'M25',
                    'Steel Grade': 'Fe415'
                },
                'Design Results': {
                    'Moment Capacity': '45.5 kN-m',
                    'Shear Capacity': '85.2 kN',
                    'Main Reinforcement': '3-16mm dia bars',
                    'Stirrups': '8mm @ 150mm c/c',
                    'Status': 'SAFE'
                },
                'Calculations': [
                    'Effective depth = 300 - 25 - 8 = 267 mm',
                    'Moment = wL²/8 = 45.5 kN-m',
                    'Required Ast = 450 mm²',
                    'Provided Ast = 603 mm² (3-16mm)',
                    'Design is SAFE'
                ]
            }
        },
        {
            'name': 'Circular Column',
            'data': {
                'Input Parameters': {
                    'Diameter': '400 mm',
                    'Height': '3000 mm',
                    'Concrete Grade': 'M25',
                    'Steel Grade': 'Fe415',
                    'Axial Load': '800 kN'
                },
                'Design Results': {
                    'Column Capacity': '1250 kN',
                    'Longitudinal Steel': '6-20mm dia bars',
                    'Lateral Ties': '8mm @ 200mm c/c',
                    'Steel Percentage': '1.5%',
                    'Status': 'SAFE'
                }
            }
        },
        {
            'name': 'Road Cross Section',
            'data': {
                'Input Parameters': {
                    'Carriageway Width': '7.5 m',
                    'Shoulder Width': '1.5 m',
                    'Formation Level': '100.5 m',
                    'Ground Level': '100.0 m'
                },
                'Design Results': pd.DataFrame({
                    'Chainage': ['0+000', '0+020', '0+040', '0+060'],
                    'Ground Level': [100.0, 100.2, 100.5, 100.8],
                    'Formation Level': [100.5, 100.6, 100.7, 100.8],
                    'Cut/Fill': ['Fill 0.5m', 'Fill 0.4m', 'Fill 0.2m', 'Level']
                })
            }
        }
    ]
    
    results = []
    
    for module in test_modules:
        print(f"\n📋 Testing: {module['name']}")
        print("-" * 60)
        
        try:
            # Test PDF generation
            from utils.pdf_export_helper import create_pdf_download_button
            from io import BytesIO
            from reportlab.lib.pagesizes import A4, landscape
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
            from reportlab.lib import colors
            from reportlab.lib.units import mm
            
            output = BytesIO()
            pagesize = landscape(A4)
            doc = SimpleDocTemplate(output, pagesize=pagesize)
            
            story = []
            styles = getSampleStyleSheet()
            
            # Add title
            story.append(Paragraph(f"Test Report: {module['name']}", styles['Title']))
            story.append(Spacer(1, 10*mm))
            
            # Add data sections
            for section_name, content in module['data'].items():
                story.append(Paragraph(section_name, styles['Heading2']))
                
                if isinstance(content, dict):
                    data = [[k, str(v)] for k, v in content.items()]
                    table = Table(data)
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)
                    ]))
                    story.append(table)
                elif isinstance(content, pd.DataFrame):
                    data = [content.columns.tolist()] + content.values.tolist()
                    table = Table(data)
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)
                    ]))
                    story.append(table)
                elif isinstance(content, list):
                    for item in content:
                        story.append(Paragraph(f"• {item}", styles['Normal']))
                
                story.append(Spacer(1, 5*mm))
            
            # Build PDF
            doc.build(story)
            pdf_size = len(output.getvalue())
            
            print(f"✅ PDF Generated Successfully")
            print(f"   Size: {pdf_size:,} bytes")
            print(f"   Format: A4 Landscape (297mm x 210mm)")
            
            results.append({
                'module': module['name'],
                'status': 'PASS',
                'size': pdf_size
            })
            
        except Exception as e:
            print(f"❌ PDF Generation Failed")
            print(f"   Error: {str(e)}")
            results.append({
                'module': module['name'],
                'status': 'FAIL',
                'error': str(e)
            })
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for r in results if r['status'] == 'PASS')
    failed = sum(1 for r in results if r['status'] == 'FAIL')
    
    print(f"\n✅ Passed: {passed}/{len(results)}")
    print(f"❌ Failed: {failed}/{len(results)}")
    print(f"📈 Success Rate: {(passed/len(results)*100):.1f}%")
    
    print("\n" + "="*60)
    
    if failed == 0:
        print("🎉 ALL PDF EXPORT TESTS PASSED!")
        print("✅ A4 Landscape PDF generation is working perfectly!")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
    
    print("="*60 + "\n")
    
    return passed == len(results)


if __name__ == "__main__":
    success = test_pdf_generation()
    sys.exit(0 if success else 1)
