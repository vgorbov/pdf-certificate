from fastapi import FastAPI
from fastapi.responses import Response
from weasyprint import HTML

app = FastAPI()

@app.get("/")
def home():
    return {"status": "ok"}

@app.post("/generate")
async def generate(data: dict):

    fio = data.get("fio")
    email = data.get("email")
    phone = data.get("phone")

    pay_date = "2026-01-01"
    amount = "10000 руб"

    html = f"""
    <h1>Подтверждение оплаты</h1>

    <p>ФИО: {fio}</p>
    <p>Email: {email}</p>
    <p>Телефон: {phone}</p>

    <hr>

    <p>Дата оплаты: {pay_date}</p>
    <p>Сумма оплаты: {amount}</p>
    """

    pdf = HTML(string=html).write_pdf()

    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=document.pdf"}
    )
