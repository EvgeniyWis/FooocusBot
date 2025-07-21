from bot.services.freepik.client.api_client import FreepikAPI


class MagnificAPI(FreepikAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = f"{self.base_url}/image-upscaler"
