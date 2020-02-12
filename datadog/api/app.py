from flask import Flask, jsonify, request
from datetime import datetime
from datadog.utils.daterange import daterange
from datadog.utils.constants import DATE_FORMAT_WITH_HOURS, PENDING, SUCCESS


def create_app(queue, db):
    """Create the Flask app."""

    app = Flask(__name__)
    app.config['QUEUE'] = queue
    app.config['DB'] = db

    @app.route('/ask_page_views', methods=["GET"])
    def ask_page_views():
        """
        This endpoint is responsible for triggering the computation of the report.
        The output json is made of two main elements : already_processed, to_process.
        - already_processed is a dict representing the tasks that has already been executed.
        - to_process is a list representing the tasks that will be executed
        :return: json
        """

        request_content = request.json

        if "start_date" not in request_content:
            return jsonify(
                status_code=404,
                message="Start date should be provided"
            )

        try:
            start_date = datetime.strptime(request_content.get("start_date"), DATE_FORMAT_WITH_HOURS)
            end_date = start_date

            if request_content.get("end_date"):
                end_date = datetime.strptime(request_content["end_date"], DATE_FORMAT_WITH_HOURS)
        except ValueError:
                return jsonify(
                    status_code=404,
                    message=f"Start date and end date type should be in the format :\"{DATE_FORMAT_WITH_HOURS}\""
                )

        to_process = []
        already_processed = dict()

        for date in daterange(start_date, end_date):
            doc = app.config['DB'].get(date)

            if doc:
                if doc.get("status") == SUCCESS:
                    already_processed[str(date)] = doc
                    continue

            app.config["QUEUE"].put(date)
            task = {"date": date, "try_count": 0, "max_tries": 1, "status": PENDING}
            app.config["DB"].insert(task)
            to_process.append(date)

        return jsonify(
            status_code=200,
            message="Will be processed",
            already_processed=already_processed,
            to_process=to_process
        )

    return app

