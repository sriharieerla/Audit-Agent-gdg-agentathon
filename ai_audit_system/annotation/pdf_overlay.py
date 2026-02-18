from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
import io
from PyPDF2 import PdfReader, PdfWriter, PageObject

def annotate_page(page, result, is_summary=False):
    """
    Adds audit annotation to a PDF page.
    result: Dictionary containing 'status' and 'remark'.
    is_summary: If True, generates a full-page summary report instead of overlay.
    """
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    
    if is_summary:
        # Create a full page report
        can.setFont("Helvetica-Bold", 16)
        can.drawString(100, 750, "AI AUDIT CONSOLIDATED REPORT")
        
        can.setFont("Helvetica", 12)
        y = 700
        
        # result is the 'final_summary' dictionary here
        if isinstance(result, dict):
            can.drawString(100, y, f"Final Score: {result.get('final_score')}%")
            y -= 20
            can.drawString(100, y, f"Risk Level: {result.get('risk_level')}")
            y -= 30
            
            can.drawString(100, y, "Conclusion:")
            y -= 15
            
            # Simple text wrapping for conclusion
            conclusion = result.get('final_conclusion', '')
            # A very basic wrap (split by words)
            words = conclusion.split()
            line = ""
            for word in words:
                if can.stringWidth(line + " " + word) < 400:
                    line += " " + word
                else:
                    can.drawString(100, y, line)
                    y -= 15
                    line = word
            can.drawString(100, y, line)
            
        can.save()
        packet.seek(0)
        new_pdf = PdfReader(packet)
        return new_pdf.pages[0]
        
    else:
        # Overlay for regular pages
        if page:
            # We need to know page size to position correctly, defaulting to standard
            # Drawing a box at the top right
            
            status = result.get("status", "UNKNOWN")
            remark = result.get("remark", "")
            accuracy = result.get("accuracy", 0)
            
            color = colors.green if status == "PASS" else colors.red
            
            can.setStrokeColor(color)
            can.setFillColor(color)
            can.rect(400, 750, 180, 50, fill=0) # Border
            
            can.setFont("Helvetica-Bold", 14)
            can.drawString(410, 780, f"STATUS: {status}")
            
            can.setFont("Helvetica", 10)
            can.setFillColor(colors.black)
            can.drawString(410, 765, f"Score: {accuracy}%")
            
            can.setFont("Helvetica-Oblique", 8)
            can.drawString(410, 755, f"Remark: {remark[:30]}...") 
            
            can.save()
            packet.seek(0)
            overlay_pdf = PdfReader(packet)
            overlay_page = overlay_pdf.pages[0]
            
            # Merge
            page.merge_page(overlay_page)
            return page
            
    return None
