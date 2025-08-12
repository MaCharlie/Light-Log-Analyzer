from flask import Flask, request, jsonify
from modules import LogPreprocessing, VectorDB

app = Flask(__name__)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/ingest', methods=['POST'])
def ingest_logs():
    model_path = request.json['model_path']
    file_path = request.json['file_path']
    log_preprocessor = LogPreprocessing.LogPreprocessing()
    vector_db = VectorDB.VectorDB(model_path)

    log_blocks = log_preprocessor.process_log_file(file_path)
    vector_db.store_log_blocks(log_blocks)
    return jsonify({
        'status': 'success',
        'message': '储存成功',
        'blocks_ingested': len(log_blocks)
    })

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    vector_db = VectorDB.VectorDB(data.get('model_path'))

    results = vector_db.search_logs(
        query=data['query'],
        filters=data.get('filters', None),
        top_k=data.get('top_k', 5)
    )
    return jsonify({
        "results":results,
        "status": "success",
        "message": "查询成功"
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
