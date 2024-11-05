from transformers import AutoTokenizer, AutoModel



model_name = "sentence-transformers/all-MiniLM-L6-v2"

AutoTokenizer.from_pretrained(model_name).save_pretrained("./model")

AutoModel.from_pretrained(model_name).save_pretrained("./model")


