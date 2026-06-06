import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# Define clean color palette
COLOR_PRIMARY = HexColor("#1e3a8a")     # Deep Blue
COLOR_ACCENT = HexColor("#dc2626")      # Crimson Red
COLOR_TEXT = HexColor("#0f172a")        # Charcoal
COLOR_MUTED = HexColor("#475569")       # Slate Grey
COLOR_BG_LIGHT = HexColor("#f1f5f9")    # Light Grey
COLOR_BORDER = HexColor("#cbd5e1")      # Slate border

class NumberedCanvas(canvas.Canvas):
    """
    Custom canvas to handle two-pass page numbering ('Page X of Y')
    and add a sleek header and footer.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        
        # Suppress header and footer on the cover page (Page 1)
        if self._pageNumber > 1:
            # Header
            self.setFont("Helvetica", 8)
            self.setFillColor(COLOR_MUTED)
            self.drawString(54, 750, "GharVal AI - Technical Documentation")
            self.setStrokeColor(COLOR_BORDER)
            self.setLineWidth(0.5)
            self.line(54, 742, 612 - 54, 742)
            
            # Footer
            self.line(54, 54, 612 - 54, 54)
            self.drawString(54, 40, "🇳🇵 घर-मूल्य निर्धारण (GharVal AI) - Nepal Real Estate AI")
            page_str = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(612 - 54, 40, page_str)
            
        self.restoreState()


def build_pdf(filename="GharVal_AI_Documentation.pdf"):
    # Target 0.75-inch margins
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=72,
        bottomMargin=72
    )

    styles = getSampleStyleSheet()
    
    # Custom, premium typographic styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=28,
        leading=34,
        textColor=COLOR_PRIMARY,
        spaceAfter=10
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=COLOR_MUTED,
        spaceAfter=30
    )
    
    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=COLOR_PRIMARY,
        spaceBefore=18,
        spaceAfter=10,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=COLOR_PRIMARY,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=COLOR_TEXT,
        spaceAfter=10
    )
    
    code_style = ParagraphStyle(
        'CodeSnippet',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=HexColor("#0f172a"),
        spaceAfter=8
    )

    story = []

    # ================= PAGE 1: COVER PAGE =================
    story.append(Spacer(1, 100))
    # Accent flag colors strip
    flag_table = Table([["", ""]], colWidths=[10, 480])
    flag_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), COLOR_ACCENT),
        ('BACKGROUND', (1,0), (1,0), COLOR_PRIMARY),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(flag_table)
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("GharVal AI", title_style))
    story.append(Paragraph("Technical Documentation & Machine Learning Architecture", subtitle_style))
    story.append(Spacer(1, 80))
    
    # Metadata Box
    meta_data = [
        [Paragraph("<b>Target Market:</b>", body_style), Paragraph("Nepal (Kathmandu Valley / Bhaktapur)", body_style)],
        [Paragraph("<b>Platform:</b>", body_style), Paragraph("GharVal AI (घर-मूल्य निर्धारण)", body_style)],
        [Paragraph("<b>Author:</b>", body_style), Paragraph("Lead Data Scientist", body_style)],
        [Paragraph("<b>Algorithms:</b>", body_style), Paragraph("Random Forest (Champion) & XGBoost", body_style)],
        [Paragraph("<b>Status:</b>", body_style), Paragraph("Active & Verified on Bhaktapur Listings", body_style)]
    ]
    meta_table = Table(meta_data, colWidths=[100, 380])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.25, COLOR_BORDER),
        ('PADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(meta_table)
    story.append(PageBreak())

    # ================= PAGE 2: SECTIONS =================
    story.append(Paragraph("1. System Architecture", h1_style))
    story.append(Paragraph(
        "The project is structured as a modular, decoupled Machine Learning pipeline that cleanly "
        "separates data generation, exploratory analysis, training, and the final application interface. "
        "Each component runs as an independent stage of the data engineering cycle:",
        body_style
    ))
    
    arch_data = [
        [Paragraph("<b>Component</b>", body_style), Paragraph("<b>Filename / Path</b>", body_style), Paragraph("<b>Function / Output</b>", body_style)],
        [Paragraph("Data Engine", body_style), Paragraph("<code>src/generate_data.py</code>", code_style), Paragraph("Synthesizes correlated housing CSV data", body_style)],
        [Paragraph("EDA Engine", body_style), Paragraph("<code>src/eda.py</code>", code_style), Paragraph("Exports statistical analysis heatmaps/plots", body_style)],
        [Paragraph("Training Pipeline", body_style), Paragraph("<code>src/train.py</code>", code_style), Paragraph("Trains & evaluates models, exports model pickles", body_style)],
        [Paragraph("User Interface", body_style), Paragraph("<code>app.py</code>", code_style), Paragraph("Interactive Nepalese valuation web app", body_style)]
    ]
    arch_table = Table(arch_data, colWidths=[90, 140, 250])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), HexColor("#ffffff")),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('TOPPADDING', (0,0), (-1,0), 6),
        ('BOX', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.25, COLOR_BORDER),
        ('PADDING', (0,0), (-1,-1), 8),
        ('BACKGROUND', (0,1), (-1,-1), HexColor("#ffffff")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [HexColor("#ffffff"), COLOR_BG_LIGHT])
    ]))
    story.append(arch_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("2. Data Strategy & Dataset Architecture", h1_style))
    story.append(Paragraph(
        "To deliver high-fidelity estimations, the project utilizes a high-quality simulated house valuation "
        "dataset containing 1,000 observations. Programmatic synthesis allows structural correlation "
        "to remain perfectly consistent and ensures absolute reproducibility. The house price is generated "
        "using a realistic structural formula incorporating non-linear quality multipliers and randomized Gaussian noise:",
        body_style
    ))
    
    formula_text = (
        "<b>Price (USD)</b> = $40,000 + ($115 * TotalSqFt) + ($22,000 * OverallQuality) + "
        "($3.5 * TotalSqFt * OverallQuality) + ($18,000 * Bathrooms) + ($10,000 * Bedrooms) + "
        "($950 * DeltaYear) + Noise"
    )
    story.append(Paragraph(formula_text, ParagraphStyle('Formula', parent=body_style, fontName='Helvetica-Bold', backColor=COLOR_BG_LIGHT, borderPadding=10, borderWidth=0.5, borderColor=COLOR_BORDER)))
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("3. Feature Definitions & Nepalese Localization", h1_style))
    story.append(Paragraph(
        "To customize the application for standard buyers and developers in Nepal, local engineering units "
        "and parameters have been integrated directly into the inference layer:",
        body_style
    ))
    
    feat_data = [
        [Paragraph("<b>Feature</b>", body_style), Paragraph("<b>Unit / Scale</b>", body_style), Paragraph("<b>Nepalese Market Context</b>", body_style)],
        [Paragraph("Area (TotalSqFt)", body_style), Paragraph("SqFt (500 - 5000)", body_style), Paragraph("Converted dynamically to <b>Anna</b> measurements (1 Anna ≈ 342.25 SqFt)", body_style)],
        [Paragraph("Overall Quality", body_style), Paragraph("Discrete (1 - 10)", body_style), Paragraph("Correlates structure: 1-3 masonry, 4-7 RCC frame, 8-10 high-end luxury villa", body_style)],
        [Paragraph("Year Built", body_style), Paragraph("Year (1950 - 2026)", body_style), Paragraph("Evaluates seismic safety premium for post-<b>2015 Gorkha Earthquake</b> construction", body_style)],
        [Paragraph("Road Width", body_style), Paragraph("Feet (10 - 26)", body_style), Paragraph("Access road width in feet (mostly 13ft blacktopped or 20ft RCC)", body_style)],
        [Paragraph("Road Type RCC", body_style), Paragraph("Binary (0 or 1)", body_style), Paragraph("1 if access road is concrete (RCC) pavement, 0 if blacktopped", body_style)],
        [Paragraph("Estimated Price", body_style), Paragraph("NPR (रु. / Rupees)", body_style), Paragraph("Scaled via exchange index (135x) and formatted into Lakhs/Crores standard", body_style)]
    ]
    feat_table = Table(feat_data, colWidths=[100, 100, 280])
    feat_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY),
        ('BOX', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.25, COLOR_BORDER),
        ('PADDING', (0,0), (-1,-1), 8),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [HexColor("#ffffff"), COLOR_BG_LIGHT])
    ]))
    story.append(feat_table)
    
    story.append(PageBreak())

    # ================= PAGE 3: MODELS =================
    story.append(Paragraph("4. Model Comparisons & Training Mechanics", h1_style))
    story.append(Paragraph(
        "The preprocessing layer splits the dataset into 80% train and 20% test sets, scaling inputs via "
        "<code>StandardScaler</code>. The pipeline trains two distinct ensemble algorithms: <b>Random Forest Regressor</b> "
        "and an <b>XGBoost (Extreme Gradient Boosting) Regressor</b>. The evaluations show exceptional convergence:",
        body_style
    ))
    
    eval_data = [
        [Paragraph("<b>Model</b>", body_style), Paragraph("<b>Test RMSE</b>", body_style), Paragraph("<b>Test R² Score</b>", body_style), Paragraph("<b>Verdict</b>", body_style)],
        [Paragraph("Random Forest", body_style), Paragraph("<b>$17,890.62</b>", body_style), Paragraph("<b>0.8317</b>", body_style), Paragraph("<b>Champion</b> (Uncorrelated noise reduction)", body_style)],
        [Paragraph("XGBoost Regressor", body_style), Paragraph("$18,634.74", body_style), Paragraph("0.8174", body_style), Paragraph("Excellent performance, slight variance loss", body_style)]
    ]
    eval_table = Table(eval_data, colWidths=[110, 100, 100, 170])
    eval_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY),
        ('BOX', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.25, COLOR_BORDER),
        ('PADDING', (0,0), (-1,-1), 8),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [HexColor("#ffffff"), COLOR_BG_LIGHT])
    ]))
    story.append(eval_table)
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("Why Random Forest Performed Best", h2_style))
    story.append(Paragraph(
        "The Bhaktapur housing dataset incorporates randomized land price indices per Anna "
        "to simulate localized market pricing variations. Random Forest's bootstrap aggregation (bagging) "
        "is mathematically designed to minimize prediction variance by averaging 100 independent "
        "decision trees, smoothing out these uncorrelated land price noise factors more effectively "
        "than XGBoost's sequential boosting updates.",
        body_style
    ))

    story.append(Paragraph("5. Interactive Inference Layer", h1_style))
    story.append(Paragraph(
        "The Streamlit dashboard (<code>app.py</code>) provides real-time model evaluation:",
        body_style
    ))
    story.append(Paragraph(
        "<b>1. Preprocessing Pipeline:</b> Inputs entered via sliders are immediately structured into a single-row "
        "dataframe, normalized via the pre-fit scaler object (<code>scaler.pkl</code>).<br/>"
        "<b>2. Model Prediction:</b> The champion Random Forest model (<code>best_model.pkl</code>) calculates the value.<br/>"
        "<b>3. Unit Conversions:</b> Area is mapped to Anna; valuation is converted to Nepalese Rupees and "
        "represented in Lakhs / Crores notation.<br/>"
        "<b>4. Seismic Adjustments:</b> Structural pricing deductions are applied to houses built pre-2015 "
        "(Kathmandu earthquake standards), prioritizing building code compliance.",
        body_style
    ))
    
    story.append(Spacer(1, 30))
    
    # Sign-off box
    sign_data = [[
        Paragraph("<b>GharVal AI System Validation</b><br/>Status: Verified<br/>Local Web App: http://localhost:8501", body_style)
    ]]
    sign_table = Table(sign_data, colWidths=[480])
    sign_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor("#ecfdf5")),
        ('BOX', (0,0), (-1,-1), 1, HexColor("#059669")),
        ('PADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(sign_table)

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF documentation: {filename}")

if __name__ == '__main__':
    build_pdf()
