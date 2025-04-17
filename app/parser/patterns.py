PATTERN_APPLE = (
    r'^\[' # Comienza con un corchete abierto
    r'(?P<date>\d{1,2}/\d{1,2}/\d{2,4}),\s*' # Fecha (dd/mm/yy o dd/mm/yyyy)
    r'(?P<time>\d{1,2}:\d{2}(?::\d{2})?(?:\s*[apAP]\.?[\s]*[mM]\.?)?)'  # Tiempo (hh:mm, opcional :ss y opcional AM/PM)
    r'\]\s+' # Cierra el corchete y sigue con espacios
    r'(?P<user>.+?):\s' # Usuario seguido de dos puntos y espacio
    r'(?P<message>.*)' # Mensaje (todo el texto restante)
)
PATTERN_ANDROID = (
    r'^(?P<date>\d{1,2}/\d{1,2}/\d{4}),\s+' # Fecha en formato dd/mm/yyyy
    r'(?P<time>\d{1,2}:\d{2}(?::\d{2})?(?:\s*[apAP]\.?[\s]*[mM]\.?)?)' # Tiempo (hh:mm, opcional :ss y opcional AM/PM)
    r'\s*-\s*' # Separador " - " con espacios opcionales
    r'(?P<user>.+?):\s' # Usuario seguido de dos puntos y espacio
    r'(?P<message>.*)'  # Mensaje (todo el texto restante)
)

SYSTEM_PATTERN_APPLE = (
    r'^\['
    r'(?P<date>\d{1,2}/\d{1,2}/\d{2,4}),\s*'
    r'(?P<time>\d{1,2}:\d{2}(?::\d{2})?(?:\s*[apAP]\.?[\s]*[mM]\.?)?)'
    r'\]\s+'
)

SYSTEM_PATTERN_ANDROID = (
    r'^(?P<date>\d{1,2}/\d{1,2}/\d{4}),\s+'
    r'(?P<time>\d{1,2}:\d{2}(?::\d{2})?(?:\s*[apAP]\.?[\s]*[mM]\.?)?)'
    r'\s*-\s*'
)