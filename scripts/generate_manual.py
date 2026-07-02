from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
CASES_OUTPUT = DATA_DIR / "casos_operativos_soporte_ti_add.pdf"
TOOLS_OUTPUT = DATA_DIR / "herramientas_y_administracion_ti_add.pdf"

CASES_SECTIONS = [
    (
        "1. Alcance del documento",
        [
            "Este documento funciona como guia de consulta para analistas del Area de TI de Distribuidora ADD. Reune casos operativos frecuentes reportados por usuarios y los pasos esperados de validacion o resolucion.",
            "El objetivo es que, ante un mensaje como un usuario dice que no funciona su impresora o un usuario se olvido su contraseña del correo, el equipo de soporte pueda consultar rapidamente los pasos a seguir.",
            "La Mesa de Ayuda atiende de lunes a viernes, de 07:30 a 17:30. Los sabados se cubren incidentes operativos de deposito y facturacion de 08:00 a 12:00. Fuera de ese horario solo se gestionan incidentes criticos mediante el numero de guardia +595 981 000 120.",
        ],
    ),
    (
        "2. Casos de acceso a carpetas, sistemas y red",
        [
            "Si un usuario informa que no abre una carpeta compartida o no accede al sistema, primero se debe validar si esta fuera de la empresa o dentro de la red interna. Si esta fuera, verificar que se encuentre conectado a la VPN. Si esta dentro, verificar que tenga conexion a Internet.",
            "Luego se debe ingresar a Panel de control, Conexiones, y revisar la configuracion de DNS de la interfaz activa. En la conexion por cable de red o en la de Wi-Fi, segun corresponda, la direccion DNS primaria debe ser 192.0.2.4 y como secundaria debe figurar 198.51.100.136 o 203.0.113.8.",
            "Si el usuario continua sin acceder al recurso, se debe validar si el problema ocurre con una sola carpeta, con varias o con todo acceso a red. Esa distincion define si se revisan permisos, conectividad o autenticacion.",
        ],
    ),
    (
        "3. Casos de contraseña de correo",
        [
            "Si un usuario olvida la contraseña del correo corporativo, debe existir un ticket previo o una solicitud formal registrada. El analista de TI debe restablecer la contraseña desde la consola administrativa, asignar una contraseña temporal y marcar que el usuario debe cambiarla en el siguiente inicio de sesion.",
            "Luego se responde el ticket con la contraseña temporal y se aclara que el sistema solicitara un cambio obligatorio al volver a ingresar.",
            "Si el usuario reporta que no recibe correos o no puede iniciar sesion despues del cambio, se debe validar el estado de la cuenta, licenciamiento y dispositivos conectados antes de escalar.",
        ],
    ),
    (
        "4. Casos de contraseña de SGI",
        [
            "Si un usuario olvida la contraseña del sistema SGI, soporte debe indicarle que ingrese a la pantalla de acceso del sistema y seleccione la opcion Olvide mi contrasena. El sistema enviara automaticamente por correo una contrasena temporal.",
            "La contrasena temporal de SGI permite volver a ingresar al sistema y obliga a definir una nueva contraseña antes de continuar.",
            "Si el usuario no recibe el correo de recuperacion, se debe revisar primero el acceso al correo antes de escalar el caso a administracion funcional de SGI.",
        ],
    ),
    (
        "5. Casos de impresoras y perifericos",
        [
            "Si Nathaly o cualquier usuario indica que no funciona una impresora, primero se debe identificar la impresora correcta y verificar su direccion IP en el archivo Excel de la compartida de Informatica.",
            "Luego se debe hacer ping a la IP de la impresora. Si responde, se puede desinstalar la impresora del equipo del usuario y volver a instalarla utilizando los drivers que se encuentran organizados por impresora en la compartida.",
            "Si la impresora no responde al ping, se debe validar alimentacion, red fisica y estado del equipo antes de escalar a infraestructura o proveedor.",
        ],
    ),
    (
        "6. Casos de VPN y trabajo remoto",
        [
            "Si un usuario informa que no funciona la VPN, primero se debe validar Internet, fecha y hora del equipo y reiniciar Sophos Connect. Si persiste, registrar el codigo de error y confirmar que utilice su usuario de dominio en formato nombre.apellido junto con la misma contraseña con la que inicia sesion en su notebook.",
            "Si la VPN requiere reprovision, TI puede ingresar a 198.51.100.252:4443 con las credenciales de dominio del usuario, descargar el archivo .ovpn correspondiente y ejecutarlo en la notebook del usuario para volver a configurar la conexion.",
            "La VPN corporativa se utiliza exclusivamente desde equipos administrados por Distribuidora ADD. Si un usuario consulta por equipos personales, soporte debe indicar que no esta permitido salvo autorizacion formal y uso del acceso web aprobado.",
        ],
    ),
    (
        "7. Apertura y calidad de tickets",
        [
            "La plataforma interna de tickets se encuentra en http://192.0.2.7:8081/ticket/scp/login.php. Si la persona se encuentra fuera de la oficina, primero debe conectarse a la VPN para poder ingresar.",
            "Todo ticket debe incluir nombre, sector, sucursal o deposito afectado, equipo o sistema involucrado, descripcion del problema, hora aproximada de inicio, mensaje de error y foto o captura cuando sea posible. Nunca deben adjuntarse contraseñas.",
            "La prioridad P1 corresponde a una interrupcion total del ERP, del sistema de facturacion, de la red principal o de la operacion de picking y despacho. La prioridad P2 corresponde a una afectacion importante para caja, ventas, deposito o una sucursal completa. P3 se usa para incidentes individuales con alternativa temporal y P4 para solicitudes planificadas.",
        ],
    ),
]

TOOLS_SECTIONS = [
    (
        "1. Alcance del documento",
        [
            "Este documento complementa los casos operativos del soporte TI con procedimientos administrativos y tecnicos de uso interno. Sirve para consultar comandos, accesos de administracion y tareas puntuales del area.",
            "Esta base esta pensada exclusivamente para analistas del Area de TI y no debe compartirse con usuarios finales.",
        ],
    ),
    (
        "2. Consolas de administracion y reseteos",
        [
            "Para restablecer la contraseña del correo corporativo, TI debe ingresar a https://admin.correo.distribuidoraadd.example/, ir a Usuarios, seleccionar Restablecer contraseña, asignar una contraseña generica y marcar que en el siguiente inicio de sesion el usuario deba cambiarla.",
            "Para conectarse a Exchange Online desde PowerShell en una sesion de soporte, primero se debe permitir la ejecucion solo para esa sesion con Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force, luego forzar TLS 1.2, importar el modulo ExchangeOnlineManagement y finalmente ejecutar Connect-ExchangeOnline -UserPrincipalName soporte.ti@distribuidoraadd.example -DisableWAM.",
            "Si se requiere reprovisionar VPN, TI puede ingresar a 198.51.100.252:4443 con credenciales de dominio del usuario y descargar el archivo .ovpn correspondiente.",
        ],
    ),
    (
        "3. Equipos y sistema operativo",
        [
            "Para verificar el numero de serie de una notebook desde PowerShell, se debe ejecutar el comando Get-WmiObject win32_bios | Select-Object SerialNumber. El resultado se utiliza para inventario, garantia o validacion del equipo.",
            "Si se necesita iniciar sesion en un equipo nuevo con cuenta local de Windows 11 durante la configuracion inicial, se debe abrir la consola con Shift + F10 y ejecutar start ms-cxh:localonly para habilitar el flujo de cuenta local.",
            "Si se requiere renovar el periodo de gracia de Escritorio Remoto en un Windows Server, se debe abrir regedit como administrador y navegar hasta HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server\\RCM\\GracePeriod. Luego se elimina la clave que comienza con L$RTMTIMEBOMB y se intenta reiniciar el servicio con Restart-Service TermService -Force.",
        ],
    ),
    (
        "4. Dominio, GPO y configuracion corporativa",
        [
            "Para cambiar el fondo corporativo de toda la empresa, se debe revisar la GPO Fondo Corporativo 26 en el controlador de dominio de ejemplo 192.0.2.4, dentro de la administracion de directivas de grupo, siguiendo la ruta Configuracion de usuario, Preferencias y Configuracion de Windows.",
            "Las modificaciones de politica corporativa deben registrarse y validarse en una ventana de cambio antes de aplicarse a toda la empresa.",
            "Todo cambio con impacto masivo en dominio, correo, red o escritorio remoto debe quedar documentado en ticket y, si corresponde, en bitacora operativa del Area de TI.",
        ],
    ),
]


def footer(canvas, document) -> None:
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#52606D"))
    canvas.drawString(2 * cm, 1.2 * cm, "Distribuidora ADD - Documento interno demostrativo")
    canvas.drawRightString(19 * cm, 1.2 * cm, f"Pagina {document.page}")
    canvas.restoreState()


def build_pdf(output: Path, title: str, sections: list[tuple[str, list[str]]]) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(output),
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        title=title,
        author="Paulo Renato Preda",
    )
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="CoverTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=27,
            leading=33,
            textColor=colors.HexColor("#123B5D"),
            alignment=TA_CENTER,
            spaceAfter=18,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SectionTitle",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=17,
            leading=21,
            textColor=colors.HexColor("#123B5D"),
            spaceAfter=14,
        )
    )
    body = ParagraphStyle(
        name="ManualBody",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=16,
        textColor=colors.HexColor("#243B53"),
        spaceAfter=12,
    )

    story = [
        Spacer(1, 4.5 * cm),
        Paragraph(title.upper(), styles["CoverTitle"]),
        Paragraph("Distribuidora ADD", styles["Heading2"]),
        Spacer(1, 0.8 * cm),
        Table(
            [["Version", "1.0"], ["Vigencia", "Julio de 2026"], ["Clasificacion", "Uso interno demostrativo"]],
            colWidths=[4 * cm, 7 * cm],
            style=TableStyle(
                [
                    ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#EAF2F8")),
                    ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#243B53")),
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#BCCCDC")),
                    ("PADDING", (0, 0), (-1, -1), 9),
                ]
            ),
        ),
        Spacer(1, 1.5 * cm),
        Paragraph(
            "Documento ficticio inspirado en el contexto operativo de una importadora y distribuidora. Fue creado exclusivamente como fuente de conocimiento para el Challenge Alura Agente.",
            body,
        ),
        PageBreak(),
    ]

    for index, (section_title, paragraphs) in enumerate(sections):
        story.append(Paragraph(section_title, styles["SectionTitle"]))
        for paragraph in paragraphs:
            story.append(Paragraph(paragraph, body))
        if index < len(sections) - 1:
            story.append(PageBreak())

    doc.build(story, onFirstPage=footer, onLaterPages=footer)


def build_manuals() -> None:
    build_pdf(CASES_OUTPUT, "Casos Operativos de Soporte TI", CASES_SECTIONS)
    build_pdf(TOOLS_OUTPUT, "Herramientas y Administracion TI", TOOLS_SECTIONS)


if __name__ == "__main__":
    build_manuals()
    print(f"PDF generado: {CASES_OUTPUT}")
    print(f"PDF generado: {TOOLS_OUTPUT}")
# Regenerar pdf's: ./.venv/bin/python scripts/generate_manual.py
