db.define_table('intel_search',
                Field('name', 'string', label='Ime poizvedbe'),
                Field('description','text', label='Opis'),
                Field('isearch', 'string', label='Poizvedba'),
                auth.signature,
                redefine=True
)
