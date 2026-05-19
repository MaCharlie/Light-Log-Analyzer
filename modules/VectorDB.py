import chromadb
from sentence_transformers import SentenceTransformer

import config

class VectorDB(object):

    _instance = None

    # 类方法，单例模式，保证模型可以复用。
    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)

            """ 初始化向量数据库 """
            cls._instance.client = chromadb.PersistentClient(path=config.chroma_data_path) # 存在自动加载 不存在自动创建
            cls._instance.collection = cls._instance.client.get_or_create_collection(
                name="server_logs",
                metadata={"hnsw:space": "cosine"}
            )

            """ 初始化embedding模型 """
            # 读取配置文件
            cls._instance.embed_model = SentenceTransformer(config.embed_model_name, config.embed_cache_path)
        return cls._instance



    @classmethod
    def store_log_blocks(cls, log_blocks: list):
        """ 将预处理后的日志块存入向量数据库 """
        # 分别存储log_id, 文档, 元数据
        ids, documents, metadatas = [], [], []

        # 对于单个日志块
        for block in log_blocks:
            # 设置日志id，起始时间+调用service的hash
            log_id = f"{block['metadata']['start_time']}-{hash(block['metadata']['services'][0])}"
            ids.append(log_id)
            documents.append(block['text_for_embedding'])
            metadatas.append({
                "request_id": block['metadata']['request_id'],
                "start_time": block['metadata']['start_time'],
                "service": block['metadata']['services'][0]
            })

        # 批量生成向量(CPU高效)
        embeddings = cls._instance.embed_model.encode(documents).tolist()

        # 存入向量数据库
        cls._instance.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )


    @classmethod
    def search_logs(cls, query: str, filters: dict = None, top_k: int = 5):
        """
        混合检索日志
        :param query: 自然语言查询--关键字
        :param filters: 元数据过滤
        :param top_k: 返回结果数量
        """
        # 1. 生成查询向量, 用于模糊查询
        query_embedding = cls._instance.embed_model.encode([query]).tolist()[0]

        # 2. 构建混合查询条件
        where_conditions = {}
        if filters:
            if "start_time" in filters:
                where_conditions["start_time"] = {"$gte": filters["start_time"]}
            if "service" in filters:
                where_conditions["service"] = {"$eq": filters["service"]}

        # 3. 执行检索: 元数据过滤 + 语义相似度
        results = cls._instance.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where_conditions,  # 元数据过滤
            include=["documents", "metadatas", "distances"]  # 返回原始文本, 元数据, 相似度距离
        )

        # 4. 整理结果
        output = []
        for i in range(len(results["ids"][0])):
            output.append({
                "id": results["ids"][0][i],
                "text": results["documents"][0][i],
                "score": results["distances"][0][i],
                "metadata": results["metadatas"][0][i]
            })

        return output

