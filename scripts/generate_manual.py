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
            "Este documento funciona como guia de consulta para analistas del Area de TI de Distribuidora ADD. Reune procedimientos operativos frecuentes reportados por usuarios y los pasos esperados de validacion o resolucion.",
            "El objetivo es que, ante un mensaje como un usuario dice que no funciona su impresora, un usuario no puede conectarse a la VPN, una parte de la oficina quedo sin Internet o un usuario no abre una carpeta compartida, el equipo de soporte pueda consultar rapidamente los pasos a seguir.",
            "Los datos tecnicos incluidos en este documento son demostrativos. Las URLs, IPs, nombres de servidores, rutas y correos fueron reemplazados por valores ficticios para evitar exponer informacion real de infraestructura.",
        ],
    ),
    (
        "2. Acceso a carpetas compartidas, sistemas y red",
        [
            "Si un usuario informa que no abre una carpeta compartida o no accede a un sistema interno, primero se debe validar si esta dentro de la red de la empresa o trabajando desde fuera. Si esta fuera de la empresa, se debe confirmar que la VPN se encuentre conectada. Si esta dentro de la oficina, se debe verificar que el equipo tenga conexion a la red y a Internet.",
            "Luego se debe revisar la configuracion de red de la interfaz activa. En Windows, ingresar a Panel de control, Conexiones de red, seleccionar la placa activa y validar los DNS configurados. Como ejemplo ficticio, el DNS primario puede ser 10.50.2.10 y el secundario 10.50.2.11.",
            "Si el usuario continua sin acceder al recurso, se debe identificar si el problema ocurre con una sola carpeta, con varias carpetas o con todo acceso a red. Si falla solo una carpeta, revisar permisos del recurso. Si fallan varias carpetas o sistemas, revisar conectividad, DNS, autenticacion de dominio y estado de la VPN si corresponde.",
        ],
    ),
    (
        "3. Sin Internet en un sector de la oficina",
        [
            "Si uno o varios usuarios informan que no hay Internet en una parte especifica de la oficina, primero se debe identificar si el problema afecta a un solo equipo, a varios equipos, a un area completa, solo a la red Wi-Fi o solo a equipos conectados por cable.",
            "El analista debe ingresar al controlador UniFi ficticio https://unifi.empresa-ejemplo.local y verificar que los switches y puntos de acceso del sector figuren encendidos, conectados y sin alertas criticas. Si un switch o AP aparece desconectado, se debe revisar energia electrica, patchera, cable de red y puerto de uplink antes de continuar.",
            "Luego se debe revisar el servidor DHCP y confirmar que el pool de direcciones no haya llegado al limite de leases disponibles. Tambien se debe verificar que rango IP esta recibiendo el equipo afectado, porque cada tipo de conexion tiene un rango asignado.",
            "Como referencia demostrativa, la red Wi-Fi corporativa debe entregar direcciones del rango 10.50.6.0/24, la red Wi-Fi de invitados debe entregar direcciones del rango 10.50.5.0/24, los usuarios conectados por cable deben recibir direcciones del rango 10.50.3.0/24 y el rango 10.50.2.0/24 queda reservado para impresoras, switches, APs y servidores.",
            "Si el equipo recibe una IP fuera del rango esperado, se debe revisar la VLAN configurada en el puerto del switch o en el SSID correspondiente. Si no recibe ninguna IP, renovar la direccion IP del equipo, probar otro puerto o red Wi-Fi y validar si el problema proviene del DHCP, del switch, del AP o del equipo del usuario.",
        ],
    ),
    (
        "4. Contraseña de correo corporativo",
        [
            "Si un usuario olvida la contraseña del correo corporativo, debe existir un ticket previo o una solicitud formal registrada. El analista de TI debe restablecer la contraseña desde la consola administrativa ficticia https://admin.correo.empresa-ejemplo.local.",
            "En la consola, ingresar a Usuarios, seleccionar la cuenta del colaborador, elegir Restablecer contraseña, asignar una contraseña temporal y marcar que el usuario debe cambiarla en el siguiente inicio de sesion.",
            "Luego se responde el ticket con la contraseña temporal y se aclara que el sistema solicitara un cambio obligatorio al volver a ingresar. No se deben registrar contraseñas definitivas en comentarios publicos ni en documentos compartidos.",
            "Si despues del cambio el usuario indica que no puede iniciar sesion o que no recibe correos, se debe revisar el estado de la cuenta, bloqueo, licenciamiento, dispositivos conectados y acceso a la red antes de escalar el caso.",
        ],
    ),
    (
        "5. Contraseña de SGI",
        [
            "Si un usuario olvida la contraseña del sistema SGI, soporte debe indicarle que ingrese a la pantalla de acceso del sistema y seleccione la opcion Olvide mi contrasena.",
            "El sistema enviara automaticamente una contraseña temporal al correo corporativo del usuario. Con esa contraseña temporal, el usuario puede volver a ingresar al SGI y definir una nueva contraseña antes de continuar.",
            "Si el usuario no recibe el correo de recuperacion, primero se debe revisar el acceso al correo corporativo, la bandeja de spam o correo no deseado y el estado de la cuenta. Si el correo funciona correctamente y aun asi no llega la recuperacion, se debe derivar el caso al administrador funcional del SGI.",
        ],
    ),
    (
        "6. Impresoras y perifericos",
        [
            "Si un usuario informa que no funciona una impresora, primero se debe identificar la impresora correcta, el sector donde esta ubicada y su direccion IP en el inventario o planilla compartida ficticia de Informatica.",
            "Luego se debe hacer ping a la IP de la impresora. Si responde, se puede quitar la impresora del equipo del usuario y volver a instalarla utilizando los drivers almacenados en la ruta ficticia \\\\fileserver-ejemplo\\informatica\\drivers\\impresoras.",
            "Si la impresora no responde al ping, se debe revisar energia electrica, cable de red, puerto del switch, estado del display, atasco de papel y toner. Si la impresora usa Wi-Fi, validar que siga conectada al SSID correspondiente.",
            "Si el problema afecta solo a un usuario, revisar cola de impresion, impresora predeterminada, driver instalado y permisos. Si afecta a varios usuarios, revisar conectividad de la impresora, servicio de impresion del servidor y estado general del equipo.",
        ],
    ),
    (
        "7. VPN y trabajo remoto",
        [
            "Si un usuario informa que no funciona la VPN, primero se debe validar que tenga Internet, que la fecha y hora del equipo sean correctas y que el cliente VPN se encuentre abierto. Luego reiniciar el cliente VPN y volver a probar la conexion.",
            "Si persiste el error, registrar el codigo o mensaje mostrado por el cliente VPN y confirmar que el usuario este usando sus credenciales de dominio en el formato definido por la empresa, por ejemplo nombre.apellido.",
            "Si se requiere reprovisionar la VPN, TI puede ingresar al portal ficticio https://vpn.empresa-ejemplo.local:4443 con credenciales autorizadas, descargar el archivo de configuracion correspondiente y cargarlo nuevamente en el cliente VPN del equipo administrado.",
            "La VPN corporativa se utiliza solo desde equipos administrados por la empresa. Si un usuario solicita configurarla en un equipo personal, soporte debe indicar que no corresponde realizar la configuracion sin autorizacion formal.",
        ],
    ),
]


TOOLS_SECTIONS = [
    (
        "1. Alcance del documento",
        [
            "Este documento complementa los casos operativos de soporte TI con procedimientos administrativos y tecnicos de uso interno. Sirve para consultar tareas de administracion, comandos, configuraciones y controles periodicos del area.",
            "La base esta pensada exclusivamente para analistas del Area de TI. No debe compartirse con usuarios finales ni utilizarse como repositorio de credenciales.",
            "Los nombres de servidores, rutas, URLs, IPs, correos y ejemplos tecnicos son ficticios y se usan solo para demostrar el funcionamiento del asistente interno.",
        ],
    ),
    (
        "2. Alta de usuario nuevo",
        [
            "El alta de usuario debe iniciarse mediante una solicitud formal o ticket del area responsable, por ejemplo Gente y Gestion del Talento. La solicitud debe incluir nombre y apellido, codigo de colaborador si corresponde, cargo, sector, sucursal o deposito, fecha de ingreso y sistemas requeridos.",
            "Con la solicitud registrada, TI crea el usuario en los sistemas necesarios, como dominio, correo corporativo y SGI. Para el dominio se debe seguir el formato de usuario definido por la empresa, por ejemplo nombre.apellido, y asignar los grupos correspondientes al sector o funcion.",
            "Luego se genera una contraseña temporal y se marca el cambio obligatorio en el primer inicio de sesion cuando el sistema lo permita. Las credenciales deben entregarse por un canal autorizado y no deben quedar publicadas en documentos compartidos.",
            "Para el alta en SGI u otro sistema interno, se registra la informacion en el formulario ABM ficticio FOR-INF-03_ABM_de_Usuarios o en la herramienta equivalente definida por TI. Al finalizar, se responde el ticket indicando los accesos creados y cualquier aclaracion necesaria para el primer ingreso.",
        ],
    ),
    (
        "3. Modificacion de usuario",
        [
            "La modificacion de usuario se realiza cuando cambia el sector, cargo, rol, sucursal o conjunto de permisos de un colaborador. Debe existir una solicitud formal o ticket indicando los cambios requeridos.",
            "Antes de aplicar cambios, TI debe validar que la solicitud detalle que accesos se agregan, modifican o retiran. Si la descripcion es incompleta, se debe pedir aclaracion al solicitante antes de modificar permisos.",
            "Luego se actualizan los grupos del dominio, permisos de carpetas, correo, SGI y otros sistemas internos que correspondan. En cambios de sector, tambien se debe revisar si corresponde quitar accesos anteriores para evitar acumulacion innecesaria de permisos.",
            "Para modificaciones en SGI u otro sistema controlado por ABM, se registra el cambio en el formulario ficticio FOR-INF-03_ABM_de_Usuarios o en la herramienta equivalente. Al finalizar, se responde el ticket con el detalle de los accesos modificados.",
        ],
    ),
    (
        "4. Baja de usuario",
        [
            "La baja de usuario debe iniciarse mediante solicitud formal o ticket del area responsable. La solicitud debe incluir datos del colaborador, fecha de baja, sistemas involucrados y si el usuario tenia acceso a informacion sensible o confidencial.",
            "Con la solicitud registrada, TI deshabilita o bloquea los accesos del usuario en dominio, correo corporativo, SGI, VPN y otros sistemas internos. Cuando sea necesario conservar informacion, no se debe eliminar contenido sin validar previamente el periodo de retencion definido.",
            "Si el usuario tenia equipo asignado, se debe coordinar la recuperacion de notebook, cargador, celular, token, accesorios u otros activos. El estado de los equipos recuperados debe actualizarse en Snipe-IT o en la herramienta de inventario correspondiente.",
            "Para bajas en SGI u otro sistema controlado por ABM, se registra la informacion en el formulario ficticio FOR-INF-03_ABM_de_Usuarios o herramienta equivalente. Al finalizar, se responde el ticket confirmando la baja o inhabilitacion de accesos.",
        ],
    ),
    (
        "5. Control de backups",
        [
            "El control de backups consiste en revisar que las copias programadas de servidores, aplicaciones, bases de datos o rutas criticas se hayan ejecutado correctamente. La verificacion puede realizarse desde la consola de backup ficticia https://backup.empresa-ejemplo.local o desde las notificaciones enviadas por correo.",
            "Como referencia demostrativa, los servidores pueden estar registrados con nombres ficticios como SRV-DC-01, SRV-DC-02, SRV-APP-01, SRV-FILES-01, SRV-SGI-01 y SRV-LAB-01. No deben documentarse nombres reales de servidores en esta base.",
            "Para cada job se debe verificar estado, hora de inicio, hora de finalizacion, duracion, tamaño transferido y mensaje de resultado. Si el backup finalizo correctamente, se deja constancia en el registro operativo definido por TI.",
            "Si un backup falla, se debe revisar la causa probable: falta de espacio, servidor apagado, credenciales vencidas, error de red, repositorio no disponible o servicio detenido. Luego se aplica la correccion correspondiente y se aguarda la siguiente copia programada o se ejecuta una copia manual si corresponde.",
            "Una vez restablecido el proceso, se registra el evento en una planilla ficticia de control, por ejemplo FOR-INF-01_Eventos_Datacenter, ubicada en una ruta de ejemplo como \\\\fileserver-ejemplo\\informatica\\auditoria.",
        ],
    ),
    (
        "6. Restauracion de informacion",
        [
            "La restauracion de informacion debe realizarse a partir de una solicitud formal o por una prueba periodica definida por TI. Antes de restaurar, se debe identificar servidor, carpeta, base de datos, fecha aproximada del respaldo requerido y motivo de la restauracion.",
            "No se debe restaurar informacion directamente sobre produccion sin validacion previa. Cuando sea posible, la restauracion debe realizarse primero en una ruta segura o ambiente de prueba, por ejemplo \\\\fileserver-ejemplo\\restore\\solicitud-0001.",
            "Despues de restaurar, se debe validar que los archivos, carpetas o datos recuperados correspondan a la fecha solicitada. El solicitante debe confirmar que la informacion restaurada es la correcta antes de cerrar la tarea.",
            "Las pruebas periodicas de restauracion deben dejar evidencia en el registro operativo definido por TI, por ejemplo FOR-INF-01_Eventos_Datacenter. La evidencia puede incluir fecha, servidor o ruta restaurada, responsable, resultado y observaciones.",
        ],
    ),
    (
        "7. Inventario de equipos en Snipe-IT",
        [
            "Cuando se adquiere o recibe un equipo informatico, TI debe registrarlo en Snipe-IT o en la herramienta de gestion de activos definida. El registro debe incluir tipo de equipo, marca, modelo, numero de serie, estado, ubicacion, usuario asignado y observaciones relevantes.",
            "Para obtener el numero de serie de una notebook desde PowerShell, se puede ejecutar el comando Get-WmiObject win32_bios | Select-Object SerialNumber. El resultado se utiliza para inventario, garantia o validacion del equipo.",
            "Si el equipo cambia de usuario, sector o ubicacion, se debe actualizar el activo en Snipe-IT. La informacion del inventario debe mantenerse alineada con la ubicacion real del equipo para facilitar auditorias, soporte y control de garantias.",
            "Al menos una vez al año se recomienda verificar los equipos registrados para confirmar ubicacion, usuario asignado y estado. Si se detectan diferencias, se actualiza el registro del activo y se deja observacion del cambio realizado.",
        ],
    ),
    (
        "8. Mantenimiento preventivo de equipos",
        [
            "El mantenimiento preventivo se ejecuta segun el calendario anual definido por TI. Antes de iniciar, se debe coordinar con el usuario para evitar interrumpir tareas operativas y confirmar disponibilidad del equipo.",
            "Durante el mantenimiento se revisa el estado general del equipo, limpieza externa, espacio en disco, rendimiento, actualizaciones pendientes, antivirus o proteccion instalada, estado de bateria si aplica, perifericos y funcionamiento basico de red.",
            "Si durante la revision se detecta un problema, se registra como mantenimiento correctivo en Snipe-IT o en la herramienta definida, dejando evidencia de la incidencia, acciones realizadas, fecha y responsable.",
            "Los servidores se programan de forma diferenciada a los equipos de usuarios. Para equipos nuevos que cuentan con garantia, los mantenimientos pueden programarse una vez finalizado el periodo de garantia, segun el criterio definido por TI.",
            "Si por ausencia del usuario, imprevisto o fuerza mayor no se puede ejecutar el mantenimiento en la fecha prevista, se debe reprogramar con el usuario involucrado y dejar constancia en el registro del activo.",
        ],
    ),
    (
        "9. Consolas de administracion y reseteos",
        [
            "Para restablecer la contraseña del correo corporativo, TI debe ingresar a la consola ficticia https://admin.correo.empresa-ejemplo.local, ir a Usuarios, seleccionar Restablecer contraseña, asignar una contraseña temporal y marcar que en el siguiente inicio de sesion el usuario deba cambiarla.",
            "Para conectarse a Exchange Online desde PowerShell en una sesion de soporte, primero se debe permitir la ejecucion solo para esa sesion con Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force. Luego se importa el modulo ExchangeOnlineManagement y se ejecuta Connect-ExchangeOnline con una cuenta administrativa autorizada de ejemplo.",
            "Si se requiere reprovisionar VPN, TI puede ingresar al portal ficticio https://vpn.empresa-ejemplo.local:4443 con credenciales autorizadas y descargar el archivo de configuracion correspondiente.",
        ],
    ),
    (
        "10. Equipos y sistema operativo",
        [
            "Si se necesita iniciar sesion en un equipo nuevo con cuenta local de Windows 11 durante la configuracion inicial, se puede abrir la consola con Shift + F10 y ejecutar start ms-cxh:localonly para habilitar el flujo de cuenta local.",
            "Si se requiere renovar el periodo de gracia de Escritorio Remoto en un Windows Server de laboratorio, se debe abrir regedit como administrador y navegar hasta HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server\\RCM\\GracePeriod. Luego se elimina la clave que comienza con L$RTMTIMEBOMB y se reinicia el servicio si corresponde.",
            "Los cambios sobre servidores o configuraciones de sistema operativo deben realizarse con autorizacion interna y deben quedar documentados en el ticket o registro operativo correspondiente.",
        ],
    ),
    (
        "11. Dominio, GPO y configuracion corporativa",
        [
            "Para cambiar un fondo corporativo o una configuracion masiva de escritorio, se debe revisar la GPO correspondiente en el controlador de dominio ficticio SRV-DC-01, dentro de la consola de administracion de directivas de grupo.",
            "Antes de aplicar una GPO a toda la empresa, se recomienda probarla en una unidad organizativa de prueba o con un grupo reducido de equipos. Luego de validar el resultado, se puede ampliar el alcance segun autorizacion interna.",
            "Todo cambio con impacto masivo en dominio, correo, red, VPN o escritorio remoto debe quedar documentado en ticket o bitacora operativa del Area de TI.",
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
            [
                ["Version", "1.1"],
                ["Vigencia", "Julio de 2026"],
                ["Clasificacion", "Uso interno demostrativo"],
            ],
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

# Regenerar PDFs:
# ./.venv/bin/python scripts/generate_manual.py
