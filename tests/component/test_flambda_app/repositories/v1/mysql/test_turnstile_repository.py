import pytest
import pymysql
from flambda_app.repositories.v1.mysql.turnstile_repository import TurnstileRepository
from flambda_app.vos.turnstile import TurnstileVO
from pymysql.err import IntegrityError

# Configuração global para o banco de testes
TEST_DB_NAME = "test_store"
TEST_TABLE_NAME = "test_turnstile"

from flambda_app.config import get_config

config = get_config()


@pytest.fixture(scope="function")
def db_connection():
    """Cria conexão com o banco de testes"""
    connection = pymysql.connect(
        host=config.get('DB_HOST'),
        user=config.get('DB_USER'),
        password=config.get('DB_PASSWORD'),
        database=TEST_DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )
    connection.select_db(TEST_DB_NAME)
    yield connection


@pytest.fixture(scope="function")
def repository(db_connection):
    """Instancia o repositório para cada teste, sobrescrevendo a tabela usada"""
    repo = TurnstileRepository(mysql_connection=db_connection)

    # Sobrescreve as variáveis para garantir o uso da tabela e schema de teste
    repo.__class__.BASE_TABLE = TEST_TABLE_NAME  # Usando a tabela de teste
    repo.__class__.BASE_SCHEMA = TEST_DB_NAME  # Usando o schema de teste

    return repo


@pytest.fixture(scope="function", autouse=True)
def setup_database(db_connection):
    """Cria estrutura da tabela e limpa os dados antes de cada teste"""
    with db_connection.cursor() as cursor:
        cursor.execute(f"DROP TABLE IF EXISTS {TEST_DB_NAME}.{TEST_TABLE_NAME}")
        cursor.execute(f"""
                    CREATE TABLE {TEST_DB_NAME}.{TEST_TABLE_NAME} (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        uuid VARCHAR(36) NOT NULL,
                        name VARCHAR(255) NOT NULL,
                        is_active BOOLEAN NOT NULL DEFAULT TRUE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                        deleted_at TIMESTAMP NULL,
                        UNIQUE (uuid)
                    )
                """)
    db_connection.commit()


def test_create(repository, db_connection):
    """Testa a criação de um registro"""

    data = {
        "uuid": "123e4567-e89b-12d3-a456-426614174000",
        "name": "Entrada Principal",
        "is_active": True
    }

    turnstile = TurnstileVO(data)
    # Chama o método create do repositório, passando o objeto TurnstileVO
    created = repository.create(turnstile)
    assert created is True


def test_create_duplicate_uuid(repository, db_connection):
    """Testa a criação de um registro com UUID duplicado (violação de chave única)"""
    turnstile_1 = TurnstileVO({
        "uuid": "123e4567-e89b-12d3-a456-426614174001",
        "name": "Entrada 1",
        "is_active": True
    })

    turnstile_2 = TurnstileVO({
        "uuid": "123e4567-e89b-12d3-a456-426614174001",
        "name": "Entrada 2",
        "is_active": True
    })

    repository.create(turnstile_1)

    # Tenta criar com UUID duplicado
    is_duplicated = repository.create(turnstile_2)
    assert is_duplicated is False


def test_get(repository):
    """Testa a recuperação de um registro"""
    turnstile = TurnstileVO({
        "uuid": "123e4567-e89b-12d3-a456-426614174001",
        "name": "Saída Principal",
        "is_active": True})

    repository.create(turnstile)
    retrieved = repository.get(value="123e4567-e89b-12d3-a456-426614174001", key="uuid")
    assert retrieved is not None
    assert retrieved.uuid == "123e4567-e89b-12d3-a456-426614174001"
    assert retrieved.name == "Saída Principal"


def test_list(repository):
    """Testa a listagem de registros"""
    repository.create(TurnstileVO({"uuid": "uuid-1", "name": "Entrada 1"}))
    repository.create(TurnstileVO({"uuid": "uuid-2", "name": "Entrada 2"}))

    results = repository.list(where={})
    assert len(results) == 2


def test_count(repository):
    """Testa a contagem de registros"""
    repository.create(TurnstileVO({"uuid": "uuid-3", "name": "Entrada 3"}))

    total = repository.count(where={})
    assert total == 1


def test_update(repository):
    """Testa a atualização de um registro"""
    turnstile = TurnstileVO({"uuid": "uuid-4", "name": "Entrada 4"})
    repository.create(turnstile)

    updated_data = TurnstileVO({"name": "Entrada Atualizada"})
    repository.update(value="uuid-4", key="uuid", turnstile=updated_data)

    updated_turnstile = repository.get(value="uuid-4", key="uuid")
    assert updated_turnstile.name == "Entrada Atualizada"


def test_soft_delete(repository, db_connection):
    """Testa a exclusão lógica de um registro"""
    turnstile = TurnstileVO({"uuid": "uuid-5", "name": "Entrada 5"})
    repository.create(turnstile)

    repository.soft_delete(value="uuid-5", key="uuid")

    db_connection.ping(reconnect=True)

    with db_connection.cursor() as cursor:
        cursor.execute(
            f"SELECT deleted_at FROM {TEST_DB_NAME}.{TEST_TABLE_NAME} WHERE uuid = 'uuid-5'")
        result = cursor.fetchone()

        assert result["deleted_at"] is not None


def test_soft_delete_nonexistent(repository):
    """Testa a exclusão lógica de um registro inexistente"""
    result = repository.soft_delete(value="uuid-nonexistent", key="uuid")
    assert result.rowcount == 0
