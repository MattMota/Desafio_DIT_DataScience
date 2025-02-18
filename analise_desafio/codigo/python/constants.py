PATHS = {
    'input' : "../../dados/dados_ficha_a_desafio.csv"
}

DECODED_CHARS = {
    "\\u00c0" : 'À',
    "\\u00c1" : 'Á',
    "\\u00c2" : 'Â',
    "\\u00c9" : 'É',
    "\\u00ca" : 'Ê',
    "\\u00cd" : 'Í',
    "\\u00d3" : 'Ó',
    "\\u00d4" : 'Ô',
    "\\u00da" : 'Ú',
    "\\u00e0" : 'à',
    "\\u00e1" : 'á',
    "\\u00e2" : 'â',
    "\\u00e3" : 'ã',
    "\\u00e7" : 'ç',
    "\\u00e9" : 'é',
    "\\u00ea" : 'ê',
    "\\u00ed" : 'í',
    "\\u00f3" : 'ó',
    "\\u00f4" : 'ô',
    "\\u00f5" : 'õ',
    "\\u00fa" : 'ú'
}

CONFORMED_BOOLEANS = {
    (0.0, '0', "false", "falso", False) : 0,
    (1.0, '1', "verdadeiro", "true", True) : 1
}