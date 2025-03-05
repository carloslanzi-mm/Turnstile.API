CREATE TABLE access (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type ENUM('entry', 'exit', 'blocked') NOT NULL, -- Tipo de evento
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Registro automático do horário do evento
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Data e hora de criação
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- Atualização automática
    deleted_at TIMESTAMP NULL, -- Campo de data e hora de exclusão
    turnstile_uuid VARCHAR(36), -- FK para o uuid do turnstile
    FOREIGN KEY (turnstile_uuid) REFERENCES turnstile(uuid) -- Referência à tabela de status usando uuid
);
