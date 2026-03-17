from fpdf import FPDF
from datetime import datetime


def generate_receipt_pdf(
    transaction_id: str,
    full_name: str,
    phone_number: str | None,
    bank_name: str,
    amount: float,
    games: list[list[int]],
    created_at: str = None,
) -> bytes:

    W = 80
    MARGIN = 5

    # 🧠 Estimate dynamic height
    base_height = 60  # header + info + footer
    row_height = 5

    info_rows = 5  # Txn, Date, Name, Phone, Bank
    game_rows = len(games)

    total_height = base_height + (info_rows + game_rows) * row_height + 20

    pdf = FPDF(unit="mm", format=(W, total_height))
    pdf.set_margins(MARGIN, MARGIN, MARGIN)
    pdf.set_auto_page_break(auto=False)
    pdf.add_page()

    # ─── Header ───────────────────────────────────────────────
    pdf.set_fill_color(30, 136, 229)
    pdf.rect(0, 0, W, 22, style="F")

    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(255, 255, 255)
    pdf.set_y(5)
    pdf.cell(0, 7, "LUCKY NUMBER BOT", align="C", ln=True)

    pdf.set_font("Helvetica", "", 7)
    pdf.cell(0, 4, "Payment Receipt", align="C", ln=True)

    # ─── Transaction Info ─────────────────────────────────────
    pdf.set_text_color(50, 50, 50)
    pdf.set_y(27)

    pdf.set_font("Helvetica", "B", 7)
    pdf.cell(0, 5, "Transaction Details", ln=True)
    pdf.set_draw_color(200, 200, 200)
    pdf.line(MARGIN, pdf.get_y(), W - MARGIN, pdf.get_y())
    pdf.ln(2)

    date_str = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    _row(pdf, "Txn ID", transaction_id)
    _row(pdf, "Date", date_str)
    _row(pdf, "Name", full_name)
    _row(pdf, "Phone", phone_number or "N/A")
    _row(pdf, "Bank", bank_name)

    # ─── Games ────────────────────────────────────────────────
    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 7)
    pdf.cell(0, 5, "Selected Numbers", ln=True)
    pdf.line(MARGIN, pdf.get_y(), W - MARGIN, pdf.get_y())
    pdf.ln(2)

    for i, game in enumerate(games):
        _row(pdf, f"Game {i + 1}", f"{game[0]}  ,  {game[1]}")

    # ─── Total ────────────────────────────────────────────────
    pdf.ln(3)
    pdf.set_draw_color(30, 136, 229)
    pdf.line(MARGIN, pdf.get_y(), W - MARGIN, pdf.get_y())
    pdf.ln(2)

    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(30, 136, 229)
    pdf.cell(40, 6, "Total Amount", ln=False)
    pdf.cell(0, 6, f"${amount:.2f}", align="R", ln=True)

    # ─── Footer ───────────────────────────────────────────────
    pdf.ln(3)
    pdf.set_font("Helvetica", "I", 6)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 4, "Thank you for your payment!", align="C", ln=True)

    return bytes(pdf.output())


def _row(pdf: FPDF, label: str, value: str):
    pdf.set_font("Helvetica", "", 6)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(25, 5, label, ln=False)
    pdf.set_text_color(30, 30, 30)
    pdf.set_font("Helvetica", "B", 6)
    pdf.cell(0, 5, value, ln=True)