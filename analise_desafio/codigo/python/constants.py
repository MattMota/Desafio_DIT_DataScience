PATHS = {
    "input" : "../../dados/fonte/dados_ficha_a_desafio.csv",
    "output" : {
        "dw" : "../../dados/data_warehouse/",
        "dl" : "../../dados/data_lake/"
    },
    "dbt" : "../../../db_desafio/seeds/"
}

CATEGORIES = {
    "booleans" : [
        "obito", "luz_eletrica",  "em_situacao_de_rua",  "frequenta_escola",
        "possui_plano_saude",  "familia_beneficiaria_auxilio_brasil",
        "crianca_matriculada_creche_pre_escola"
    ],
    "multivalued" : [
        "meios_transporte", "doencas_condicoes",
        "meios_comunicacao", "em_caso_doenca_procura"
    ],
    "well_defined" : [
        "sexo", "bairro", "raca_cor", "religiao", "escolaridade", "nacionalidade",
        "renda_familiar", "identidade_genero", "orientacao_sexual", "tipo"
    ]
}

TABLE_DROP_VALUES = {
    "bridges" : {
        "meios_comunicacao" : [
            "3 salários mínimos",
            "4 salários mínimos",
            "mais de 4 salários mínimos",
            "manhã"
        ],
        "em_caso_doenca_procura" : [
            "1 salário mínimo"
        ]
    },
    "dimensions" : {
        "religiao" : ["acomp. cresc. e desenv. da criança"],
        "renda_familiar" : ["manhã", "internet"],
        "identidade_genero" : [
            "homossexual (gay / lésbica)",
            "bissexual",
            "sim"
        ]
    }
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