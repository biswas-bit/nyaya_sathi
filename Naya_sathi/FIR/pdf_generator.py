import os
from django.conf import settings
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, BaseDocTemplate, PageTemplate, Frame
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
from PIL import Image as PILImage
import io

class PassportPhotoPageTemplate(PageTemplate):
    def __init__(self, id, passport_photo_path=None, **kw):
        self.passport_photo_path = passport_photo_path
        # Create frame with margins to accommodate passport photo
        frame = Frame(72, 18, A4[0]-144, A4[1]-90, leftPadding=0, bottomPadding=0, 
                     rightPadding=0, topPadding=0, id='normal')
        PageTemplate.__init__(self, id, [frame], **kw)
    
    def beforeDrawPage(self, canvas, doc):
        # Draw passport photo in top right corner if available
        if self.passport_photo_path and os.path.exists(self.passport_photo_path):
            try:
                # Get original image dimensions
                pil_img = PILImage.open(self.passport_photo_path)
                orig_width, orig_height = pil_img.size
                
                # Calculate dimensions maintaining aspect ratio
                max_width = 1.5 * inch
                max_height = 2 * inch
                
                # Calculate scaling factor
                width_ratio = max_width / orig_width
                height_ratio = max_height / orig_height
                scale_factor = min(width_ratio, height_ratio)
                
                # Calculate final dimensions
                final_width = orig_width * scale_factor
                final_height = orig_height * scale_factor
                
                # Position in top right corner
                x = A4[0] - final_width - 72  # 72 points from right edge
                y = A4[1] - final_height - 72  # 72 points from top edge
                
                # Draw the image
                canvas.drawImage(self.passport_photo_path, x, y, 
                               width=final_width, height=final_height, 
                               preserveAspectRatio=True)
                
            except Exception as e:
                # If image fails to load, continue without it
                pass

def generate_fir_pdf(fir_report):
    """
    Generate a clean, human-readable PDF from FIR report data
    """
    buffer = io.BytesIO()
    
    # Get passport photo path if it exists
    passport_photo_path = None
    if fir_report.passport_photo:
        passport_photo_path = os.path.join(settings.MEDIA_ROOT, str(fir_report.passport_photo))
    
    # Create document with custom page template
    doc = BaseDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72,
                         topMargin=90, bottomMargin=18)
    
    # Add page templates
    first_page_template = PassportPhotoPageTemplate('first_page', passport_photo_path)
    normal_page_template = PageTemplate('normal_page', 
                                      [Frame(72, 18, A4[0]-144, A4[1]-90, 
                                           leftPadding=0, bottomPadding=0, 
                                           rightPadding=0, topPadding=0, id='normal')])
    
    doc.addPageTemplates([first_page_template, normal_page_template])
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.darkblue
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        spaceBefore=20,
        textColor=colors.darkblue
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6,
        alignment=TA_LEFT
    )
    
    label_style = ParagraphStyle(
        'LabelStyle',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6,
        textColor=colors.darkblue,
        fontName='Helvetica-Bold'
    )
    
    # Content elements
    story = []
    
    # Start with first page template (includes passport photo)
    from reportlab.platypus import NextPageTemplate
    story.append(NextPageTemplate('first_page'))
    
    # Title
    story.append(Paragraph("FIRST INFORMATION REPORT (FIR)", title_style))
    story.append(Spacer(1, 20))
    
    # Report Info Table
    report_info_data = [
        ['Report ID:', str(fir_report.id)],
        ['Subject:', fir_report.get_subject_display_name()],
        ['Date & Time:', fir_report.created_at.strftime('%d %B %Y, %I:%M %p')],
        ['Status:', 'Submitted']
    ]
    
    report_info_table = Table(report_info_data, colWidths=[2*inch, 4*inch])
    report_info_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    story.append(report_info_table)
    story.append(Spacer(1, 30))
    
    # Personal Information Section
    story.append(Paragraph("PERSONAL INFORMATION", heading_style))
    
    personal_data = [
        ['Full Name:', fir_report.name],
        ['Email Address:', fir_report.email],
        ['Contact Number:', fir_report.contact],
        ['Address:', fir_report.address]
    ]
    
    personal_table = Table(personal_data, colWidths=[2*inch, 4*inch])
    personal_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
    ]))
    
    story.append(personal_table)
    story.append(Spacer(1, 30))
    
    # Incident Description Section
    story.append(Paragraph("INCIDENT DESCRIPTION", heading_style))
    description_para = Paragraph(fir_report.description, normal_style)
    story.append(description_para)
    story.append(Spacer(1, 30))
    
    # Add page break before evidence images
    evidence_images = fir_report.evidence_images.all()
    if evidence_images:
        story.append(PageBreak())
        story.append(NextPageTemplate('normal_page'))
        
        # Evidence Section - New Page
        story.append(Paragraph("EVIDENCE IMAGES", title_style))
        story.append(Spacer(1, 30))
        
        for idx, evidence in enumerate(evidence_images, 1):
            try:
                evidence_path = os.path.join(settings.MEDIA_ROOT, str(evidence.image))
                if os.path.exists(evidence_path):
                    # Evidence heading
                    evidence_title = f"Evidence {idx}"
                    if evidence.description:
                        evidence_title += f": {evidence.description}"
                    story.append(Paragraph(evidence_title, heading_style))
                    story.append(Spacer(1, 10))
                    
                    # Resize image to fit on page
                    pil_img = PILImage.open(evidence_path)
                    orig_width, orig_height = pil_img.size
                    
                    # Calculate dimensions maintaining aspect ratio
                    max_width = 5*inch
                    max_height = 4*inch
                    
                    # Calculate scaling factor
                    width_ratio = max_width / orig_width
                    height_ratio = max_height / orig_height
                    scale_factor = min(width_ratio, height_ratio)
                    
                    # Calculate final dimensions
                    final_width = orig_width * scale_factor
                    final_height = orig_height * scale_factor
                    
                    img = Image(evidence_path)
                    img.drawHeight = final_height
                    img.drawWidth = final_width
                    story.append(img)
                    story.append(Spacer(1, 30))
                    
            except Exception as e:
                story.append(Paragraph(f"Evidence image {idx} could not be loaded: {str(e)}", normal_style))
                story.append(Spacer(1, 20))
    
    # Add page break before citizenship documents
    if fir_report.citizenship_front or fir_report.citizenship_back:
        story.append(PageBreak())
        story.append(NextPageTemplate('normal_page'))
        
        # Citizenship Documents Section - New Page
        story.append(Paragraph("CITIZENSHIP DOCUMENTS", title_style))
        story.append(Spacer(1, 30))
        
        # Create a table for front and back images side by side
        citizenship_data = []
        citizenship_images = []
        
        if fir_report.citizenship_front:
            try:
                front_path = os.path.join(settings.MEDIA_ROOT, str(fir_report.citizenship_front))
                if os.path.exists(front_path):
                    front_img = Image(front_path)
                    front_img.drawHeight = 3*inch
                    front_img.drawWidth = 4*inch
                    citizenship_images.append(('FRONT SIDE', front_img))
            except Exception as e:
                citizenship_images.append(('FRONT SIDE', Paragraph(f"Image could not be loaded: {str(e)}", normal_style)))
        
        if fir_report.citizenship_back:
            try:
                back_path = os.path.join(settings.MEDIA_ROOT, str(fir_report.citizenship_back))
                if os.path.exists(back_path):
                    back_img = Image(back_path)
                    back_img.drawHeight = 3*inch
                    back_img.drawWidth = 4*inch
                    citizenship_images.append(('BACK SIDE', back_img))
            except Exception as e:
                citizenship_images.append(('BACK SIDE', Paragraph(f"Image could not be loaded: {str(e)}", normal_style)))
        
        # Add citizenship images
        for label, img in citizenship_images:
            story.append(Paragraph(label, heading_style))
            story.append(Spacer(1, 10))
            story.append(img)
            story.append(Spacer(1, 30))
    
    # Footer
    story.append(Spacer(1, 50))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        alignment=TA_CENTER,
        textColor=colors.grey
    )
    
    story.append(Paragraph("This is a computer-generated document. No signature is required.", footer_style))
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%d %B %Y at %I:%M %p')}", footer_style))
    
    # Build PDF
    doc.build(story)
    
    # Get the value of the BytesIO buffer and return it
    pdf = buffer.getvalue()
    buffer.close()
    
    return pdf

def download_fir_pdf(request, fir_report):
    """
    Generate and return PDF as HTTP response for download
    """
    pdf_data = generate_fir_pdf(fir_report)
    
    response = HttpResponse(pdf_data, content_type='application/pdf')
    filename = f"FIR_Report_{fir_report.id}_{fir_report.created_at.strftime('%Y%m%d_%H%M%S')}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response