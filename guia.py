from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import Flowable
from reportlab.lib.colors import HexColor

# ── Color palette ──────────────────────────────────────────────
C_NAVY     = HexColor("#1A2A4A")   # dark navy – headers
C_BLUE     = HexColor("#2563EB")   # accent blue
C_LIGHT    = HexColor("#EFF6FF")   # light blue bg
C_GRAY     = HexColor("#F1F5F9")   # row stripe
C_DKGRAY   = HexColor("#475569")   # body text
C_ORANGE   = HexColor("#EA580C")   # IMPORTANTE
C_GREEN    = HexColor("#16A34A")   # NOTA
C_RULE     = HexColor("#CBD5E1")   # hr line
C_WHITE    = colors.white

PAGE_W, PAGE_H = A4
MARGIN = 2.2 * cm


# ── Custom horizontal rule ──────────────────────────────────────
class ThinRule(Flowable):
    def __init__(self, width, color=C_RULE, thickness=0.5):
        Flowable.__init__(self)
        self.width = width
        self.color = color
        self.thickness = thickness
        self.height = thickness + 2

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, self.thickness, self.width, self.thickness)


# ── Page template with header/footer ───────────────────────────
def make_page_template(canvas, doc):
    canvas.saveState()
    w, h = A4
    # Top bar
    canvas.setFillColor(C_NAVY)
    canvas.rect(0, h - 1.1 * cm, w, 1.1 * cm, fill=1, stroke=0)
    canvas.setFillColor(C_WHITE)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.drawString(MARGIN, h - 0.75 * cm, "MANUAL DE USUARIO  |  RamisToolX (Sistema OCS)")
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(w - MARGIN, h - 0.75 * cm, "Corporación Ramis S.A.C.  —  2026")
    # Bottom bar
    canvas.setFillColor(C_NAVY)
    canvas.rect(0, 0, w, 0.8 * cm, fill=1, stroke=0)
    canvas.setFillColor(C_WHITE)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(MARGIN, 0.28 * cm, "Confidencial  ·  Uso interno  ·  Team Orbit")
    canvas.drawRightString(w - MARGIN, 0.28 * cm, f"Página {doc.page}")
    canvas.restoreState()


# ── Cover page ──────────────────────────────────────────────────
def cover_page():
    elements = []
    w = PAGE_W - 2 * MARGIN

    # Big navy block (simulated via a 1-cell table)
    cover_data = [[""]]
    cover_table = Table(cover_data, colWidths=[w], rowHeights=[4.5 * cm])
    cover_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), C_NAVY),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [C_NAVY]),
    ]))
    elements.append(Spacer(1, 1.5 * cm))
    elements.append(cover_table)
    elements.append(Spacer(1, 0.3 * cm))

    st = getSampleStyleSheet()

    title_style = ParagraphStyle("cover_title", parent=st["Normal"],
        fontSize=28, textColor=C_NAVY, fontName="Helvetica-Bold",
        spaceAfter=4, leading=34, alignment=TA_LEFT)
    sub_style = ParagraphStyle("cover_sub", parent=st["Normal"],
        fontSize=14, textColor=C_BLUE, fontName="Helvetica-Bold",
        spaceAfter=2, alignment=TA_LEFT)
    caption_style = ParagraphStyle("cover_cap", parent=st["Normal"],
        fontSize=10, textColor=C_DKGRAY, fontName="Helvetica",
        spaceAfter=2, alignment=TA_LEFT)

    elements.append(Spacer(1, 0.6 * cm))
    elements.append(Paragraph("RamisToolX", title_style))
    elements.append(Paragraph("Sistema OCS — Gestión de Préstamos y Devoluciones", sub_style))
    elements.append(ThinRule(w, C_BLUE, 1.5))
    elements.append(Spacer(1, 0.4 * cm))

    # Ficha técnica table
    ficha = [
        ["CAMPO", "DETALLE"],
        ["Nombre del Sistema", "RamisToolX (Sistema OCS)"],
        ["Cliente", "Corporación Ramis S.A.C."],
        ["Desarrollado por", "Team Orbit"],
        ["Versión del Documento", "1.0.0"],
        ["Año de Emisión", "2026"],
        ["Clasificación", "Confidencial — Uso Interno"],
        ["Plataforma Frontend", "Aplicación Móvil (Flutter)"],
        ["Backend", "API REST — FastAPI (Dockerizado)"],
        ["Base de Datos", "PostgreSQL"],
    ]
    col_w = [5.5 * cm, w - 5.5 * cm]
    ft = Table(ficha, colWidths=col_w)
    ft.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), C_NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), C_WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 1), (-1, -1), 9),
        ("TEXTCOLOR", (0, 1), (-1, -1), C_NAVY),
        ("BACKGROUND", (0, 1), (-1, -1), C_GRAY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [C_WHITE, C_GRAY]),
        ("GRID", (0, 0), (-1, -1), 0.4, C_RULE),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    elements.append(ft)
    elements.append(Spacer(1, 1 * cm))

    # Disclaimer
    disc = ParagraphStyle("disc", parent=st["Normal"],
        fontSize=7.5, textColor=C_DKGRAY, fontName="Helvetica-Oblique",
        alignment=TA_CENTER, leading=11)
    elements.append(Paragraph(
        "Este documento es propiedad exclusiva de Corporación Ramis S.A.C. "
        "y ha sido elaborado por Team Orbit. Queda estrictamente prohibida "
        "su reproducción parcial o total sin autorización escrita.",
        disc))
    elements.append(PageBreak())
    return elements


# ── Style helpers ───────────────────────────────────────────────
def get_styles():
    st = getSampleStyleSheet()
    base = dict(fontName="Helvetica", textColor=C_DKGRAY, leading=14)

    styles = {
        "h1": ParagraphStyle("h1", **base,
            fontSize=17, fontName="Helvetica-Bold", textColor=C_NAVY,
            spaceBefore=18, spaceAfter=6, leading=22,
            borderPad=(0, 0, 4, 0)),
        "h2": ParagraphStyle("h2", **base,
            fontSize=13, fontName="Helvetica-Bold", textColor=C_BLUE,
            spaceBefore=14, spaceAfter=4),
        "h3": ParagraphStyle("h3", **base,
            fontSize=11, fontName="Helvetica-Bold", textColor=C_NAVY,
            spaceBefore=10, spaceAfter=3),
        "body": ParagraphStyle("body", **base,
            fontSize=9.5, alignment=TA_JUSTIFY, spaceAfter=5),
        "bullet": ParagraphStyle("bullet", **base,
            fontSize=9.5, leftIndent=18, firstLineIndent=-12,
            spaceAfter=3, bulletIndent=6),
        "step_num": ParagraphStyle("step_num", **base,
            fontSize=9.5, fontName="Helvetica-Bold", textColor=C_BLUE,
            leftIndent=0, spaceAfter=2),
        "step_body": ParagraphStyle("step_body", **base,
            fontSize=9.5, leftIndent=22, spaceAfter=5),
        "note": ParagraphStyle("note", **base,
            fontSize=9, fontName="Helvetica-Oblique", textColor=C_GREEN,
            leftIndent=12, spaceBefore=4, spaceAfter=4),
        "important": ParagraphStyle("important", **base,
            fontSize=9, fontName="Helvetica-Bold", textColor=C_ORANGE,
            leftIndent=12, spaceBefore=4, spaceAfter=4),
        "screenshot": ParagraphStyle("screenshot", **base,
            fontSize=8.5, fontName="Helvetica-Oblique", textColor=C_DKGRAY,
            alignment=TA_CENTER, spaceBefore=4, spaceAfter=8),
        "caption": ParagraphStyle("caption", **base,
            fontSize=8, textColor=C_DKGRAY, alignment=TA_CENTER),
        "toc_title": ParagraphStyle("toc_title", **base,
            fontSize=11, fontName="Helvetica-Bold", textColor=C_NAVY,
            spaceAfter=3),
        "toc_item": ParagraphStyle("toc_item", **base,
            fontSize=9.5, leftIndent=12, spaceAfter=2),
        "toc_sub": ParagraphStyle("toc_sub", **base,
            fontSize=9, leftIndent=28, spaceAfter=1, textColor=C_DKGRAY),
    }
    return styles


def section_header(title, s, w):
    """Returns a blue left-bar section header block."""
    bar_data = [[Paragraph(title, s["h1"])]]
    bar = Table(bar_data, colWidths=[w])
    bar.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("LINEAFTER", (0, 0), (0, -1), 0, C_WHITE),
        ("LINEBEFORE", (0, 0), (0, 0), 4, C_BLUE),
        ("BACKGROUND", (0, 0), (-1, -1), C_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return bar


def screenshot_box(label, s, w):
    """Placeholder box for screenshot."""
    data = [[Paragraph(f"[ ESPACIO PARA CAPTURA DE PANTALLA — {label} ]", s["screenshot"])]]
    t = Table(data, colWidths=[w])
    t.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.8, C_RULE),
        ("BACKGROUND", (0, 0), (-1, -1), C_GRAY),
        ("TOPPADDING", (0, 0), (-1, -1), 18),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 18),
    ]))
    return t


def note_box(text, s, w, kind="note"):
    color = C_GREEN if kind == "note" else C_ORANGE
    label = "NOTA" if kind == "note" else "IMPORTANTE"
    icon_style = ParagraphStyle("icon", fontSize=9, fontName="Helvetica-Bold",
        textColor=color, leading=13)
    body_style = ParagraphStyle("nbody", fontSize=9,
        fontName="Helvetica-Oblique" if kind == "note" else "Helvetica",
        textColor=HexColor("#1E293B"), leading=13)
    data = [[Paragraph(f"[{label}]", icon_style),
             Paragraph(text, body_style)]]
    t = Table(data, colWidths=[1.8 * cm, w - 1.8 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), HexColor("#F0FDF4") if kind == "note" else HexColor("#FFF7ED")),
        ("LINEBEFORE", (0, 0), (0, 0), 3, color),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (0, -1), 8),
        ("LEFTPADDING", (1, 0), (1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return t


def step_table(num, title, body_paragraphs, s, w):
    """Numbered step row."""
    num_cell = Paragraph(str(num), ParagraphStyle("sn",
        fontSize=14, fontName="Helvetica-Bold", textColor=C_WHITE,
        alignment=TA_CENTER, leading=18))
    title_p = Paragraph(title, ParagraphStyle("st",
        fontSize=10, fontName="Helvetica-Bold", textColor=C_NAVY, leading=14))
    content = [title_p] + body_paragraphs
    data = [[num_cell, content]]
    t = Table(data, colWidths=[1.0 * cm, w - 1.0 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), C_BLUE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (0, -1), 4),
        ("LEFTPADDING", (1, 0), (1, -1), 10),
        ("ROUNDEDCORNERS", [4, 4, 4, 4]),
    ]))
    return t


# ── TOC ─────────────────────────────────────────────────────────
def toc_section(s, w):
    elements = []
    elements.append(section_header("ÍNDICE DE CONTENIDOS", s, w))
    elements.append(Spacer(1, 0.4 * cm))

    toc_entries = [
        ("1.", "Ficha Técnica y Portada", None),
        ("2.", "Control de Acceso — Módulo de Login", [
            ("2.1", "Pantalla de Inicio de Sesión"),
            ("2.2", "Autenticación y Segmentación por Rol (JWT)"),
        ]),
        ("3.", "Capítulo I — Flujo de Autoservicio (Trabajador)", [
            ("3.1", "Paso 1: Autenticación con Rol Trabajador"),
            ("3.2", "Paso 2: Menú Principal"),
            ("3.3", "Paso 3: Selección de Artículos"),
            ("3.4", "Paso 4: Configuración del Carrito"),
            ("3.5", "Paso 5: Generación del Código QR Dinámico"),
            ("3.6", "Paso 6: Interacción en Almacén"),
        ]),
        ("4.", "Capítulo II — Flujo Asistido / Manual (Almacenero)", [
            ("4.1", "Paso 1: Autenticación con Rol Almacenero"),
            ("4.2", "Paso 2: Opción Préstamo Manual"),
            ("4.3", "Paso 3: Catálogo de Equipos"),
            ("4.4", "Paso 4: Carrito Exclusivo del Almacenero"),
            ("4.5", "Paso 5: Vinculación del Personal"),
            ("4.6", "Paso 6: Resumen, Firma y Cierre"),
        ]),
        ("5.", "Glosario de Estados del Sistema", None),
        ("6.", "Control de Cambios del Documento", None),
    ]

    for num, title, subs in toc_entries:
        row = [[Paragraph(num, s["toc_item"]), Paragraph(title, s["toc_title"])]]
        t = Table(row, colWidths=[1 * cm, w - 1 * cm])
        t.setStyle(TableStyle([
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
            ("LINEBELOW", (0, 0), (-1, -1), 0.3, C_RULE),
        ]))
        elements.append(t)
        if subs:
            for s_num, s_title in subs:
                row2 = [[Paragraph(s_num, s["toc_sub"]), Paragraph(s_title, s["toc_sub"])]]
                t2 = Table(row2, colWidths=[1.2 * cm, w - 1.2 * cm])
                t2.setStyle(TableStyle([
                    ("TOPPADDING", (0, 0), (-1, -1), 1),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
                ]))
                elements.append(t2)
    elements.append(PageBreak())
    return elements


# ── LOGIN SECTION ────────────────────────────────────────────────
def login_section(s, w):
    elements = []
    elements.append(section_header("CONTROL DE ACCESO — MÓDULO DE LOGIN", s, w))
    elements.append(Spacer(1, 0.3 * cm))

    elements.append(Paragraph("2.1  Pantalla de Inicio de Sesión", s["h2"]))
    elements.append(Paragraph(
        "Al ejecutar la aplicación RamisToolX en el dispositivo móvil, el sistema presenta "
        "inmediatamente la pantalla de inicio de sesión. Esta pantalla es única y común para "
        "todos los usuarios del sistema, independientemente del rol que tengan asignado.",
        s["body"]))
    elements.append(Spacer(1, 0.2 * cm))
    elements.append(screenshot_box("Pantalla de Login — Ingreso de Credenciales", s, w))
    elements.append(Spacer(1, 0.3 * cm))

    elements.append(Paragraph("Componentes de la pantalla de login:", s["h3"]))
    bullets = [
        "Campo <b>Usuario:</b> Ingrese el nombre de usuario o correo electrónico corporativo registrado en el sistema.",
        "Campo <b>Contraseña:</b> Ingrese la contraseña asignada. Los caracteres se ocultarán automáticamente durante la escritura.",
        "Botón <b>Iniciar Sesión:</b> Envía las credenciales al servidor para su validación.",
        "Enlace <b>¿Olvidaste tu contraseña?:</b> Permite iniciar el proceso de recuperación de acceso (contactar al administrador del sistema).",
    ]
    for b in bullets:
        elements.append(Paragraph(f"• {b}", s["bullet"]))

    elements.append(Spacer(1, 0.3 * cm))
    elements.append(Paragraph("2.2  Autenticación y Segmentación por Rol (JWT)", s["h2"]))
    elements.append(Paragraph(
        "Una vez que el usuario presiona el botón Iniciar Sesión, el sistema ejecuta el siguiente "
        "proceso de autenticación de manera transparente y automática:",
        s["body"]))

    auth_steps = [
        ("Envío de Credenciales",
         "La aplicación envía de forma segura el usuario y la contraseña al servidor de autenticación "
         "(API REST — FastAPI). La comunicación viaja cifrada mediante el protocolo HTTPS."),
        ("Validación en el Servidor",
         "El backend consulta la base de datos PostgreSQL para verificar que las credenciales "
         "ingresadas correspondan a un usuario activo y registrado en el sistema."),
        ("Emisión del Token JWT",
         "Si las credenciales son válidas, el servidor genera y devuelve un Token de Seguridad "
         "(JSON Web Token — JWT). Este token contiene, entre otros datos, el Rol del usuario "
         "(TRABAJADOR o ALMACENERO), garantizando que la sesión esté firmada y sea infalsificable."),
        ("Segmentación de Interfaz",
         "La aplicación lee el Rol contenido en el JWT y redirige automáticamente al usuario "
         "a su Dashboard correspondiente. Un Trabajador verá el menú de autoservicio; un Almacenero "
         "verá el panel de gestión completo, con opciones exclusivas de su rol."),
    ]
    for i, (title, body) in enumerate(auth_steps, 1):
        bp = [Paragraph(body, ParagraphStyle("sb", fontSize=9.5, textColor=C_DKGRAY,
                fontName="Helvetica", leading=14, spaceAfter=4))]
        elements.append(Spacer(1, 0.15 * cm))
        elements.append(step_table(i, title, bp, s, w))

    elements.append(Spacer(1, 0.3 * cm))
    elements.append(note_box(
        "Si el usuario o la contraseña son incorrectos, el sistema mostrará un mensaje de error "
        "en pantalla. Tras tres (3) intentos fallidos consecutivos, la cuenta podrá quedar bloqueada "
        "temporalmente. Contacte al administrador del sistema para desbloquearla.",
        s, w, "important"))

    elements.append(Spacer(1, 0.4 * cm))

    # Role table
    elements.append(Paragraph("Cuadro Resumen de Roles del Sistema", s["h3"]))
    role_data = [
        ["ROL", "ACCESO OTORGADO", "RESTRICCIÓN"],
        ["Trabajador", "Menú de Autoservicio:\nGenerar Préstamo\nDevolver Equipos",
         "No puede gestionar préstamos de terceros\nNo accede al catálogo administrativo"],
        ["Almacenero", "Panel Completo:\nPréstamo Manual\nAprobación de pedidos\nGestión de stock",
         "Acceso total al sistema con\ntrazabilidad completa de operaciones"],
    ]
    rt = Table(role_data, colWidths=[3.2 * cm, (w - 3.2 * cm) / 2, (w - 3.2 * cm) / 2])
    rt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), C_NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), C_WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [C_WHITE, C_GRAY]),
        ("GRID", (0, 0), (-1, -1), 0.4, C_RULE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
        ("TEXTCOLOR", (0, 1), (0, -1), C_BLUE),
    ]))
    elements.append(rt)
    elements.append(PageBreak())
    return elements


# ── CHAPTER I ───────────────────────────────────────────────────
def chapter1(s, w):
    elements = []

    # Chapter banner
    banner_data = [["CAPÍTULO I", "FLUJO DE AUTOSERVICIO\nPara trabajadores que conocen y utilizan la aplicación"]]
    bt = Table(banner_data, colWidths=[3.2 * cm, w - 3.2 * cm])
    bt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), C_BLUE),
        ("BACKGROUND", (1, 0), (1, -1), C_NAVY),
        ("TEXTCOLOR", (0, 0), (-1, -1), C_WHITE),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (0, -1), 11),
        ("FONTSIZE", (1, 0), (1, -1), 10),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("LEFTPADDING", (0, 0), (0, -1), 10),
        ("LEFTPADDING", (1, 0), (1, -1), 14),
        ("LEADING", (1, 0), (1, -1), 16),
    ]))
    elements.append(bt)
    elements.append(Spacer(1, 0.4 * cm))

    intro_text = (
        "El Flujo de Autoservicio permite que un Trabajador gestione de forma autónoma su solicitud "
        "de préstamo de herramientas y equipos directamente desde su dispositivo móvil, sin necesidad "
        "de la intervención del Almacenero durante la fase de creación del pedido. La interacción con "
        "el Almacén se produce únicamente al momento del despacho físico, mediante la validación de un "
        "Código QR dinámico."
    )
    elements.append(Paragraph(intro_text, s["body"]))
    elements.append(Spacer(1, 0.3 * cm))

    # STEP 1
    elements.append(Paragraph("PASO 1 — Autenticación con Rol de Trabajador", s["h2"]))
    elements.append(Paragraph(
        "El Trabajador abre la aplicación RamisToolX en su dispositivo móvil e ingresa sus credenciales "
        "corporativas (usuario y contraseña) en la pantalla de Login. El sistema valida las credenciales "
        "contra el servidor y, al identificar el Rol de <b>TRABAJADOR</b>, redirige automáticamente al "
        "Dashboard del Trabajador.", s["body"]))
    elements.append(screenshot_box("Dashboard del Trabajador — Vista Principal", s, w))
    elements.append(note_box(
        "El token JWT emitido en el inicio de sesión tiene una vigencia limitada. Si la sesión expira, "
        "el sistema solicitará al usuario que vuelva a autenticarse para garantizar la seguridad de las operaciones.",
        s, w, "note"))
    elements.append(Spacer(1, 0.3 * cm))

    # STEP 2
    elements.append(Paragraph("PASO 2 — Navegación en el Menú Principal", s["h2"]))
    elements.append(Paragraph(
        "Tras el inicio de sesión exitoso, el sistema muestra el Menú Principal del Trabajador con "
        "las siguientes opciones disponibles:", s["body"]))
    menu_data = [
        ["OPCIÓN", "DESCRIPCIÓN"],
        ["Generar Préstamo", "Inicia el proceso de solicitud de herramientas o equipos. "
         "El trabajador selecciona los artículos, configura el carrito y genera el QR para el despacho."],
        ["Devolver Equipos", "Permite registrar la devolución de herramientas previamente prestadas. "
         "El trabajador escanea o selecciona el préstamo activo para iniciar el proceso de devolución."],
    ]
    mt = Table(menu_data, colWidths=[3.8 * cm, w - 3.8 * cm])
    mt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), C_NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), C_WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [C_WHITE, C_GRAY]),
        ("GRID", (0, 0), (-1, -1), 0.4, C_RULE),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
        ("TEXTCOLOR", (0, 1), (0, -1), C_BLUE),
    ]))
    elements.append(mt)
    elements.append(Spacer(1, 0.2 * cm))
    elements.append(screenshot_box("Menú Principal del Trabajador — Opciones Disponibles", s, w))
    elements.append(Spacer(1, 0.3 * cm))

    # STEP 3
    elements.append(Paragraph("PASO 3 — Selección de Artículos", s["h2"]))
    elements.append(Paragraph(
        "Al seleccionar la opción <b>Generar Préstamo</b>, el sistema despliega el catálogo completo "
        "de herramientas y equipos disponibles en el almacén. El catálogo muestra en tiempo real "
        "únicamente los artículos con stock disponible, consultando directamente la base de datos PostgreSQL.",
        s["body"]))
    elements.append(Spacer(1, 0.15 * cm))

    cat_steps = [
        "Navegue por el catálogo desplazándose verticalmente en la pantalla. Los artículos se presentan con nombre, descripción, imagen referencial y cantidad disponible en stock.",
        "Utilice la <b>barra de búsqueda</b> (si está disponible) para filtrar artículos por nombre o categoría.",
        "Presione el botón <b>'+'</b> ubicado junto a cada artículo para agregarlo a su carrito y definir la cantidad solicitada. Cada toque incrementa la cantidad en una (1) unidad.",
        "Presione el botón <b>'−'</b> para reducir la cantidad o eliminar el artículo del carrito.",
        "El contador del carrito, visible en la parte superior de la pantalla, se actualiza automáticamente mostrando el número total de ítems seleccionados.",
    ]
    for b in cat_steps:
        elements.append(Paragraph(f"• {b}", s["bullet"]))

    elements.append(Spacer(1, 0.2 * cm))
    elements.append(screenshot_box("Catálogo de Artículos — Selección con Botones '+' y '−'", s, w))
    elements.append(note_box(
        "El sistema no permite solicitar una cantidad de artículos superior al stock disponible. "
        "Si se intenta agregar más unidades de las disponibles, el botón '+' se bloqueará automáticamente "
        "y se mostrará un aviso de stock insuficiente.",
        s, w, "important"))
    elements.append(Spacer(1, 0.3 * cm))

    # STEP 4
    elements.append(Paragraph("PASO 4 — Configuración del Carrito de Compras", s["h2"]))
    elements.append(Paragraph(
        "Una vez que el Trabajador ha seleccionado todos los artículos requeridos, accede al "
        "<b>Carrito de Compras</b> para revisar y configurar su solicitud antes de enviarla.",
        s["body"]))

    cart_items = [
        "<b>Revisión de ítems:</b> Se muestra la lista completa de artículos seleccionados con su nombre, cantidad solicitada y la cantidad disponible en stock. El trabajador puede ajustar cantidades o eliminar ítems en esta vista.",
        "<b>Selección de Fecha Límite de Devolución:</b> El sistema presenta un componente de calendario interactivo. El Trabajador debe seleccionar obligatoriamente la fecha en que compromete la devolución de los equipos. No es posible avanzar sin definir esta fecha.",
        "<b>Resumen del Pedido:</b> Al pie de la pantalla se muestra un resumen consolidado con el total de artículos y la fecha de devolución comprometida.",
        "<b>Botón 'Generar Solicitud':</b> Finaliza la configuración del carrito y dispara el proceso de generación del código QR.",
    ]
    for item in cart_items:
        elements.append(Paragraph(f"• {item}", s["bullet"]))

    elements.append(Spacer(1, 0.2 * cm))
    elements.append(screenshot_box("Carrito de Compras — Revisión de Ítems y Calendario de Devolución", s, w))
    elements.append(note_box(
        "La fecha límite de devolución es un campo obligatorio del sistema. La selección de una fecha "
        "pasada no está permitida; el calendario sólo habilitará fechas a partir del día siguiente al actual.",
        s, w, "important"))
    elements.append(Spacer(1, 0.3 * cm))

    # STEP 5
    elements.append(Paragraph("PASO 5 — Generación del Código QR Dinámico", s["h2"]))
    elements.append(Paragraph(
        "Al confirmar el carrito, la aplicación envía la solicitud de préstamo al servidor (FastAPI). "
        "El backend procesa la petición, registra el pedido en la base de datos PostgreSQL con el "
        "estado inicial <b>PENDIENTE_APROBACION</b> y devuelve el identificador único del pedido (ID). "
        "Con dicho ID, la aplicación genera y dibuja en pantalla un <b>Código QR Dinámico</b>.",
        s["body"]))

    elements.append(Spacer(1, 0.15 * cm))
    qr_bullets = [
        "El QR generado es <b>único e irrepetible</b> para cada solicitud. Contiene el ID interno del pedido en la base de datos.",
        "El código QR es válido únicamente mientras el pedido se encuentre en estado <b>PENDIENTE_APROBACION</b>.",
        "El QR se despliega en pantalla completa para facilitar su lectura por parte del Almacenero.",
        "El trabajador <b>no debe cerrar</b> esta pantalla hasta que el Almacenero haya escaneado y procesado exitosamente el pedido.",
    ]
    for b in qr_bullets:
        elements.append(Paragraph(f"• {b}", s["bullet"]))

    elements.append(Spacer(1, 0.2 * cm))
    elements.append(screenshot_box("Pantalla del Código QR Dinámico — Estado: PENDIENTE_APROBACION", s, w))
    elements.append(note_box(
        "El stock de los artículos solicitados NO se descuenta del inventario en este paso. "
        "El descuento efectivo del stock sólo ocurre cuando el Almacenero aprueba y procesa "
        "el despacho en el siguiente paso, garantizando consistencia en el inventario.",
        s, w, "important"))
    elements.append(Spacer(1, 0.3 * cm))

    # STEP 6
    elements.append(Paragraph("PASO 6 — Interacción en Almacén (Despacho con QR)", s["h2"]))
    elements.append(Paragraph(
        "Con la pantalla del QR visible en el dispositivo del Trabajador, ambos se dirigen al punto "
        "de despacho. El Almacenero opera con su propio dispositivo móvil para completar el proceso:",
        s["body"]))

    dispatch_steps = [
        ("Escaneo del Código QR",
         "El Almacenero abre la función de escaneo en su aplicación y apunta la cámara del dispositivo "
         "hacia el QR mostrado en la pantalla del Trabajador. El sistema lee el ID del pedido "
         "contenido en el código."),
        ("Visualización del Resumen del Pedido",
         "De forma automática, la app del Almacenero consulta la API y despliega el resumen completo "
         "del pedido: nombre del trabajador solicitante, lista de artículos con cantidades, "
         "fecha límite de devolución y estado actual del pedido (PENDIENTE_APROBACION)."),
        ("Verificación Física",
         "El Almacenero coteja físicamente los artículos del pedido con lo mostrado en pantalla, "
         "asegurándose de que cada ítem y cantidad sea correcta antes de continuar."),
        ("Captura de Firma Digital Manuscrita",
         "El sistema solicita la firma de conformidad del Trabajador. El Trabajador traza su firma "
         "directamente sobre la pantalla táctil del dispositivo móvil del Almacenero. "
         "Esta firma queda almacenada como evidencia digital vinculada al registro del préstamo."),
        ("Procesamiento del Despacho",
         "El Almacenero presiona el botón <b>'Confirmar Despacho'</b>. El sistema actualiza "
         "el estado del pedido a <b>ENTREGADO</b> en la base de datos PostgreSQL, descuenta "
         "las cantidades del stock de inventario de cada artículo y genera el registro definitivo "
         "del préstamo con fecha, hora y firma adjunta."),
    ]
    for i, (title, body) in enumerate(dispatch_steps, 1):
        bp = [Paragraph(body, ParagraphStyle("sb2", fontSize=9.5, textColor=C_DKGRAY,
                fontName="Helvetica", leading=14, spaceAfter=4))]
        elements.append(Spacer(1, 0.12 * cm))
        elements.append(step_table(i, title, bp, s, w))

    elements.append(Spacer(1, 0.3 * cm))
    elements.append(screenshot_box("Almacenero — Resumen del Pedido tras Escaneo del QR", s, w))
    elements.append(Spacer(1, 0.15 * cm))
    elements.append(screenshot_box("Captura de Firma Digital Manuscrita del Trabajador", s, w))
    elements.append(Spacer(1, 0.3 * cm))
    elements.append(note_box(
        "Una vez que el estado cambia a ENTREGADO, el stock en la base de datos PostgreSQL se actualiza "
        "de manera inmediata y permanente. Esta operación es irreversible sin la intervención de un "
        "Administrador del Sistema. El registro del préstamo queda disponible para auditoría.",
        s, w, "important"))

    elements.append(PageBreak())
    return elements


# ── CHAPTER II ──────────────────────────────────────────────────
def chapter2(s, w):
    elements = []

    banner_data = [["CAPÍTULO II", "FLUJO ASISTIDO / MANUAL\nPara trabajadores que NO utilizan la aplicación móvil"]]
    bt = Table(banner_data, colWidths=[3.2 * cm, w - 3.2 * cm])
    bt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), C_ORANGE),
        ("BACKGROUND", (1, 0), (1, -1), C_NAVY),
        ("TEXTCOLOR", (0, 0), (-1, -1), C_WHITE),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (0, -1), 11),
        ("FONTSIZE", (1, 0), (1, -1), 10),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("LEFTPADDING", (0, 0), (0, -1), 10),
        ("LEFTPADDING", (1, 0), (1, -1), 14),
        ("LEADING", (1, 0), (1, -1), 16),
    ]))
    elements.append(bt)
    elements.append(Spacer(1, 0.4 * cm))

    intro = (
        "El Flujo Asistido o Manual está diseñado para aquellos casos en que el Trabajador no cuenta "
        "con la aplicación instalada en su dispositivo móvil, no dispone de conectividad, o simplemente "
        "prefiere solicitar las herramientas de forma presencial en el área de almacén. En este flujo, "
        "el <b>Almacenero</b> gestiona la totalidad del proceso desde su propio dispositivo, incluyendo "
        "la selección de artículos, la vinculación del trabajador responsable y la captura de su firma digital."
    )
    elements.append(Paragraph(intro, s["body"]))
    elements.append(Spacer(1, 0.3 * cm))

    # STEP 1
    elements.append(Paragraph("PASO 1 — Autenticación con Rol de Almacenero", s["h2"]))
    elements.append(Paragraph(
        "El Almacenero abre la aplicación RamisToolX en su dispositivo móvil e ingresa sus credenciales "
        "corporativas. El sistema, al verificar el Rol <b>ALMACENERO</b> en el token JWT, redirige "
        "automáticamente al Dashboard del Almacenero, el cual presenta opciones de gestión avanzadas "
        "no disponibles para el Rol Trabajador.", s["body"]))
    elements.append(Spacer(1, 0.2 * cm))
    elements.append(screenshot_box("Dashboard del Almacenero — Panel de Gestión Completo", s, w))
    elements.append(Spacer(1, 0.3 * cm))

    # STEP 2
    elements.append(Paragraph("PASO 2 — Selección de la Opción 'Préstamo Manual'", s["h2"]))
    elements.append(Paragraph(
        "En el menú exclusivo del Almacenero se muestra la opción <b>'Préstamo Manual'</b>. "
        "Esta opción es visible <b>única y exclusivamente</b> para usuarios con Rol Almacenero "
        "y no aparece en la interfaz del Trabajador.", s["body"]))

    elements.append(Spacer(1, 0.15 * cm))
    elements.append(Paragraph("Opciones exclusivas del panel del Almacenero:", s["h3"]))
    almacenero_opts = [
        "<b>Préstamo Manual:</b> Inicia la gestión de un préstamo en representación de un trabajador que solicita herramientas de forma presencial.",
        "<b>Aprobar Pedidos:</b> Lista los pedidos con estado PENDIENTE_APROBACION generados por los trabajadores mediante QR.",
        "<b>Gestión de Stock:</b> Visualización y control del inventario en tiempo real.",
        "<b>Historial de Operaciones:</b> Registro completo y trazable de todos los préstamos y devoluciones.",
    ]
    for b in almacenero_opts:
        elements.append(Paragraph(f"• {b}", s["bullet"]))

    elements.append(Spacer(1, 0.2 * cm))
    elements.append(screenshot_box("Menú del Almacenero — Opciones Exclusivas por Rol", s, w))
    elements.append(Spacer(1, 0.3 * cm))

    # STEP 3
    elements.append(Paragraph("PASO 3 — Navegación del Catálogo de Equipos", s["h2"]))
    elements.append(Paragraph(
        "Al seleccionar <b>Préstamo Manual</b>, el sistema despliega el mismo catálogo de herramientas "
        "y equipos disponibles en el almacén. El Almacenero navega por el catálogo y registra "
        "digitalmente los artículos que el Trabajador solicita de forma presencial y verbal.",
        s["body"]))
    elements.append(Spacer(1, 0.15 * cm))

    cat3_bullets = [
        "El catálogo muestra todos los artículos disponibles con nombre, descripción y stock actual.",
        "Utilice los botones <b>'+'</b> y <b>'−'</b> para definir las cantidades de cada artículo solicitado por el Trabajador.",
        "El sistema valida en tiempo real que la cantidad solicitada no supere el stock disponible.",
        "Una vez seleccionados todos los artículos, el Almacenero accede al carrito para continuar.",
    ]
    for b in cat3_bullets:
        elements.append(Paragraph(f"• {b}", s["bullet"]))

    elements.append(Spacer(1, 0.2 * cm))
    elements.append(screenshot_box("Catálogo de Equipos — Vista del Almacenero (Préstamo Manual)", s, w))
    elements.append(Spacer(1, 0.3 * cm))

    # STEP 4
    elements.append(Paragraph("PASO 4 — Configuración del Carrito Exclusivo del Almacenero", s["h2"]))
    elements.append(Paragraph(
        "En el Carrito de Compras del flujo manual se habilita dinámicamente una funcionalidad "
        "exclusiva del Rol Almacenero: el botón especial <b>'Seleccionar Trabajador'</b>. "
        "Este botón NO aparece en el carrito del flujo de autoservicio del Trabajador.",
        s["body"]))

    cart4_items = [
        "<b>Revisión de ítems seleccionados:</b> Lista de artículos con nombre y cantidad solicitada.",
        "<b>Selección de Fecha Límite de Devolución:</b> El Almacenero define, en coordinación con el Trabajador, la fecha de devolución comprometida mediante el componente de calendario.",
        "<b>Botón 'Seleccionar Trabajador' (Exclusivo):</b> Botón habilitado dinámicamente por el sistema al detectar el Rol Almacenero en el token JWT. Permite vincular el préstamo al Trabajador responsable.",
    ]
    for item in cart4_items:
        elements.append(Paragraph(f"• {item}", s["bullet"]))

    elements.append(Spacer(1, 0.2 * cm))
    elements.append(screenshot_box("Carrito Exclusivo del Almacenero — Botón 'Seleccionar Trabajador' Habilitado", s, w))
    elements.append(note_box(
        "El botón 'Seleccionar Trabajador' se habilita de forma dinámica por la lógica de la aplicación "
        "al verificar el Rol del token JWT activo. Su presencia garantiza que ningún préstamo manual "
        "quede sin responsable asignado en la base de datos.",
        s, w, "note"))
    elements.append(Spacer(1, 0.3 * cm))

    # STEP 5
    elements.append(Paragraph("PASO 5 — Vinculación del Personal Responsable", s["h2"]))
    elements.append(Paragraph(
        "Al presionar el botón <b>'Seleccionar Trabajador'</b>, el sistema abre un módulo de "
        "búsqueda que consulta el directorio de personal registrado en la base de datos PostgreSQL.",
        s["body"]))

    link_steps = [
        ("Búsqueda del Trabajador",
         "El Almacenero puede buscar al trabajador por nombre, apellido o número de empleado "
         "utilizando la barra de búsqueda del módulo. La lista de resultados se filtra en tiempo real."),
        ("Selección del Responsable",
         "El Almacenero selecciona al trabajador correcto de la lista de resultados. "
         "El sistema muestra los datos del trabajador (nombre completo, área o departamento, DNI o código "
         "de empleado) para confirmación antes de vincularlo al pedido."),
        ("Vinculación Confirmada",
         "Una vez seleccionado, el nombre del trabajador responsable aparece en el resumen del carrito. "
         "A partir de este momento, el préstamo queda formalmente asociado al trabajador seleccionado "
         "en la base de datos y en todos los reportes del sistema."),
    ]
    for i, (title, body) in enumerate(link_steps, 1):
        bp = [Paragraph(body, ParagraphStyle("sb3", fontSize=9.5, textColor=C_DKGRAY,
                fontName="Helvetica", leading=14, spaceAfter=4))]
        elements.append(Spacer(1, 0.12 * cm))
        elements.append(step_table(i, title, bp, s, w))

    elements.append(Spacer(1, 0.2 * cm))
    elements.append(screenshot_box("Módulo de Búsqueda y Selección de Trabajador", s, w))
    elements.append(Spacer(1, 0.3 * cm))

    # STEP 6
    elements.append(Paragraph("PASO 6 — Resumen, Firma Digital y Cierre del Préstamo", s["h2"]))
    elements.append(Paragraph(
        "Con el carrito configurado y el trabajador vinculado, el sistema presenta el "
        "<b>Resumen Total del Préstamo</b> antes de la confirmación definitiva. "
        "Este paso es el cierre formal de la operación.",
        s["body"]))

    close_steps = [
        ("Visualización del Resumen Total",
         "La pantalla muestra el detalle completo y definitivo del préstamo: nombre del trabajador "
         "responsable, lista de artículos con cantidades, fecha límite de devolución y el total de ítems."),
        ("Captura de la Firma Digital Manuscrita",
         "El Almacenero entrega el dispositivo móvil al Trabajador. "
         "El Trabajador traza su firma manuscrita directamente sobre la pantalla táctil del dispositivo, "
         "en el área de firma habilitada. Esta firma constituye la constancia digital de conformidad "
         "y aceptación de los términos del préstamo."),
        ("Confirmación y Generación del Préstamo",
         "El Almacenero presiona el botón <b>'Confirmar y Generar Préstamo'</b>. "
         "El sistema registra el préstamo en la base de datos PostgreSQL con el estado <b>ASIGNADO</b>, "
         "descuenta las cantidades de stock de cada artículo de forma inmediata y permanente, "
         "y genera el registro definitivo con fecha, hora, firma y datos del trabajador responsable."),
        ("Confirmación Visual en Pantalla",
         "El sistema muestra un mensaje de éxito confirmando la generación del préstamo, "
         "el número de pedido asignado y los datos del registro. El Almacenero puede optar por "
         "consultar el historial de operaciones para verificar el registro."),
    ]
    for i, (title, body) in enumerate(close_steps, 1):
        bp = [Paragraph(body, ParagraphStyle("sb4", fontSize=9.5, textColor=C_DKGRAY,
                fontName="Helvetica", leading=14, spaceAfter=4))]
        elements.append(Spacer(1, 0.12 * cm))
        elements.append(step_table(i, title, bp, s, w))

    elements.append(Spacer(1, 0.3 * cm))
    elements.append(screenshot_box("Resumen Total del Préstamo Manual — Vista Previa antes de Confirmar", s, w))
    elements.append(Spacer(1, 0.15 * cm))
    elements.append(screenshot_box("Área de Firma Digital Manuscrita del Trabajador", s, w))
    elements.append(Spacer(1, 0.15 * cm))
    elements.append(screenshot_box("Pantalla de Confirmación — Préstamo Generado (Estado: ASIGNADO)", s, w))
    elements.append(Spacer(1, 0.3 * cm))

    elements.append(note_box(
        "Al confirmar el préstamo, el stock en PostgreSQL se actualiza de manera inmediata e irreversible. "
        "El sistema no permite registrar un préstamo si alguno de los artículos seleccionados no cuenta "
        "con stock suficiente al momento de la confirmación, garantizando la integridad del inventario "
        "en todo momento.",
        s, w, "important"))

    elements.append(PageBreak())
    return elements


# ── GLOSSARY ────────────────────────────────────────────────────
def glossary_section(s, w):
    elements = []
    elements.append(section_header("GLOSARIO DE ESTADOS DEL SISTEMA", s, w))
    elements.append(Spacer(1, 0.3 * cm))
    elements.append(Paragraph(
        "La siguiente tabla describe los estados posibles que puede tomar un préstamo dentro del "
        "ciclo de vida del Sistema RamisToolX (OCS):", s["body"]))
    elements.append(Spacer(1, 0.2 * cm))

    states = [
        ["ESTADO", "DESCRIPCIÓN", "¿AFECTA STOCK?", "FLUJO"],
        ["PENDIENTE_\nAPROBACION",
         "El Trabajador ha generado la solicitud y obtenido el QR. "
         "El pedido aguarda el escaneo y aprobación del Almacenero.",
         "NO", "Autoservicio"],
        ["ENTREGADO",
         "El Almacenero procesó el despacho tras escanear el QR y "
         "capturar la firma del Trabajador. Las herramientas han sido entregadas físicamente.",
         "SÍ — Descuento", "Autoservicio"],
        ["ASIGNADO",
         "El Almacenero registró el préstamo de forma manual (Flujo Asistido) "
         "y las herramientas han sido entregadas. El stock fue descontado al confirmar.",
         "SÍ — Descuento", "Manual"],
        ["DEVUELTO",
         "El Trabajador ha devuelto las herramientas al almacén y el Almacenero "
         "ha registrado la devolución en el sistema. El stock es repuesto.",
         "SÍ — Reposición", "Ambos"],
        ["CANCELADO",
         "El pedido fue anulado antes de ser procesado. "
         "No generó movimiento de stock.",
         "NO", "Ambos"],
    ]
    col_w = [3.2 * cm, (w - 7.4 * cm), 2.8 * cm, 2.4 * cm]
    st_table = Table(states, colWidths=col_w)
    st_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), C_NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), C_WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [C_WHITE, C_GRAY]),
        ("GRID", (0, 0), (-1, -1), 0.4, C_RULE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
        ("TEXTCOLOR", (0, 1), (0, -1), C_BLUE),
        ("ALIGN", (2, 0), (2, -1), "CENTER"),
        ("ALIGN", (3, 0), (3, -1), "CENTER"),
    ]))
    elements.append(st_table)
    elements.append(PageBreak())
    return elements


# ── CHANGE LOG ──────────────────────────────────────────────────
def changelog_section(s, w):
    elements = []
    elements.append(section_header("CONTROL DE CAMBIOS DEL DOCUMENTO", s, w))
    elements.append(Spacer(1, 0.3 * cm))

    log_data = [
        ["VERSIÓN", "FECHA", "AUTOR", "DESCRIPCIÓN DEL CAMBIO"],
        ["1.0.0", "Junio 2026", "Team Orbit", "Emisión inicial del Manual de Usuario Oficial del Sistema RamisToolX (OCS)."],
        ["", "", "", ""],
        ["", "", "", ""],
    ]
    cl = Table(log_data, colWidths=[2.2 * cm, 2.8 * cm, 3.5 * cm, w - 8.5 * cm])
    cl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), C_NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), C_WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [C_WHITE, C_GRAY]),
        ("GRID", (0, 0), (-1, -1), 0.4, C_RULE),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("ALIGN", (0, 0), (1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    elements.append(cl)
    elements.append(Spacer(1, 1 * cm))

    sign_data = [
        ["ELABORADO POR", "REVISADO POR", "APROBADO POR"],
        ["\n\n\n\n___________________________\nTeam Orbit\nDesarrollo de Software\n2026",
         "\n\n\n\n___________________________\nJefatura de Operaciones\nCorporación Ramis S.A.C.\n2026",
         "\n\n\n\n___________________________\nGerencia General\nCorporación Ramis S.A.C.\n2026"],
    ]
    sign_w = (w) / 3
    st2 = Table(sign_data, colWidths=[sign_w, sign_w, sign_w])
    st2.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), C_NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), C_WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.4, C_RULE),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 1), (-1, -1), "BOTTOM"),
        ("FONTSIZE", (0, 1), (-1, -1), 8.5),
        ("TEXTCOLOR", (0, 1), (-1, -1), C_DKGRAY),
    ]))
    elements.append(st2)
    return elements


# ── MAIN ────────────────────────────────────────────────────────
def build_pdf():
    output = "/mnt/user-data/outputs/Manual_RamisToolX_OCS.pdf"
    doc = SimpleDocTemplate(
        output,
        pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=1.8 * cm, bottomMargin=1.5 * cm,
        title="Manual de Usuario — RamisToolX (Sistema OCS)",
        author="Team Orbit",
        subject="Manual de Usuario Oficial",
    )

    s = get_styles()
    w = PAGE_W - 2 * MARGIN

    story = []
    story += cover_page()
    story += toc_section(s, w)
    story += login_section(s, w)
    story += chapter1(s, w)
    story += chapter2(s, w)
    story += glossary_section(s, w)
    story += changelog_section(s, w)

    doc.build(story, onFirstPage=make_page_template, onLaterPages=make_page_template)
    print(f"PDF generado: {output}")

build_pdf()