from fpdf import FPDF
from datetime import datetime


def generate_receipt_pdf(
    transaction_id: str,
    full_name: str,
    bank_name: str,
    amount: float,
    games: list[list[int]],
    created_at: str = None,
) -> bytes:
    pdf = FPDF()
    pdf.add_page()

    # ─── Header ───────────────────────────────────────────────
    pdf.set_fill_color(30, 136, 229)
    pdf.rect(0, 0, 210, 35, style="F")

    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(255, 255, 255)
    pdf.set_y(10)
    pdf.cell(0, 10, "NUMBER BOT", align="C", ln=True)

    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 6, "Payment Receipt", align="C", ln=True)

    # ─── Transaction Info ─────────────────────────────────────
    pdf.set_text_color(50, 50, 50)
    pdf.set_y(45)

    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 8, "Transaction Details", ln=True)
    pdf.set_draw_color(200, 200, 200)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

    date_str = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    _row(pdf, "Transaction ID", transaction_id)
    _row(pdf, "Date", date_str)
    _row(pdf, "Name", full_name)
    _row(pdf, "Bank", bank_name)

    # ─── Games ────────────────────────────────────────────────
    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 8, "Selected Numbers", ln=True)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

    for i, game in enumerate(games):
        _row(pdf, f"Game {i + 1}", f"{game[0]}  ,  {game[1]}")

    # ─── Total ────────────────────────────────────────────────
    pdf.ln(5)
    pdf.set_draw_color(30, 136, 229)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(30, 136, 229)
    pdf.cell(90, 10, "Total Amount", ln=False)
    pdf.cell(0, 10, f"${amount:.2f}", align="R", ln=True)

    # ─── Footer ───────────────────────────────────────────────
    pdf.set_y(-25)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 6, "Thank you for your payment!", align="C", ln=True)
    pdf.cell(0, 6, "This is an auto-generated receipt.", align="C", ln=True)

    return bytes(pdf.output())


def _row(pdf: FPDF, label: str, value: str):
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(60, 8, label, ln=False)
    pdf.set_text_color(30, 30, 30)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 8, value, ln=True)