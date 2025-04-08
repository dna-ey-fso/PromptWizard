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

TOKEN_COST_INPUT = 0.00000004
TOKEN_COST_OUTPUT = 0.00000004

class ConfigUpdateRequest(BaseModel):
    config_dict: dict

@app.post("/update-config")
def update_config(request: ConfigUpdateRequest):
    file_path = promptopt_config_path
    try:
        # Vérification si le fichier existe
        if not os.path.exists(file_path):
            raise HTTPException(status_code=400, detail=f"Configuration file {file_path} does not exist.")

        # Lecture et mise à jour du fichier YAML
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file) or {}

        for field, value in request.config_dict.items():
            data[field] = value

        with open(file_path, 'w') as file:
            yaml.dump(data, file, default_flow_style=False)

        return {"message": "YAML file updated successfully!"}
    except yaml.YAMLError as e:
        raise HTTPException(status_code=500, detail=f"YAML error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.get("/get-best-prompt")
def get_best_prompt():
    try:
        # Vérification si les fichiers de configuration existent
        if not os.path.exists(promptopt_config_path):
            raise HTTPException(status_code=400, detail=f"Configuration file {promptopt_config_path} is missing.")
        if not os.path.exists(setup_config_path):
            raise HTTPException(status_code=400, detail=f"Setup file {setup_config_path} is missing.")

        # Initialisation de GluePromptOpt
        gp = GluePromptOpt(
            promptopt_config_path,
            setup_config_path,
            dataset_jsonl=None,  # Peut être modifié pour inclure un chemin vers un dataset
            data_processor=None  # Peut être modifié pour inclure un processeur de données
        )

        # Appel à get_best_prompt avec des options supplémentaires
        best_prompt, expert_profile = gp.get_best_prompt(
            use_examples=False,
            run_without_train_examples=True,
            generate_synthetic_examples=False
        )

        # Calcul des tokens d'input et d'output
        token_counts = gp.calculate_tokens(best_prompt, expert_profile)

        return {
            "best_prompt": best_prompt,
            "expert_profile": expert_profile,
            "input_tokens": token_counts["input_tokens"] * TOKEN_COST_INPUT,
            "output_tokens": token_counts["output_tokens"] * TOKEN_COST_OUTPUT,
            "total_tokens": (token_counts["input_tokens"] * TOKEN_COST_INPUT  + token_counts["output_tokens"] * TOKEN_COST_OUTPUT)
        }


    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")