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
OUTPUT = ROOT / "data" / "procedimientos_y_guias_soporte_ti_distribuidora_add.pdf"

SECTIONS = [
    (
        "1. Objetivo y alcance",
        [
            "Este documento establece los procedimientos del Area de TI de Distribuidora ADD y funciona como base operativa de consulta para el equipo de soporte. Reune indicaciones para atencion a usuarios, gestion de accesos y resolucion de incidentes frecuentes.",
            "Aplica a personal administrativo, fuerza de ventas, deposito, logistica y sucursales que utilizan equipos, cuentas, sistemas o conectividad provistos por la empresa.",
            "La Mesa de Ayuda atiende de lunes a viernes, de 07:30 a 17:30. Los sabados se cubren incidentes operativos de deposito y facturacion de 08:00 a 12:00. Fuera de ese horario solo se gestionan incidentes criticos mediante el numero de guardia +595 981 000 120.",
            "Los canales oficiales son el correo soporte.ti@distribuidoraadd.example y el interno 120. Los pedidos enviados por WhatsApp personal o por mensajes informales no se registran como tickets.",
        ],
    ),
    (
        "2. Registro y prioridad de tickets",
        [
            "La plataforma interna de tickets se encuentra en http://192.0.2.7:8081/ticket/scp/login.php. Si la persona se encuentra fuera de la oficina, primero debe conectarse a la VPN para poder ingresar.",
            "El formato de acceso a la plataforma es Usuario A.nombre.apellido y contrasena inicial nombre.apellido. La contrasena puede cambiarse posteriormente desde la configuracion del sistema.",
            "Para crear un ticket se debe ingresar a la opcion Nuevo Ticket, buscar al usuario correcto y completar los datos de seguimiento. En el campo CC se pueden agregar correos para dar visibilidad y en Aviso de Ticket debe quedar la opcion Alertar a todos.",
            "Todo ticket debe incluir nombre, sector, sucursal o deposito afectado, equipo o sistema involucrado, descripcion del problema, hora aproximada de inicio, mensaje de error y foto o captura cuando sea posible. Nunca deben adjuntarse contraseñas.",
            "En la carga del ticket se debe dejar Fuente del Ticket en Email, seleccionar el tema de ayuda correspondiente, elegir el departamento TI y completar resumen, descripcion, prioridad y adjuntos antes de hacer clic en Abrir.",
            "La prioridad P1 corresponde a una interrupcion total del ERP, del sistema de facturacion, de la red principal o de la operacion de picking y despacho. El tiempo objetivo de primera respuesta es 15 minutos y la actualizacion se realiza cada 30 minutos.",
            "La prioridad P2 corresponde a una afectacion importante para caja, ventas, deposito o una sucursal completa, con primera respuesta en 1 hora. P3 corresponde a incidentes individuales con alternativa temporal, con respuesta en 4 horas habiles. P4 se usa para solicitudes planificadas, con respuesta en 1 dia habil.",
            "La prioridad es validada por la Mesa de Ayuda. Marcar todos los casos como urgentes no acelera su atencion y puede dificultar la gestion de incidentes realmente criticos.",
        ],
    ),
    (
        "3. Contraseñas y cuentas",
        [
            "Si una persona olvida la contraseña de su correo corporativo, debe abrir un ticket en la plataforma interna de TI. La solicitud debe indicar nombre del usuario, area, problema detectado y un medio alternativo de contacto. El restablecimiento no se gestiona por WhatsApp ni por pedido verbal.",
            "Si una persona olvida la contraseña del sistema SGI, debe ingresar a la pantalla de acceso del sistema y seleccionar la opcion Olvide mi contrasena. El sistema enviara automaticamente por correo una contrasena temporal.",
            "La contrasena temporal de SGI permite volver a ingresar al sistema. Al acceder con esa contrasena temporal, el sistema solicita obligatoriamente definir una nueva contrasena antes de continuar.",
            "Si la persona no puede recibir el correo de recuperacion de SGI, debe abrir un ticket para revision del acceso o del correo asociado. El tecnico verificara identidad mediante nombre completo, numero de colaborador, CI y validacion con su responsable. Soporte nunca solicita la contraseña anterior.",
            "Una cuenta se bloquea despues de cinco intentos fallidos. El bloqueo automatico dura 20 minutos. Si el acceso es urgente, la Mesa de Ayuda puede desbloquearla despues de validar la identidad.",
            "Las contraseñas deben tener al menos 12 caracteres e incluir mayuscula, minuscula, numero y simbolo. No se permite reutilizar ninguna de las ultimas ocho contraseñas ni compartir credenciales.",
        ],
    ),
    (
        "4. Solicitud de accesos",
        [
            "El acceso a carpetas compartidas, impresoras de red, ERP, sistema de preventa o tableros de stock se solicita mediante el formulario de Accesos. Debe indicarse el recurso, el nivel requerido, la justificacion laboral y la fecha de finalizacion cuando sea temporal.",
            "La solicitud requiere aprobacion del responsable directo y del propietario del proceso. Para modulos de tesoreria, costos o cuentas corrientes tambien se necesita aprobacion de Gerencia Administrativa. Soporte no concede accesos basandose solamente en un correo informal.",
            "Los accesos temporales vencen en la fecha indicada. Las revisiones de permisos se realizan trimestralmente y los privilegios que ya no tengan justificacion son retirados.",
        ],
    ),
    (
        "5. Software y equipos",
        [
            "El software debe solicitarse al Area de TI. Solo pueden instalarse aplicaciones aprobadas y con licencia vigente. La persona usuaria no debe desactivar el antivirus ni utilizar instaladores descargados desde sitios no oficiales.",
            "Las solicitudes de notebook, monitor, lector de codigo, impresora termica o accesorios requieren aprobacion del responsable del area. El plazo normal de preparacion es de tres dias habiles si existe stock. Todo equipo entregado queda asociado a la persona responsable en el inventario.",
            "En caso de perdida o robo, se debe avisar inmediatamente a Seguridad, RRHH y a la Mesa de Ayuda. Soporte bloqueara la cuenta, revocara sesiones y activara el borrado remoto cuando el equipo lo permita. Tambien se debe realizar la denuncia correspondiente dentro de las 24 horas.",
        ],
    ),
    (
        "6. Conexion remota y VPN",
        [
            "La VPN corporativa se utiliza exclusivamente desde equipos administrados por Distribuidora ADD. Para conectarse, la persona debe abrir Sophos Connect e ingresar con su usuario de dominio en formato nombre.apellido y la misma contraseña con la que inicia sesion en su notebook.",
            "Si la VPN no conecta, primero debe verificar Internet, confirmar que la fecha y hora del equipo sean correctas y reiniciar el cliente Sophos Connect. Si el error continua, debe registrar el codigo mostrado y abrir un ticket. No se deben instalar clientes VPN alternativos.",
            "La sesion VPN se desconecta despues de 30 minutos de inactividad. Esta medida es automatica y no puede ser deshabilitada por la Mesa de Ayuda.",
        ],
    ),
    (
        "7. Correo y amenazas",
        [
            "Un correo sospechoso debe reportarse con el boton Reportar phishing de Outlook. No se debe responder, descargar adjuntos ni abrir enlaces. El equipo de TI analizara el mensaje y comunicara las medidas necesarias.",
            "Si la persona ya ingreso sus credenciales en un sitio sospechoso, debe desconectar el equipo de la red, llamar inmediatamente a la Mesa de Ayuda y cambiar la contraseña desde otro dispositivo seguro.",
            "Los archivos con informacion confidencial se comparten unicamente mediante los repositorios corporativos autorizados. No deben enviarse a cuentas personales ni almacenarse en servicios gratuitos de nube.",
        ],
    ),
    (
        "8. Escalamiento y cierre",
        [
            "Un ticket se escala al segundo nivel cuando requiere permisos especializados, cambios de infraestructura o cuando el procedimiento de primer nivel no resuelve el incidente. Los casos de seguridad se derivan de inmediato al equipo de Seguridad de la Informacion.",
            "Antes de cerrar un ticket, Soporte registra la solucion y solicita confirmacion a la persona usuaria. Si no recibe respuesta, envia dos recordatorios en dias habiles distintos y cierra el caso al tercer dia habil. El ticket puede reabrirse durante los cinco dias posteriores.",
            "La satisfaccion puede calificarse al finalizar el ticket. Las observaciones se revisan mensualmente para mejorar los procedimientos y detectar problemas recurrentes.",
        ],
    ),
    (
        "9. Guias rapidas para soporte TI",
        [
            "Si una persona indica que no funciona una carpeta compartida o no accede al sistema, primero se debe validar si esta fuera de la empresa o dentro de la red interna. Si esta fuera, verificar que se encuentre conectada a la VPN. Si esta dentro, verificar que tenga conexion a Internet.",
            "Luego se debe ingresar a Panel de control, Conexiones, y revisar la configuracion de DNS de la interfaz activa. En la conexion por cable de red o en la de Wi-Fi, segun corresponda, la direccion DNS primaria debe ser 192.0.2.4 y como secundaria debe figurar 198.51.100.136 o 203.0.113.8.",
            "Si una persona olvida la contraseña del correo, debe abrir un ticket y TI debe ingresar a https://admin.correo.distribuidoraadd.example/, ir a Usuarios, seleccionar Restablecer contraseña, asignar una contraseña generica y marcar que en el siguiente inicio de sesion el usuario deba cambiar su contraseña. Luego se responde el ticket con la contraseña temporal e indicando que el sistema le solicitara cambiarla.",
            "Si una persona informa que no funciona la VPN, TI puede ingresar a 198.51.100.252:4443 con las credenciales de dominio del usuario, descargar el archivo .ovpn correspondiente y ejecutarlo en la notebook del usuario para volver a configurar la conexion.",
            "Si una impresora no funciona, TI debe verificar la direccion IP de la impresora en el archivo Excel ubicado en la compartida de Informatica y probar conectividad con ping. Si la impresora responde, se puede desinstalar la impresora del equipo del usuario y volver a instalarla utilizando los drivers que se encuentran organizados por impresora en la compartida.",
            "Para verificar el numero de serie de una notebook desde PowerShell, se debe ejecutar el comando Get-WmiObject win32_bios | Select-Object SerialNumber. El resultado se utiliza para inventario, garantia o validacion del equipo.",
            "Si se necesita iniciar sesion en un equipo nuevo con cuenta local de Windows 11 durante la configuracion inicial, se debe abrir la consola con Shift + F10 y ejecutar start ms-cxh:localonly para habilitar el flujo de cuenta local.",
            "Para conectarse a Exchange Online desde PowerShell en una sesion de soporte, primero se debe permitir la ejecucion solo para esa sesion con Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force, luego forzar TLS 1.2, importar el modulo ExchangeOnlineManagement y finalmente ejecutar Connect-ExchangeOnline -UserPrincipalName soporte.ti@distribuidoraadd.example -DisableWAM.",
            "Si se requiere renovar el periodo de gracia de Escritorio Remoto en un Windows Server, se debe abrir regedit como administrador y navegar hasta HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server\\RCM\\GracePeriod. Luego se elimina la clave que comienza con L$RTMTIMEBOMB y se intenta reiniciar el servicio con Restart-Service TermService -Force.",
            "Para cambiar el fondo corporativo de toda la empresa, se debe revisar la GPO Fondo Corporativo 26 en el controlador de dominio de ejemplo 192.0.2.4, dentro de la administracion de directivas de grupo, siguiendo la ruta Configuracion de usuario, Preferencias y Configuracion de Windows.",
        ],
    ),
    (
        "10. Preguntas frecuentes",
        [
            "¿Puedo prestar mi cuenta a otra persona? No. Las cuentas son personales e intransferibles.",
            "¿Soporte puede ver mi contraseña? No. Las contraseñas no son visibles para el personal tecnico y nunca se solicitan por telefono, correo o chat.",
            "¿Puedo trabajar desde una computadora personal? Solo cuando exista autorizacion formal y se utilice el acceso web aprobado. La VPN no puede instalarse en equipos personales.",
            "¿Donde consulto el estado de mi solicitud? En la seccion Mis tickets del portal, utilizando el numero recibido al crear el caso.",
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


def build_manual() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        title="Procedimientos y Guias de Soporte TI - Distribuidora ADD",
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
        Paragraph("PROCEDIMIENTOS Y GUIAS DE SOPORTE TI", styles["CoverTitle"]),
        Paragraph("Distribuidora ADD", styles["Heading2"]),
        Spacer(1, 0.8 * cm),
        Table(
            [["Version", "1.0"], ["Vigencia", "Junio de 2026"], ["Clasificacion", "Uso interno demostrativo"]],
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

    for index, (title, paragraphs) in enumerate(SECTIONS):
        story.append(Paragraph(title, styles["SectionTitle"]))
        for paragraph in paragraphs:
            story.append(Paragraph(paragraph, body))
        if index < len(SECTIONS) - 1:
            story.append(PageBreak())

    doc.build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    build_manual()
    print(f"PDF generado: {OUTPUT}")
