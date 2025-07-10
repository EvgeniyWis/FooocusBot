CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    user_id BIGINT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS loras (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    setting_number INT NOT NULL,
    UNIQUE(title, setting_number)
);

CREATE TABLE IF NOT EXISTS user_loras (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    lora_id INT NOT NULL REFERENCES loras(id) ON DELETE CASCADE,
    model_id INT REFERENCES models(id) ON DELETE CASCADE,
    setting_number INT NOT NULL,
    weight FLOAT NOT NULL,
    is_override BOOLEAN DEFAULT FALSE,
    UNIQUE (user_id, lora_id, model_id, setting_number)
);


CREATE TABLE IF NOT EXISTS user_prompts (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    model_id INT NOT NULL REFERENCES models(id) ON DELETE CASCADE,
    setting_number INT NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('positive', 'negative')),
    prompt TEXT NOT NULL,
    UNIQUE (user_id, model_id, setting_number, type)
);

CREATE TABLE IF NOT EXISTS models (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    setting_number INT NOT NULL,
    UNIQUE (name, setting_number)
);