CREATE TABLE turnstile (
    id INT AUTO_INCREMENT PRIMARY KEY,
    uuid VARCHAR(36) NOT NULL, -- Identificador único
    name VARCHAR(255) NOT NULL, -- Nome do status
    is_active BOOLEAN NOT NULL DEFAULT TRUE, -- Indica se o status está ativo
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Data e hora de criação
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- Atualização automática
    deleted_at TIMESTAMP NULL, -- Campo de data e hora de exclusão
    UNIQUE (uuid) -- Índice único para garantir integridade
);
