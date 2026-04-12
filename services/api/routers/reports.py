import io
from datetime import datetime
 
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    HRFlowable, Image, PageBreak, Paragraph,
    SimpleDocTemplate, Spacer, Table, TableStyle,
)
 
# ── Palette ──────────────────────────────────────────────────────────────────
INK        = colors.HexColor("#0F1923")   # near-black text
MUTED      = colors.HexColor("#6B7685")   # secondary text
RULE       = colors.HexColor("#DDE2E8")   # light divider
PAGE_BG    = colors.white
ACCENT     = colors.HexColor("#1A56DB")   # brand blue
ACCENT_LIGHT = colors.HexColor("#EBF0FF") # blue tint bg
 
SEV = {
    "critical": colors.HexColor("#DC2626"),
    "high":     colors.HexColor("#EA580C"),
    "medium":   colors.HexColor("#D97706"),
    "low":      colors.HexColor("#16A34A"),
}
SEV_BG = {
    "critical": colors.HexColor("#FEF2F2"),
    "high":     colors.HexColor("#FFF7ED"),
    "medium":   colors.HexColor("#FFFBEB"),
    "low":      colors.HexColor("#F0FDF4"),
}
 
W, H = A4
MARGIN = 18 * mm
USE_W  = W - 2 * MARGIN
 
 
# ── Style helpers ─────────────────────────────────────────────────────────────
def S(name, **kw):
    defaults = dict(fontName="Helvetica", fontSize=9,
                    textColor=INK, leading=14, spaceAfter=0)
    defaults.update(kw)
    return ParagraphStyle(name, **defaults)
 
 
STYLES = {
    "cover_title":  S("ct",  fontSize=28, fontName="Helvetica-Bold",
                       textColor=colors.white, leading=34),
    "cover_sub":    S("cs",  fontSize=11, textColor=colors.HexColor("#BFC9D4"),
                       leading=16),
    "cover_meta":   S("cm",  fontSize=8,  textColor=colors.HexColor("#8FA0B0"),
                       leading=12),
    "section_hd":   S("sh",  fontSize=10, fontName="Helvetica-Bold",
                       textColor=ACCENT, spaceBefore=14, spaceAfter=5,
                       leading=14),
    "body":         S("bd",  fontSize=9,  textColor=INK, leading=14),
    "muted":        S("mu",  fontSize=8,  textColor=MUTED, leading=12),
    "label":        S("lb",  fontSize=7,  fontName="Helvetica-Bold",
                       textColor=MUTED, leading=10, spaceAfter=1),
    "value":        S("vl",  fontSize=10, fontName="Helvetica-Bold",
                       textColor=INK, leading=13),
    "value_accent": S("va",  fontSize=11, fontName="Helvetica-Bold",
                       textColor=ACCENT, leading=13),
    "mono":         S("mn",  fontSize=8,  fontName="Courier",
                       textColor=colors.HexColor("#1A3A5C"), leading=12),
    "footer":       S("ft",  fontSize=7,  textColor=MUTED, alignment=TA_CENTER),
    "tbl_hd":       S("th",  fontSize=8,  fontName="Helvetica-Bold",
                       textColor=colors.white, leading=11),
    "tbl_cell":     S("tc",  fontSize=8,  textColor=INK, leading=12),
    "tbl_muted":    S("tm",  fontSize=8,  textColor=MUTED, leading=12),
}
 
 
def rule(color=RULE, thickness=0.5, space=6):
    return HRFlowable(width="100%", thickness=thickness,
                      color=color, spaceAfter=space, spaceBefore=4)
 
 
def vspace(n=6):
    return Spacer(1, n)
 
 
# ── Cover page ────────────────────────────────────────────────────────────────
def _cover(story, meta: dict):
    now   = meta["generated"]
    total = meta["total"]
    period = meta.get("period", "Last 24 hours")
 
    # Full-bleed dark header band
    band = Table(
        [[
            Paragraph("OpsPilot", STYLES["cover_title"]),
            Paragraph(
                f'<font color="#8FA0B0">Generated<br/>{now}</font>',
                S("cr", fontSize=8, textColor=colors.HexColor("#8FA0B0"),
                  alignment=TA_RIGHT, leading=12),
            ),
        ]],
        colWidths=[USE_W * 0.7, USE_W * 0.3],
    )
    band.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), INK),
        ("TOPPADDING",    (0, 0), (-1, -1), 18),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 18),
        ("LEFTPADDING",   (0, 0), (-1, -1), 16),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 16),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("ROUNDEDCORNERS", [4, 4, 0, 0]),
    ]))
    story.append(band)
 
    # Sub-band accent stripe
    stripe = Table([[""]], colWidths=[USE_W])
    stripe.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), ACCENT),
        ("TOPPADDING",    (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(stripe)
    story.append(vspace(14))
 
    # Subtitle line
    story.append(Paragraph(
        "Incident Intelligence Report", 
        S("st", fontSize=13, fontName="Helvetica-Bold", textColor=INK, leading=18),
    ))
    story.append(Paragraph(period, STYLES["muted"]))
    story.append(vspace(18))
    story.append(rule(ACCENT, thickness=1.5, space=14))
 
 
# ── KPI summary row ───────────────────────────────────────────────────────────
def _kpi_row(story, alerts: list):
    total = len(alerts)
    by_sev = {s: 0 for s in ["critical", "high", "medium", "low"]}
    services = {}
    for a in alerts:
        s = a.get("severity", "low").lower()
        by_sev[s] = by_sev.get(s, 0) + 1
        svc = a.get("service", "unknown")
        services[svc] = services.get(svc, 0) + 1
 
    top_svc = max(services, key=services.get) if services else "—"
 
    def kpi(label, value, color=INK):
        return [
            Paragraph(label, STYLES["label"]),
            Paragraph(
                str(value),
                S("kv", fontSize=18, fontName="Helvetica-Bold",
                  textColor=color, leading=22),
            ),
        ]
 
    cells = [
        kpi("TOTAL INCIDENTS", total, ACCENT),
        kpi("CRITICAL", by_sev["critical"], SEV["critical"]),
        kpi("HIGH", by_sev["high"], SEV["high"]),
        kpi("MEDIUM", by_sev["medium"], SEV["medium"]),
        kpi("LOW", by_sev["low"], SEV["low"]),
        kpi("TOP SERVICE", top_svc, INK),
    ]
 
    t = Table([cells], colWidths=[USE_W / 6] * 6)
    t.setStyle(TableStyle([
        ("BOX",           (0, 0), (-1, -1), 0.5, RULE),
        ("INNERGRID",     (0, 0), (-1, -1), 0.5, RULE),
        ("TOPPADDING",    (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND",    (0, 0), (0, -1), ACCENT_LIGHT),
    ]))
    story.append(t)
    story.append(vspace(16))
 
 
# ── Severity breakdown table ──────────────────────────────────────────────────
def _severity_table(story, alerts: list):
    story.append(Paragraph("Severity Breakdown", STYLES["section_hd"]))
    story.append(rule())
 
    total = len(alerts)
    by_sev = {s: 0 for s in ["critical", "high", "medium", "low"]}
    for a in alerts:
        s = a.get("severity", "low").lower()
        by_sev[s] = by_sev.get(s, 0) + 1
 
    action = {
        "critical": "Immediate — page on-call now",
        "high":     "Urgent — investigate within 1 hour",
        "medium":   "Standard — review within 4 hours",
        "low":      "Informational — review at next standup",
    }
 
    rows = [[
        Paragraph("SEVERITY",       STYLES["tbl_hd"]),
        Paragraph("COUNT",          STYLES["tbl_hd"]),
        Paragraph("% OF TOTAL",     STYLES["tbl_hd"]),
        Paragraph("RECOMMENDED ACTION", STYLES["tbl_hd"]),
    ]]
 
    for sev in ["critical", "high", "medium", "low"]:
        count = by_sev[sev]
        pct   = f"{count/total*100:.1f}%" if total else "0%"
        c     = SEV[sev]
        rows.append([
            Paragraph(
                f'<font color="#{c.hexval()[2:]}"><b>{sev.upper()}</b></font>',
                STYLES["tbl_cell"],
            ),
            Paragraph(str(count), STYLES["tbl_cell"]),
            Paragraph(pct,        STYLES["tbl_cell"]),
            Paragraph(action[sev], STYLES["tbl_muted"]),
        ])
 
    col_w = [USE_W*0.15, USE_W*0.10, USE_W*0.15, USE_W*0.60]
    t = Table(rows, colWidths=col_w)
    style = [
        ("BACKGROUND",    (0, 0), (-1, 0),  INK),
        ("BACKGROUND",    (0, 1), (-1, -1), colors.white),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ("BOX",           (0, 0), (-1, -1), 0.5, RULE),
        ("INNERGRID",     (0, 0), (-1, -1), 0.5, RULE),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ]
    for i, sev in enumerate(["critical", "high", "medium", "low"], 1):
        if by_sev[sev] > 0:
            style.append(("BACKGROUND", (0, i), (0, i), SEV_BG[sev]))
    t.setStyle(TableStyle(style))
    story.append(t)
    story.append(vspace(18))
 
 
# ── Metrics mini-table ────────────────────────────────────────────────────────
def _metrics_strip(metrics: dict):
    def cell(label, val, unit="", warn=False):
        color = SEV["high"] if warn else INK
        return [
            Paragraph(label, STYLES["label"]),
            Paragraph(
                f'{val}{unit}',
                S("mv", fontSize=9, fontName="Helvetica-Bold",
                  textColor=color, leading=12),
            ),
        ]
 
    cpu  = metrics.get("cpu", 0)
    mem  = metrics.get("memory", 0)
    err  = metrics.get("error_rate", 0)
    lat  = metrics.get("latency_p99", 0)
 
    cells = [
        cell("CPU", cpu, "%",  warn=float(cpu) > 80),
        cell("MEMORY", mem, "%", warn=float(mem) > 80),
        cell("ERROR RATE", err, "",  warn=float(err) > 0.1),
        cell("P99 LATENCY", lat, " ms", warn=float(lat) > 2000),
    ]
 
    t = Table([cells], colWidths=[USE_W / 4] * 4)
    t.setStyle(TableStyle([
        ("BOX",           (0, 0), (-1, -1), 0.5, RULE),
        ("INNERGRID",     (0, 0), (-1, -1), 0.5, RULE),
        ("BACKGROUND",    (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ("TOPPADDING",    (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
    ]))
    return t
 
 
# ── Individual incident card ──────────────────────────────────────────────────
def _incident_card(story, idx: int, alert: dict):
    sev     = alert.get("severity", "low").lower()
    service = alert.get("service", "unknown")
    score   = alert.get("anomaly_score", "—")
    metrics = alert.get("metrics", {})
    explain = alert.get("explanation", "No explanation available.")
    sev_c   = SEV.get(sev, MUTED)
    sev_bg  = SEV_BG.get(sev, colors.white)
 
    # ── Card header ──
    header = Table(
        [[
            Paragraph(
                f'<font color="#{sev_c.hexval()[2:]}">●</font>'
                f'  <b>Incident #{idx:02d}</b>  ·  {service}',
                S("ih", fontSize=10, fontName="Helvetica-Bold",
                  textColor=INK, leading=14),
            ),
            Paragraph(
                f'Severity: <b>{sev.upper()}</b>  ·  Score: <b>{score}</b>',
                S("is", fontSize=8, textColor=MUTED,
                  alignment=TA_RIGHT, leading=12),
            ),
        ]],
        colWidths=[USE_W * 0.6, USE_W * 0.4],
    )
    header.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), sev_bg),
        ("BOX",           (0, 0), (-1, -1), 0.5, sev_c),
        ("TOPPADDING",    (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ("LEFTPADDING",   (0, 0), (-1, -1), 12),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 12),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(header)
 
    # ── Metrics strip ──
    story.append(_metrics_strip(metrics))
 
    # ── AI analysis box ──
    clean = explain.replace("\n", "<br/>")
    analysis = Table(
        [
            [Paragraph("AI ANALYSIS", STYLES["label"])],
            [Paragraph(clean, STYLES["mono"])],
        ],
        colWidths=[USE_W],
    )
    analysis.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), ACCENT_LIGHT),
        ("BOX",           (0, 0), (-1, -1), 0.5, ACCENT),
        ("LEFTPADDING",   (0, 0), (-1, -1), 12),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 12),
        ("TOPPADDING",    (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(analysis)
    story.append(vspace(12))
 
 
# ── Page footer callback ──────────────────────────────────────────────────────
class _Footer:
    def __init__(self, total_pages_ref):
        self._ref = total_pages_ref
 
    def __call__(self, canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(MUTED)
        y = 10 * mm
        canvas.drawString(MARGIN, y,
            "OpsPilot · AI-Powered Incident Intelligence · Confidential")
        canvas.drawRightString(W - MARGIN, y,
            f"Page {doc.page}")
        canvas.setStrokeColor(RULE)
        canvas.setLineWidth(0.5)
        canvas.line(MARGIN, y + 4 * mm, W - MARGIN, y + 4 * mm)
        canvas.restoreState()
 
 
# ── Master builder ────────────────────────────────────────────────────────────
def build_pdf(alerts: list) -> bytes:
    buf    = io.BytesIO()
    footer = _Footer({})
    now    = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
 
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=14 * mm, bottomMargin=20 * mm,
        onFirstPage=footer, onLaterPages=footer,
    )
 
    story = []
 
    _cover(story, {"generated": now, "total": len(alerts)})
    _kpi_row(story, alerts)
    _severity_table(story, alerts)
 
    story.append(Paragraph("Incident Details", STYLES["section_hd"]))
    story.append(rule())
    story.append(vspace(4))
 
    for i, alert in enumerate(alerts, 1):
        _incident_card(story, i, alert)
 
    # ── Closing note ──
    story.append(rule(ACCENT, thickness=1))
    story.append(Paragraph(
        "This report was generated automatically by OpsPilot. "
        "All AI analysis should be verified by a qualified engineer before action is taken. "
        f"Generated: {now}",
        STYLES["muted"],
    ))
 
    doc.build(story)
    buf.seek(0)
    return buf.read()
 
 
# ── FastAPI router ────────────────────────────────────────────────────────────
try:
    import json
    import os
    import redis.asyncio as aioredis
    from fastapi import APIRouter
    from fastapi.responses import StreamingResponse
 
    router = APIRouter()
 
    @router.get("/api/reports/latest")
    async def generate_report(limit: int = 50):
        rc = aioredis.from_url(os.getenv("REDIS_URL", "redis://redis:6379"))
        try:
            entries = await rc.xrevrange("opspilot:alerts", count=limit)
            alerts = []
            for _id, fields in entries:
                try:
                    alerts.append(json.loads(fields[b"data"]))
                except Exception:
                    continue
        finally:
            await rc.aclose()
 
        pdf   = build_pdf(alerts)
        fname = f"opspilot_{datetime.utcnow().strftime('%Y%m%d_%H%M')}.pdf"
        return StreamingResponse(
            io.BytesIO(pdf),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={fname}"},
        )
 
except ImportError:
    pass