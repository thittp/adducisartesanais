from contextlib import closing
import mysql.connector

###############################################
#### Funções auxiliares de banco de dados. ####
###############################################

# Converte uma linha em um dicionário.
def row_to_dict(description, row):
    if row is None: return None
    d = {}
    for i in range(0, len(row)):
        d[description[i][0]] = row[i]
    return d

# Converte uma lista de linhas em um lista de dicionários.
def rows_to_dict(description, rows):
    result = []
    for row in rows:
        result.append(row_to_dict(description, row))
    return result

####################################
#### Definições básicas de BD. ####
####################################
### Partes de login. ###
def conectar():
    return mysql.connector.connect(host="adducis.ch3noq1jgsa1.us-east-2.rds.amazonaws.com",user="adducis",password= "654artesanais",database="Usuarios")


def db_fazer_login(login, senha):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT login, senha, nome, tipo FROM usuario WHERE login = %s AND senha = %s;", (login, senha))
        return row_to_dict(cur.description, cur.fetchone())


def db_consultar_usuario(id):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id, nome, login, senha, tipo, telefone FROM usuario WHERE id = (%s)", [id])
        return row_to_dict(cur.description, cur.fetchone())


### Cadastro de usuarios. ###
def db_listar_usuarios():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id, nome, login, senha, tipo, telefone FROM usuario")
        return rows_to_dict(cur.description, cur.fetchall())


def db_criar_usuario(nome, login, senha, tipo, telefone):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO usuario (nome, login, senha, tipo, telefone) VALUES (%s, %s, %s, %s, %s)", [nome, login, senha, tipo, telefone])
        id = cur.lastrowid
        con.commit()
        return {'id': id, 'nome': nome, 'login': login, 'senha': senha, 'tipo': tipo, 'telefone': telefone}

def db_editar_usuario(id, nome, login, senha, tipo, telefone):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("UPDATE usuario SET nome = %s, login = %s, senha = %s, tipo = %s, telefone = %s WHERE id = %s", [nome, login, senha, tipo, telefone, id])
        con.commit()
        return {'id': id, 'nome': nome, 'login': login, 'senha': senha, 'tipo': tipo, 'telefone': telefone}


def db_deletar_usuario(id):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("DELETE FROM usuario WHERE id = %s", [id])
        con.commit()



### produtos ###
def db_listar_produtos():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_produto, nome, preco_atual, ingredientes, prazo_validade, descricao, quantidade FROM produto WHERE status = 'Ativo'")
        return rows_to_dict(cur.description, cur.fetchall())


def db_criar_produto(nome, status, preco_atual, ingredientes, prazo_validade, descricao):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO produto (nome, status, preco_atual, ingredientes, prazo_validade, descricao) VALUES (%s, %s, %s, %s, %s, %s)", [nome, status, preco_atual, ingredientes, prazo_validade, descricao])
        id_produto = cur.lastrowid
        con.commit()
        return {'id_produto': id_produto, 'nome': nome, 'status': status, 'preco_atual': preco_atual, 'ingredientes': ingredientes, 'prazo_validade': prazo_validade, 'descricao': descricao}


def db_consultar_produto(id_produto):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT * FROM produto WHERE id_produto = (%s)", [id_produto])
        return row_to_dict(cur.description, cur.fetchone())


def db_editar_produto(id_produto, nome, status, preco_atual, ingredientes, prazo_validade, descricao):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("UPDATE produto SET nome = %s, status = %s, preco_atual = %s, ingredientes = %s, prazo_validade = %s, descricao = %s WHERE id_produto = %s", [nome, status, preco_atual, ingredientes, prazo_validade, descricao, id_produto])
        con.commit()
        return {'id_produto': id_produto, 'nome': nome, 'status': status, 'preco_atual':preco_atual, 'ingredientes':ingredientes, 'prazo_validade':prazo_validade, 'descricao':descricao}


def db_listar_produtosinativos():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_produto, nome, preco_atual, ingredientes, prazo_validade, descricao FROM produto WHERE status = 'Inativo'")
        return rows_to_dict(cur.description, cur.fetchall())



### vendas ###
def db_listar_vendas():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT * FROM vendas")
        return rows_to_dict(cur.description, cur.fetchall())

def db_consultar_vendas(id_venda):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT * FROM vendas WHERE id_venda = (%s)", [id_venda])
        return row_to_dict(cur.description, cur.fetchone())




### insumo ###
def db_listar_insumo():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT I.id_insumo, I.nome, coalesce(sum(C.quantidade_insumo), '-') as soma,  coalesce(max(date_format(C.data_vencimento, '%d/%m/%Y')), '-') as vencimento FROM insumo AS I Left JOIN itemcompra AS C ON I.id_insumo = C.id_insumo WHERE status = 'Ativo' GROUP BY I.id_insumo")
        return rows_to_dict(cur.description, cur.fetchall())


def db_criar_insumo(nome, status):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO insumo (nome, status) VALUES (%s, %s)", [nome, status])
        id_insumo = cur.lastrowid
        con.commit()
        return {'id_insumo': id_insumo, 'nome': nome, 'status': status}


def db_editar_insumo(id_insumo, nome, status):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("UPDATE insumo SET nome = %s, status = %s WHERE id_insumo = %s", [nome, status, id_insumo])
        con.commit()
        return {'id_insumo': id_insumo, 'nome': nome, 'status': status}


def db_consultar_insumo(id_insumo):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_insumo, nome, status FROM insumo WHERE id_insumo = (%s)", [id_insumo])
        return row_to_dict(cur.description, cur.fetchone())


def db_listar_insumoinativos():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT I.id_insumo, I.nome, coalesce(sum(C.quantidade_insumo), '-') as soma,  coalesce(max(date_format(C.data_vencimento, '%d/%m/%Y')), '-') as vencimento FROM insumo AS I Left JOIN itemcompra AS C ON I.id_insumo = C.id_insumo WHERE status = 'inativo' GROUP BY I.id_insumo")
        return rows_to_dict(cur.description, cur.fetchall())



### compra ###
def db_listar_compra():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT C.id_compra, date_format(C.data_compra, '%d/%m/%Y') as datacompra, C.preco_compra as soma FROM compra AS C")
        return rows_to_dict(cur.description, cur.fetchall())


def db_criar_compra(data_compra, preco_compra):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO compra (data_compra, preco_compra) VALUES (%s, %s)", [data_compra, preco_compra])
        id_compra = cur.lastrowid
        con.commit()
        return {'id_compra': id_compra, 'data_compra': data_compra}


def db_consultar_compra(id_compra):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_compra, data_compra, preco_compra FROM compra WHERE id_compra = (%s)", [id_compra])
        return row_to_dict(cur.description, cur.fetchone())


def db_editar_compra(id_compra, data_compra, preco_compra):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("UPDATE compra SET data_compra = %s, preco_compra = %s WHERE id_compra = %s", [data_compra, preco_compra, id_compra])
        con.commit()
        return {'id_compra': id_compra, 'data_compra': data_compra, 'preco_compra': preco_compra}



### itemcompra ###
def db_listar_item():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT * FROM itemcompra")
        return rows_to_dict(cur.description, cur.fetchall())



### estoque ###
def db_listar_estoque():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT P.id_produto, P.nome, sum(F.quantidade) - sum(V.quantidade) AS quantidade FROM produto as P LEFT JOIN itemfabricacao AS F ON P.id_produto = F.id_produto LEFT JOIN itensvendas AS V ON P.id_produto = V.id_produto GROUP BY P.id_produto")
        return rows_to_dict(cur.description, cur.fetchall())



### fabricacao ###
def db_listar_fabricacao():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT F.id_fabricacao, date_format(F.data_fabricacao, '%d/%m/%Y') as data_fabricacao, coalesce(sum(I.quantidade), '-') as soma FROM fabricacao AS F Left JOIN itemfabricacao AS I ON F.id_fabricacao = I.id_fabricacao GROUP BY F.id_fabricacao")
        return rows_to_dict(cur.description, cur.fetchall())



### Caixa ###
def db_listar_saldo():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT date_format(X.data_registro, '%d/%m/%Y') as 'Data', format(coalesce(sum(X.valor_entrada),0)-(coalesce(sum(X.valor_saida),0)), 2) as ValorDia FROM caixa as X GROUP BY X.data_registro")
        return rows_to_dict(cur.description, cur.fetchall())


def db_listar_entradas():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT date_format(V.data_venda, '%d/%m/%Y') as 'Data', CONCAT('R$ ', Replace(FORMAT(sum(V.preco_venda), 2), '.', ',')) AS Valor FROM vendas as V GROUP BY V.data_venda")
        return rows_to_dict(cur.description, cur.fetchall())


def db_listar_saidas():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT date_format(C.data_compra, '%d/%m/%Y') as 'Data', CONCAT('R$ ', Replace(FORMAT(sum(C.preco_compra), 2), '.', ',')) AS Valor FROM compra as C GROUP BY C.data_compra")
        return rows_to_dict(cur.description, cur.fetchall())
