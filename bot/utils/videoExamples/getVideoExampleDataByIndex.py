from .getVideoExamplesData import getVideoExamplesData

# Функция для получения видео-примера по его индексу
async def getVideoExampleDataByIndex(index: str):
    templates_examples = await getVideoExamplesData()
    return templates_examples[index]