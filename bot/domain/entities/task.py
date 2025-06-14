from dataclasses import asdict, dataclass
from typing import Dict, Any


@dataclass
class TaskDTO:
    """
    Data Transfer Object (DTO) для представления задачи генерации.
    
    Attributes:
        job_id: Уникальный идентификатор задачи
        user_id: ID пользователя Telegram
        message_id: ID сообщения для обновления
        model_name: Название модели генерации
        setting_number: Номер настройки
        job_type: Тип задачи (например, 'image_generation')
        is_test_generation: Флаг тестовой генерации
        check_other_jobs: Флаг проверки других задач
        chat_id: ID чата
    """
    job_id: str
    user_id: int
    message_id: int
    model_name: str
    setting_number: int
    job_type: str
    is_test_generation: bool
    check_other_jobs: bool
    chat_id: int
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразует объект TaskDTO в словарь.
        
        Returns:
            Словарь с данными задачи
        """
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TaskDTO':
        """
        Создает объект TaskDTO из словаря.
        
        Args:
            data: Словарь с данными задачи
            
        Returns:
            Новый экземпляр TaskDTO
        """
        return cls(**data)
