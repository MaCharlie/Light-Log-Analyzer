# 运行信息
app_host = "0.0.0.0"
app_port = 5000

# 文件信息
# embed_model_path = "D:/cs/projects/RAG/mooc/RAG_full_stack_course_notebooks/llm_app/gte-large-zh/"
# chroma_data_path = "D:\cs\projects\RAG\LoggingFlask\chroma_data"

embed_model_name = "sentence-transformers/all-MiniLM-L6-v2"
embed_cache_path = "./model/embeddings"
chroma_data_path = "./chroma_data"

# llm
base_url = "http://localhost:11434/v1/"
model_name = "qwen2:72b"

# 重排序模型
reranker_model = "BAAI/bge-reranker-small"