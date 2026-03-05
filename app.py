from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from weasyprint import HTML

app = FastAPI()

# Чтобы форма с GetCourse/другого домена могла обращаться к API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # потом можно сузить под твой домен
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "ok"}

def render_html(fio: str, email: str, phone: str, pay_date: str, amount: str) -> str:
    return f"""
<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8" />
  <style>
    body {{ font-family: DejaVu Sans, Arial, sans-serif; padding: 40px; }}
    .title {{ font-size: 22px; font-weight: 700; margin-bottom: 18px; }}
    .row {{ margin: 8px 0; font-size: 14px; }}
    .box {{ border: 1px solid #333; padding: 16px; margin-top: 16px; }}
    .small {{ margin-top: 30px; font-size: 11px; color: #555; }}
  </style>
</head>
<body>
  <div class="title">Подтверждение оплаты</div>

  <div class="row"><b>ФИО:</b> {fio}</div>
  <div class="row"><b>Email:</b> {email}</div>
  <div class="row"><b>Телефон:</b> {phone}</div>

  <div class="box">
    <div class="row"><b>Дата оплаты:</b> {pay_date}</div>
    <div class="row"><b>Сумма оплаты:</b> {amount}</div>
  </div>

  <div class="small">Документ сформирован автоматически.</div>
</body>
</html>
"""

@app.post("/generate")
async def generate(data: dict):
    fio = (data.get("fio") or "").strip()
    email = (data.get("email") or "").strip()
    phone = (data.get("phone") or "").strip()

    if not fio or not email:
        raise HTTPException(status_code=400, detail="Нужно указать fio и email")

    # Пока заглушки (на следующем шаге подключим GetCourse)
    pay_date = "2026-01-01"
    amount = "10000 руб"

    html = render_html(fio, email, phone, pay_date, amount)
    pdf_bytes = HTML(string=html).write_pdf()

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="certificate.pdf"'}
    )
