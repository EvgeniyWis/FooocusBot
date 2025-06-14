from bot.helpers.videoExamples.getVideoExamplesData import getVideoExamplesData


# Функция для получения видео-примера по его индексу
async def getVideoExampleDataByIndex(index: int):
    templates_examples = await getVideoExamplesData()
    return templates_examples[index]
