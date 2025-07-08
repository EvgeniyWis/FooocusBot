CREATE DATABASE IF NOT EXISTS 'focuus_bot';

CREATE TABLE IF NOT EXISTS 'users' (
    'id' INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    'user_id' BIGINT NOT NULL UNIQUE,
)

CREATE TABLE IF NOT EXISTS 'loras_for_img_generation' (
    'id' INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    'title' VARCHAR(255) NOT NULL UNIQUE,
                                                      
)

CREATE TABLE IF NOT EXISTS 'loras_current_user' (
    'id' INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    'user_id' iNT FOREIGN KEY REFERENCES 'users'('id') NOT NULL,
    'loras_id' INT FOREIGN KEY REFERENCES 'loras_for_img_generation'('id') NOT NULL,
    'loras_weight' FLOAT NOT NULL,
)  

CREATE TABLE IF NOT EXISTS 'prompt_for_img_generation_current_user' (
    
)