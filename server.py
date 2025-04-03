from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import yaml
import os
from dotenv import load_dotenv
from promptwizard.glue.promptopt.instantiate import GluePromptOpt

load_dotenv(override=True)

app = FastAPI()

path_to_config = "configs"
promptopt_config_path = os.path.join(path_to_config, "promptopt_config.yaml")
setup_config_path = os.path.join(path_to_config, "setup_config.yaml")

class ConfigUpdateRequest(BaseModel):
    config_dict: dict

@app.post("/update-config")
def update_config(request: ConfigUpdateRequest):
    file_path = promptopt_config_path
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)

        for field, value in request.config_dict.items():
            data[field] = value

        with open(file_path, 'w') as file:
            yaml.dump(data, file, default_flow_style=False)

        return {"message": "YAML file updated successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get-best-prompt")
def get_best_prompt():
    try:
        gp = GluePromptOpt(promptopt_config_path,
                           setup_config_path,
                           dataset_jsonl=None,
                           data_processor=None)

        best_prompt, expert_profile = gp.get_best_prompt(use_examples=False, run_without_train_examples=True, generate_synthetic_examples=False)
        return {"best_prompt": best_prompt, "expert_profile": expert_profile}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))