"""Genera el informe PDF a partir de registros y capturas reales. Requiere reportlab."""
from pathlib import Path
import json,xml.etree.ElementTree as ET
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,Image,PageBreak,KeepTogether
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from xml.sax.saxutils import escape
P=Path(__file__).resolve().parents[1]; E=P/'evidencias'; C=E/'pantallazos'
for name,file in [('Arial','Arial.ttf'),('Arial-Bold','Arial Bold.ttf')]:
    font=Path('/System/Library/Fonts/Supplemental')/file
    if font.exists():pdfmetrics.registerFont(TTFont(name,str(font)))
F='Arial' if 'Arial' in pdfmetrics.getRegisteredFontNames() else 'Helvetica'
B='Arial-Bold' if F=='Arial' else 'Helvetica-Bold'
pdfmetrics.registerFontFamily(F,normal=F,bold=B)
navy=colors.HexColor('#142c45');teal=colors.HexColor('#127367');grey=colors.HexColor('#50667a');light=colors.HexColor('#eef3f7')
s=getSampleStyleSheet()
s.add(ParagraphStyle(name='TitleX',fontName=B,fontSize=30,leading=35,textColor=navy,spaceAfter=15))
s.add(ParagraphStyle(name='H',fontName=B,fontSize=19,leading=23,textColor=navy,spaceAfter=12))
s.add(ParagraphStyle(name='Sub',fontName=B,fontSize=12,leading=16,textColor=teal,spaceBefore=11,spaceAfter=7))
s.add(ParagraphStyle(name='BodyX',fontName=F,fontSize=10.1,leading=14.5,textColor=navy,spaceAfter=8))
s.add(ParagraphStyle(name='SmallX',fontName=F,fontSize=8.4,leading=11.5,textColor=grey,spaceAfter=7))
s.add(ParagraphStyle(name='CellX',fontName=F,fontSize=9,leading=12,textColor=navy))
s.add(ParagraphStyle(name='CellHead',fontName=B,fontSize=9,leading=12,textColor=colors.white))
s.add(ParagraphStyle(name='CodeX',fontName='Courier',fontSize=8,leading=11,textColor=navy,spaceAfter=8))
story=[]
def para(t,style='BodyX'):story.append(Paragraph(t,s[style]))
def title(t,n):para(f'{n:02d} / INFORME DE PRÁCTICA','SmallX');para(t,'H')
def table(rows,widths):
    t=Table([[Paragraph(escape(str(v)),s['CellHead' if i==0 else 'CellX']) for v in row] for i,row in enumerate(rows)],colWidths=widths,repeatRows=1)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),navy),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,light]),('LINEBELOW',(0,0),(-1,-1),0.4,colors.HexColor('#dce4ec'))]))
    story.extend([t,Spacer(1,10)])
def pic(name,caption,width=499):
    path=C/name;w,h=ImageReader(str(path)).getSize();story.append(Image(str(path),width=width,height=width*h/w));story.append(Spacer(1,5));para(caption,'SmallX')
def page():story.append(PageBreak())
repo='https://github.com/nathernandez1189/practica-rest-mysql-ubidots'
persist=json.loads((E/'persistencia.json').read_text())
assert all(x['passed'] for x in persist['markers'].values())
root=ET.parse(E/'pytest.xml').getroot();suite=root.find('testsuite');assert int(suite.attrib['failures'])==0 and int(suite.attrib['errors'])==0
para('COMPUTACIÓN EN LA NUBE · ESPECIALIZACIÓN','SmallX')
para('Práctica REST<br/>MySQL e IoT','TitleX')
para('<b>Natalia Hernández Piedrahita</b><br/><b>Miguel Ángel Diuza</b><br/><b>Juan Ospina Tenorio</b>')
para('Ejecución: 24 de septiembre de 2026 · America/Bogota.<br/>Entorno: Ubuntu 22.04 ARM64, Vagrant y VirtualBox.','SmallX')
table([['35 / 35','42 / 42','60 / 60'],['Pruebas Python aprobadas','Respuestas HTTP correctas','Aserciones Postman/Newman']], [166,166,167])
pic('01-resumen.png','Figura 1. Captura real del panel local construido a partir de los registros de ejecución incluidos en el repositorio.')
para('<b>Estado:</b> APIs de memoria y MySQL, desafío JavaScript y persistencia comprobados. El simulador Ubidots está implementado y probado localmente; faltan cuenta, recepción real, dashboard y alerta por correo.','BodyX')
para(f'Repositorio público: <link href="{repo}" color="#127367">{repo}</link>','SmallX')
page()
title('API REST y ejecución sobre Ubuntu',2)
para('La práctica implementa el recurso <b>books</b> con los campos id, title, description y author. Las dos APIs Flask comparten el contrato HTTP; la implementación JavaScript utiliza el mismo esquema MySQL.')
table([['Servicio','Almacenamiento','Puerto'],['Python / apirest.py','Memoria del proceso','5000'],['Python / apirest_mysql.py','MySQL 8.0.46','5001'],['JavaScript / server.js','MySQL 8.0.46','5002']], [210,229,60])
table([['Operación','Ruta','Resultado esperado'],['Consultar','GET /books y /books/<id>','200; 404 si no existe'],['Crear','POST /books','201 y cabecera Location'],['Actualizar','PUT /books/<id>','200; validación 400'],['Eliminar','DELETE /books/<id>','200; 404 si no existe']], [100,210,189])
para('Se rechazan títulos vacíos, tipos incorrectos y campos desconocidos. Las consultas SQL se parametrizan; se comprobó que una cadena con sintaxis SQL se conserva como texto. Los errores de conexión se devuelven como 503 sin exponer datos internos.')
pic('05-curl.png','Figura 2. Registro real de curl contra MySQL: siete respuestas esperadas. También se ejecutó el mismo flujo en memoria y JavaScript.',width=400)
para('Las APIs se instalaron en /home/vagrant/practica-rest-equipo, sobre servidorUbuntu (192.168.100.3). La alternativa servidorRest del Vagrantfile fue validada como configuración; no se creó esa nueva VM.','SmallX')
page()
title('MySQL y persistencia comprobada',3)
para('La base exclusiva <b>rest_equipo</b> usa una tabla <b>books</b> con motor InnoDB y codificación utf8mb4. id es clave primaria autoincremental; title, description y author son VARCHAR(255). La cuenta de la API tiene permisos de lectura y escritura sobre esta base.')
rows=[['Origen','ID de prueba','Tras encender','Interpretación']]
for label,m in persist['markers'].items():rows.append([label,m['book']['id'],m['after_status'],'Se perdió en memoria' if label=='memory' else 'Se conservó íntegro'])
table(rows,[120,90,100,189])
pic('02-persistencia.png','Figura 3. Resultados contrastados antes y después de un apagado real de Ubuntu. El archivo vm-apagada.txt registra el estado poweroff.')
para('Los registros se crearon antes del apagado y se consultaron después del encendido. Se compararon sus campos completos. MySQL mantuvo los libros creados por Python y JavaScript; el registro de memoria devolvió 404.')
para('Antes: '+persist['before_utc']+'<br/>Después: '+persist['after_utc'],'SmallX')
para('<b>Respuesta al ejercicio:</b> apagar la VM conserva los datos confirmados de MySQL en su disco. La memoria del proceso se reinicia. Destruir la VM o borrar su disco es diferente de apagarla y puede eliminar los datos.')
para('Evidencias: persistencia.json, vm-apagada.txt, vm-encendido.txt, mysql-despues-encendido.txt y respaldo-rest_equipo.sql. La copia SQL contiene únicamente libros de esta práctica.','SmallX')
page()
title('Pruebas reproducibles y Postman',4)
para('Las comprobaciones se separan por herramienta. Algunas validan el mismo comportamiento desde niveles distintos; no se suman como si fueran requisitos únicos.')
table([['Grupo','Resultado','Archivo auditable'],['Python / pytest','35 aprobadas','evidencias/pytest.txt y pytest.xml'],['HTTP real','14 por API; 42 en total','evidencias/http-real.json'],['Postman / Newman','20 por API; 60 aserciones','evidencias/newman-5000/5001/5002.*'],['curl','7 por API; 21 respuestas','evidencias/curl-*.txt']], [105,140,254])
pic('04-postman-newman.png','Figura 4. Captura del resumen de Newman: ocho peticiones y veinte aserciones por implementación, sin fallos.')
para('<b>Alcance de Postman:</b> la colección se ejecutó con Newman, el ejecutor oficial de Postman. No se afirma haber utilizado la interfaz gráfica. La colección está lista para importarla y ejecutar Collection Runner.')
para('Cobertura: CRUD completo, lectura de un recurso eliminado, ids inexistentes, títulos inválidos, campos inesperados, caracteres Unicode y texto con sintaxis SQL. Las pruebas Python agregan vaciado total de memoria, ids no reutilizados y respuestas 503 controladas.')
para('La automatización de GitHub repite pruebas Python y pruebas de integración con un servicio MySQL real. El estado vigente debe consultarse en la pestaña Actions del repositorio; los archivos locales conservan el resultado de esta ejecución.','SmallX')
page()
title('Ubidots: implementación y pendiente real',5)
para('<b>Esta parte aún no está completada en la nube.</b> Durante la ejecución no había cuenta Ubidots disponible. Por eso no se certifica recepción de datos, dashboard ni correo. La simulación local y los dobles de prueba no sustituyen esas evidencias.')
table([['Variable','Contenido','Widget previsto'],['temperature','Temperatura simulada, 18 a 35 °C','Barras'],['humidity','Humedad simulada, 35 a 85 %','Gauge / indicador'],['position','Latitud y longitud ficticias','Mapa'],['luminosity','100 a 1000 lux; variable adicional','Indicador numérico'],['pressure','745 a 755 hPa; variable adicional','Línea']], [115,230,154])
para('El cliente usa requests y HTTPS. El token se lee de UBIDOTS_TOKEN; no se guarda en el código. El envío usa una etiqueta de dispositivo validada, un tiempo máximo de espera y comprobación de errores internos por variable. El modo --dry-run muestra expresamente que no envía datos.')
para('Pasos necesarios para cerrar el requisito','Sub')
for text in ['1. Crear y verificar una cuenta educativa Ubidots STEM y configurar el token local.','2. Enviar cinco muestras desde Python; repetir la actualización con curl y la colección Postman.','3. Crear los cinco widgets y capturar cambios de valores y marcas de tiempo.','4. Configurar temperature > 30 y un destinatario autorizado; enviar 24 y luego 34, y verificar el correo recibido.','5. Guardar las respuestas, el dashboard, el evento y el correo sin exponer credenciales.']:
 para(text)
para('La guía detallada está en docs/UBIDOTS.md. Las coordenadas son simuladas alrededor de Bogotá y no representan la ubicación de los integrantes. Los envíos son finitos para controlar el consumo de la cuenta.')
para('Fuentes oficiales','Sub')
para('<link href="https://ubidots.com/stem" color="#127367">ubidots.com/stem</link><br/><link href="https://help.ubidots.com/en/articles/569964-simulate-data-in-ubidots-using-python" color="#127367">Ubidots: simulación de datos en Python</link><br/><link href="https://help.ubidots.com/en/articles/639806-plans-billing-what-is-the-difference-between-ubidots-and-ubidots-stem" color="#127367">Ubidots: condiciones y límites del plan STEM</link>','SmallX')
page()
title('Desafío, reproducción y sustentación',6)
para('El desafío opcional se implementó en <b>JavaScript</b>, usando el módulo HTTP de Node.js y mysql2. Comparte el contrato de libros y la base con Python; se comprobó con las mismas pruebas HTTP, curl, Postman y persistencia.')
pic('06-api-mysql-en-vivo.png','Figura 5. Consulta directa a la API activa en el navegador: libros iniciales y los dos marcadores conservados después del apagado.',width=450)
para('Reproducir y revisar','Sub')
para('1. Consultar README.md y docs/REPRODUCIR.md.<br/>2. Encender servidorUbuntu desde ~/prueba con Vagrant; entrar por SSH.<br/>3. En /home/vagrant/practica-rest-equipo ejecutar pytest y scripts/verify_http.py.<br/>4. Importar las colecciones de postman/ o repetir Newman.<br/>5. Revisar registros de evidencias/ y el informe; cerrar Ubidots cuando exista cuenta.')
table([['Integrante','Propuesta de explicación'],['Natalia Hernández Piedrahita','API REST, métodos HTTP y pruebas'],['Miguel Ángel Diuza','MySQL, consultas y persistencia'],['Juan Ospina Tenorio','Simulador IoT y desafío JavaScript']], [205,294])
para('Este reparto es una propuesta para la sustentación, no una atribución de autoría del código. La guía incluye preguntas probables y respuestas técnicas.','SmallX')
para('Referencias docentes: guías REST (2024) y REST + MySQL (2023); repositorios de omondragon/APIRestFlask, APIRestFlaskMySQLUbuntu y UbidotsClient. Revisiones y adaptaciones documentadas en docs/REFERENCIAS.md. Los PDFs originales no se redistribuyen.','SmallX')
para('<b>Entrega:</b> el repositorio queda disponible para el profesor. Su publicación no equivale al envío en CampusDigital; no se ha realizado una entrega en ese portal desde esta tarea.','SmallX')

def footer(c,d):
    c.setStrokeColor(colors.HexColor('#d3dee7'));c.line(48,43,547,43);c.setFont(F,8);c.setFillColor(grey);c.drawString(48,29,'REST / MySQL / IoT · Natalia, Miguel y Juan Ospina');c.drawRightString(547,29,str(d.page))
output=P/'docs/Informe-Practica-REST-MySQL-IoT.pdf'
doc=SimpleDocTemplate(str(output),pagesize=(595.28,841.89),rightMargin=48,leftMargin=48,topMargin=42,bottomMargin=55,title='Práctica REST, MySQL e IoT - Informe de evidencias',author='Natalia Hernández Piedrahita, Miguel Ángel Diuza, Juan Ospina Tenorio')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(output)
