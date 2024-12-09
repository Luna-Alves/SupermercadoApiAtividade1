from helpers.application import app
from helpers.database import get_connection
from helpers.logging import logger
from models.Produto import Produto
from models.Usuario import Usuario
from models.Setor import Setor
from models.Categoria import Categoria
from flask import request, jsonify

@app.route("/")
def home():
    return {"versao": "1.0"}, 200

@app.route("/produtos", methods=['GET'])
def get_produtos():
    try:
        conn = get_connection()
        cursor = conn.execute("SELECT * FROM produtos")
        produtos = [Produto(row['id'], row['nome']).to_json() for row in cursor.fetchall()]
        logger.info("Todos os produtos:")
        return jsonify(produtos), 200
    except Exception as e:
        logger.error(f"Erro ao listar produtos: {e}")
        return jsonify({'error': str(e)}), 500

@app.route("/produtos/<int:id>", methods=['GET'])
def get_produto(id):
    try:
        conn = get_connection()
        cursor = conn.execute("SELECT * FROM produtos WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row:
            produto = Produto(row['id'], row['nome']).to_json()
            logger.info(f"Produto: {produto}")
            return jsonify(produto), 200
        else:
            logger.warning(f"Produto {id} não encontrado")
            return jsonify({'mensagem': 'Produto não encontrado'}), 404
    except Exception as e:
        logger.error(f"Produto não encontrado: {e}")
        return jsonify({'error': str(e)}), 500

@app.route("/produtos", methods=['POST'])
def add_produto():
    try:
        data = request.get_json()
        nome = data.get('nome')
        if not nome:
            logger.warning("Por favor digitar nome do produto")
            return jsonify({'mensagem': 'Digite o nome do produto'}), 400
        conn = get_connection()
        cursor = conn.execute("INSERT INTO produtos (nome) VALUES (?)", (nome,))
        conn.commit()
        novo_id = cursor.lastrowid
        produto = {'id': novo_id, 'nome': nome}
        logger.info(f"Produto adicionado: {produto}")
        return jsonify(produto), 201
    except Exception as e:
        logger.error(f"Erro ao adicionar o produto: {e}")
        return jsonify({'error': str(e)}), 500

@app.route("/produtos/<int:id>", methods=['PUT'])
def update_produto(id):
    try:
        data = request.get_json()
        nome = data.get('nome')
        if not nome:
            logger.warning("Por favor digite o nome do produto para atualizar")
            return jsonify({'mensagem': 'Digite o nome do produto'}), 400
        conn = get_connection()
        cursor = conn.execute("SELECT * FROM produtos WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row:
            conn.execute("UPDATE produtos SET nome = ? WHERE id = ?", (nome, id))
            conn.commit()
            produto = {'id': id, 'nome': nome}
            logger.info(f"Produto atualizado: {produto}")
            return jsonify(produto), 200
        else:
            logger.warning(f"Produto {id} não foi encontrado")
            return jsonify({'mensagem': 'Produto não encontrado'}), 404
    except Exception as e:
        logger.error(f"Erro ao atualizar o produto: {e}")
        return jsonify({'error': str(e)}), 500

@app.route("/produtos/<int:id>", methods=['DELETE'])
def delete_produto(id):
    try:
        conn = get_connection()
        cursor = conn.execute("SELECT * FROM produtos WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row:
            conn.execute("DELETE FROM produtos WHERE id = ?", (id,))
            conn.commit()
            logger.info(f"O produto {id} foi deletado")
            return jsonify({'mensagem': 'Produto deletado com sucesso'}), 200
        else:
            logger.warning(f"O produto {id} não foi encontrado")
            return jsonify({'mensagem': 'Produto não encontrado'}), 404
    except Exception as e:
        logger.error(f"Erro ao deletar produto: {e}")
        return jsonify({'error': str(e)}), 500

@app.route("/usuarios", methods=['GET'])
def get_usuarios():
    try:
        conn = get_connection()
        cursor = conn.execute("SELECT * FROM usuarios")
        usuarios = [Usuario(row['id'], row['nome']).to_json() for row in cursor.fetchall()]
        logger.info("Todos os usuários")
        return jsonify(usuarios), 200
    except Exception as e:
        logger.error(f"Erro ao listar os usuários: {e}")
        return jsonify({'error': str(e)}), 500

@app.route("/usuarios/<int:id>", methods=['GET'])
def get_usuario(id):
    try:
        conn = get_connection()
        cursor = conn.execute("SELECT * FROM usuarios WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row:
            usuario = Usuario(row['id'], row['nome']).to_json()
            logger.info(f"Usuário encontrado: {usuario}")
            return jsonify(usuario), 200
        else:
            logger.warning(f"Usuário {id} não foi encontrado")
            return jsonify({'mensagem': 'Usuário não encontrado'}), 404
    except Exception as e:
        logger.error(f"O usuário não foi encontrado: {e}")
        return jsonify({'error': str(e)}), 500

@app.route("/usuarios", methods=['POST'])
def add_usuario():
    try:
        data = request.get_json()
        nome = data.get('nome')
        if not nome:
            logger.warning("Digite um nome de usuário")
            return jsonify({'mensagem': 'Digite um nome de usuário'}), 400
        conn = get_connection()
        cursor = conn.execute("INSERT INTO usuarios (nome) VALUES (?)", (nome,))
        conn.commit()
        novo_id = cursor.lastrowid
        usuario = {'id': novo_id, 'nome': nome}
        logger.info(f"Usuário adicionado: {usuario}")
        return jsonify(usuario), 201
    except Exception as e:
        logger.error(f"Erro ao adicionar usuário: {e}")
        return jsonify({'error': str(e)}), 500

@app.route("/usuarios/<int:id>", methods=['PUT'])
def update_usuario(id):
    try:
        data = request.get_json()
        nome = data.get('nome')
        if not nome:
            logger.warning("Digite um nome de usuário para atualizar")
            return jsonify({'mensagem': 'Digite um nome de usuário'}), 400
        conn = get_connection()
        cursor = conn.execute("SELECT * FROM usuarios WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row:
            conn.execute("UPDATE usuarios SET nome = ? WHERE id = ?", (nome, id))
            conn.commit()
            usuario = {'id': id, 'nome': nome}
            logger.info(f"Usuário atualizado: {usuario}")
            return jsonify(usuario), 200
        else:
            logger.warning(f"Usuário {id} não foi encontrado")
            return jsonify({'mensagem': 'Usuário não encontrado'}), 404
    except Exception as e:
        logger.error(f"Erro ao atualizar o usuário: {e}")
        return jsonify({'error': str(e)}), 500

@app.route("/usuarios/<int:id>", methods=['DELETE'])
def delete_usuario(id):
    try:
        conn = get_connection()
        cursor = conn.execute("SELECT * FROM usuarios WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row:
            conn.execute("DELETE FROM usuarios WHERE id = ?", (id,))
            conn.commit()
            logger.info(f"Usuário {id} deletado")
            return jsonify({'mensagem': 'Usuário deletado com sucesso'}), 200
        else:
            logger.warning(f"Usuário {id} não encontrado")
            return jsonify({'mensagem': 'Usuário não encontrado'}), 404
    except Exception as e:
        logger.error(f"Erro ao deletar usuário: {e}")
        return jsonify({'error': str(e)}), 500

@app.route("/setores", methods=['GET'])
def get_setores():
    try:
        conn = get_connection()
        cursor = conn.execute("SELECT * FROM setores")
        setores = [Setor(row['id'], row['nome']).to_json() for row in cursor.fetchall()]
        logger.info("Todos os setores")
        return jsonify(setores), 200
    except Exception as e:
        logger.error(f"Erro ao listar os setores: {e}")
        return jsonify({'error': str(e)}), 500

@app.route("/setores/<int:id>", methods=['GET'])
def get_setor(id):
    try:
        conn = get_connection()
        cursor = conn.execute("SELECT * FROM setores WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row:
            setor = Setor(row['id'], row['nome']).to_json()
            logger.info(f"Setor encontrado: {setor}")
            return jsonify(setor), 200
        else:
            logger.warning(f"Setor {id} não encontrado")
            return jsonify({'mensagem': 'Setor não encontrado'}), 404
    except Exception as e:
        logger.error(f"Erro ao obter setor: {e}")
        return jsonify({'error': str(e)}), 500

@app.route("/setores", methods=['POST'])
def add_setor():
    try:
        data = request.get_json()
        nome = data.get('nome')
        if not nome:
            logger.warning("Digite o nome do setor")
            return jsonify({'mensagem': 'Digite o nome do setor'}), 400
        conn = get_connection()
        cursor = conn.execute("INSERT INTO setores (nome) VALUES (?)", (nome,))
        conn.commit()
        novo_id = cursor.lastrowid
        setor = {'id': novo_id, 'nome': nome}
        logger.info(f"Setor adicionado: {setor}")
        return jsonify(setor), 201
    except Exception as e:
        logger.error(f"Erro ao adicionar o setor: {e}")
        return jsonify({'error': str(e)}), 500

@app.route("/setores/<int:id>", methods=['PUT'])
def update_setor(id):
    try:
        data = request.get_json()
        nome = data.get('nome')
        if not nome:
            logger.warning("Digite o nome do setor para atualizar")
            return jsonify({'mensagem': 'Digite o nome do setor'}), 400
        conn = get_connection()
        cursor = conn.execute("SELECT * FROM setores WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row:
            conn.execute("UPDATE setores SET nome = ? WHERE id = ?", (nome, id))
            conn.commit()
            setor = {'id': id, 'nome': nome}
            logger.info(f"Setor atualizado: {setor}")
            return jsonify(setor), 200
        else:
            logger.warning(f"Setor {id} não foi encontrado")
            return jsonify({'mensagem': 'Setor não encontrado'}), 404
    except Exception as e:
        logger.error(f"Erro ao atualizar setor: {e}")
        return jsonify({'error': str(e)}), 500

@app.route("/setores/<int:id>", methods=['DELETE'])
def delete_setor(id):
    try:
        conn = get_connection()
        cursor = conn.execute("SELECT * FROM setores WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row:
            conn.execute("DELETE FROM setores WHERE id = ?", (id,))
            conn.commit()
            logger.info(f"Setor com id {id} deletado")
            return jsonify({'mensagem': 'Setor deletado com sucesso'}), 200
        else:
            logger.warning(f"Setor {id} não foi encontrado")
            return jsonify({'mensagem': 'Setor não encontrado'}), 404
    except Exception as e:
        logger.error(f"Erro ao deletar o setor: {e}")
        return jsonify({'error': str(e)}), 500

@app.route("/categorias", methods=['GET'])
def get_categorias():
    try:
        conn = get_connection()
        cursor = conn.execute("SELECT * FROM categorias")
        categorias = [Categoria(row['id'], row['nome']).to_json() for row in cursor.fetchall()]
        logger.info("Todas as categorias")
        return jsonify(categorias), 200
    except Exception as e:
        logger.error(f"Erro ao carregar as categorias: {e}")
        return jsonify({'error': str(e)}), 500

@app.route("/categorias/<int:id>", methods=['GET'])
def get_categoria(id):
    try:
        conn = get_connection()
        cursor = conn.execute("SELECT * FROM categorias WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row:
            categoria = Categoria(row['id'], row['nome']).to_json()
            logger.info(f"Categoria encontrada: {categoria}")
            return jsonify(categoria), 200
        else:
            logger.warning(f"Categoria {id} não encontrada")
            return jsonify({'mensagem': 'Categoria não encontrada'}), 404
    except Exception as e:
        logger.error(f"Erro ao carregar categoria: {e}")
        return jsonify({'error': str(e)}), 500

@app.route("/categorias", methods=['POST'])
def add_categoria():
    try:
        data = request.get_json()
        nome = data.get('nome')
        if not nome:
            logger.warning("Digite o nome da categoria")
            return jsonify({'mensagem': 'Digite o nome da categoria'}), 400
        conn = get_connection()
        cursor = conn.execute("INSERT INTO categorias (nome) VALUES (?)", (nome,))
        conn.commit()
        novo_id = cursor.lastrowid
        categoria = {'id': novo_id, 'nome': nome}
        logger.info(f"Categoria adicionada: {categoria}")
        return jsonify(categoria), 201
    except Exception as e:
        logger.error(f"Erro ao adicionar categoria: {e}")
        return jsonify({'error': str(e)}), 500

@app.route("/categorias/<int:id>", methods=['PUT'])
def update_categoria(id):
    try:
        data = request.get_json()
        nome = data.get('nome')
        if not nome:
            logger.warning("Digite o nome da categoria para atualizar")
            return jsonify({'mensagem': 'Digite o nome da categoria'}), 400
        conn = get_connection()
        cursor = conn.execute("SELECT * FROM categorias WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row:
            conn.execute("UPDATE categorias SET nome = ? WHERE id = ?", (nome, id))
            conn.commit()
            categoria = {'id': id, 'nome': nome}
            logger.info(f"Categoria atualizada: {categoria}")
            return jsonify(categoria), 200
        else:
            logger.warning(f"Categoria {id} não encontrada")
            return jsonify({'mensagem': 'Categoria não encontrada'}), 404
    except Exception as e:
        logger.error(f"Erro ao atualizar categoria: {e}")
        return jsonify({'error': str(e)}), 500

@app.route("/categorias/<int:id>", methods=['DELETE'])
def delete_categoria(id):
    try:
        conn = get_connection()
        cursor = conn.execute("SELECT * FROM categorias WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row:
            conn.execute("DELETE FROM categorias WHERE id = ?", (id,))
            conn.commit()
            logger.info(f"Categoria {id} deletada")
            return jsonify({'mensagem': 'Categoria deletada com sucesso'}), 200
        else:
            logger.warning(f"Categoria não encontrada")
            return jsonify({'mensagem': 'Categoria não encontrada'}), 404
    except Exception as e:
        logger.error(f"Erro ao deletar categoria: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
