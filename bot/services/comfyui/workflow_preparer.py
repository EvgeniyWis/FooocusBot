import copy
import json
from pathlib import Path


class ComfyUIWorkflowPreparer:
    def __init__(self, workflow_template_path: str | Path):
        self.workflow_template_path = Path(workflow_template_path)

    def prepare(self, prompt: str, image_name: str) -> dict:
        with open(self.workflow_template_path) as f:
            template = json.load(f)
        workflow = copy.deepcopy(template["prompt"])
        workflow["220"]["inputs"]["text"] = prompt
        workflow["126"]["inputs"]["image"] = image_name
        return workflow
