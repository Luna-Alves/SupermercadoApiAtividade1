class Categoria:
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome

    def to_json(self):
        return {'id': self.id, 'nome': self.nome}
