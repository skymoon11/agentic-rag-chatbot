import os
import uuid

from dotenv import load_dotenv
from flask import Flask, jsonify, request

from src.graph.workflow import rag_graph
from src.ingestion.parsers import process_file

load_dotenv()

app = Flask(__name__)

# Basic in-memory document store for indexed content.
INDEXED_DOCUMENTS = {}


@app.route("/api/health", methods=["GET"])
def health_check():
	return jsonify({"status": "healthy", "service": "agentic-rag-backend"}), 200


@app.route("/api/upload", methods=["POST"])
def upload_file():
	"""Handle multimodal uploads (PDF, DOCX, CSV, TXT, and audio)."""
	if "file" not in request.files:
		return jsonify({"error": "No file part in the request"}), 400

	uploaded_file = request.files["file"]
	if uploaded_file.filename == "":
		return jsonify({"error": "No selected file"}), 400

	try:
		parsed_data = process_file(uploaded_file)
		document_id = parsed_data["document_id"]
		INDEXED_DOCUMENTS[document_id] = parsed_data

		return jsonify(
			{
				"status": "success",
				"message": "File processed and indexed successfully",
				"document_id": document_id,
				"filename": parsed_data["filename"],
				"format": parsed_data["format"],
				"char_count": parsed_data["char_count"],
			}
		), 201

	except ValueError as value_error:
		return jsonify({"error": str(value_error)}), 400
	except Exception as error:
		return jsonify({"error": f"Internal processing error: {error}"}), 500


@app.route("/api/chat", methods=["POST"])
def chat():
	"""Execute the LangGraph multi-agent state graph."""
	data = request.get_json() or {}
	user_query = data.get("message", "").strip()
	session_id = data.get("session_id", str(uuid.uuid4()))

	if not user_query:
		return jsonify({"error": "Field 'message' is required"}), 400

	initial_state = {
		"question": user_query,
		"retry_count": 0,
		"documents": [],
		"rewritten_query": "",
		"generation": "",
		"hallucination_grade": "",
	}

	try:
		result = rag_graph.invoke(initial_state)

		return jsonify(
			{
				"session_id": session_id,
				"query": user_query,
				"optimized_query": result.get("rewritten_query"),
				"response": result.get("generation"),
				"retrieved_context": result.get("documents", []),
				"hallucination_evaluation": result.get("hallucination_grade"),
				"total_attempts": result.get("retry_count", 1),
			}
		), 200

	except Exception as error:
		return jsonify({"error": f"Agent processing failed: {error}"}), 500


if __name__ == "__main__":
	port = int(os.getenv("PORT", 5000))
	app.run(host="0.0.0.0", port=port, debug=True)
