import lamini
from lamini import Lamini
import os, dotenv
from data import get_data

dotenv.load_dotenv()

lamini.api_key = os.getenv("LAMINI_API_KEY")

llm = Lamini(model_name="meta-llama/Meta-Llama-3.1-8B-Instruct")

data = get_data()

llm.tune(data_or_dataset_id=data,
         finetune_args={"learning_rate": 1.0e-3},
         )