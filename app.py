from flask import Flask, jsonify, request
import subprocess
import logging
import json

app = Flask(__name__)

@app.route('/')
def index():
    return 'Flask is working.'

@app.route('/run-script-1', methods=['POST'])
def run_script_1():
    try:
        logging.info("Starting subprocess to run the script")
        result = subprocess.run(
            ["python3", "/Users/haripriyakrishnan/Downloads/Python/flask_app/spotify_dailyglobalchart_notification.py"], 
            capture_output=True, text=True
        )
        
        logging.info("Subprocess completed with return code %s", result.returncode)
        logging.info("Subprocess stdout: %s", result.stdout)
        logging.info("Subprocess stderr: %s", result.stderr)

        if result.returncode == 0:
            if "change_detected" in result.stdout:
                logging.info("Change detected in script output")
                return jsonify(status="change_detected"), 200
            else:
                logging.info("No change detected in script output")
                return jsonify(status="no_change"), 200
        
        logging.error("Subprocess did not complete successfully")
        return jsonify(error="Script executed with issues", stdout=result.stdout, stderr=result.stderr), 500
          
    except Exception as e:
        logging.exception("An error occurred while running the script")
        return jsonify(error=f"An error occurred: {str(e)}"), 500

@app.route('/run-script-2', methods=['POST'])
def run_script_2():
    try:
        logging.info("Starting spotify_tracks_notification.py...")

        # Call the Python script
        result = subprocess.run(
            ["python3", "/Users/haripriyakrishnan/Downloads/Python/flask_app/spotify_tracks_notification.py"],
            capture_output=True, text=True
        )

        # Log the results
        logging.info("Script completed with return code: %s", result.returncode)
        logging.info("stdout: %s", result.stdout)

        if result.returncode == 0:
            logging.info("Spotify Tracks updated successfully.")
            return jsonify(status="Spotify Tracks are updated successfully"), 200
        else:
            logging.error("Error in script execution: %s", result.stderr)
            return jsonify(error=f"Spotify Tracks update failed:\n{result.stderr}"), 500

    except FileNotFoundError as fnf_error:
        logging.error("Script not found: %s", fnf_error)
        return jsonify(error="Script not found."), 500

    except Exception as e:
        logging.error("An unexpected error occurred: %s", str(e))
        return jsonify(error=f"An error occurred: {str(e)}"), 500
    
@app.route('/run-script-3', methods=['POST'])
def run_script_3():
    try:
        logging.info("Starting subprocess to run the script")
        result = subprocess.run(
            ["python3", "/Users/haripriyakrishnan/Downloads/Python/flask_app/spotify_weeklyglobalartist.py"], 
            capture_output=True, text=True
        )
        
        logging.info("Subprocess completed with return code %s", result.returncode)
        logging.info("Subprocess stdout: %s", result.stdout)
        logging.info("Subprocess stderr: %s", result.stderr)

        if result.returncode == 0:
            return jsonify(status="Spotify Tracks are updated successfully"), 200
        else:
            return jsonify(error=f"Spotify Tracks update failed:\n{result.stderr}"), 500
          
    except Exception as e:
        return jsonify(error=f"An error occurred: {str(e)}"), 500

@app.route('/run-script-4', methods=['POST'])
def run_script4():
    if request.content_type != 'application/json':
        return jsonify({"error": "Unsupported Media Type"}), 415

    try:
        result = subprocess.run(
            ['python', '/Users/haripriyakrishnan/Downloads/Python/01.tkfm_spotify_create_playlist.py'],
            capture_output=True,
            text=True,
            check=True
        )

        # Log the standard output and standard error
        app.logger.info("Standard Output: %s", result.stdout)
        app.logger.info("Standard Error: %s", result.stderr)

        # Attempt to parse the output as JSON
        try:
            response = json.loads(result.stdout)
        except json.JSONDecodeError:
            app.logger.error("Failed to parse JSON: %s", result.stdout)
            return jsonify({"error": "Invalid JSON output from Python script"}), 500

        return jsonify(response), 200

    except subprocess.CalledProcessError as e:
        app.logger.error("Python script error: %s", e.stderr)
        return jsonify({"error": "Error executing Python script"}), 500
    except Exception as e:
        app.logger.error("Exception occurred: %s", str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/run-script-5', methods=['POST'])
def run_script5():
    if request.content_type != 'application/json':
        return jsonify({"error": "Unsupported Media Type"}), 415

    try:
        result = subprocess.run(
            ['python', '/Users/haripriyakrishnan/Downloads/Python/08.b.tkfm_youtube_playlist.py'],
            capture_output=True,
            text=True,
            check=True
        )

        # Log the standard output and standard error
        app.logger.info("Standard Output: %s", result.stdout)
        app.logger.info("Standard Error: %s", result.stderr)

        # Attempt to parse the output as JSON
        try:
            response = json.loads(result.stdout)
        except json.JSONDecodeError:
            app.logger.error("Failed to parse JSON: %s", result.stdout)
            return jsonify({"error": "Invalid JSON output from Python script"}), 500

        return jsonify(response), 200

    except subprocess.CalledProcessError as e:
        app.logger.error("Python script error: %s", e.stderr)
        return jsonify({"error": "Error executing Python script"}), 500
    except Exception as e:
        app.logger.error("Exception occurred: %s", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)


