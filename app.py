from flask import Flask, render_template, request
import tracker

app = Flask(__name__)


@app.route("/")
def index():
    """Renders the main input form."""
    return render_template("index.html")


@app.route("/track", methods=["POST"])

def track():
    """
    Receives the form submission, runs the tracker,
    and renders the results page.
    """
    steam_id = request.form.get("steam_id")
    # The checkbox will send 'true' if checked, otherwise it's None
    use_test_data = request.form.get("use_test_data") == "true"

    # If using test data, we don't need a real steam_id, but we pass one for consistency
    if use_test_data:
        steam_id_for_tracker = "TEST_DATA_MODE"
    else:
        if not steam_id:
            # Basic validation
            return "Error: SteamID is required if not using test data.", 400
        steam_id_for_tracker = steam_id

    items, results, error = tracker.run_tracker(
        steam_id_for_tracker, use_test_data
    )

    return render_template(

        "results.html",
        items=items,
        results=results,
        steam_id=steam_id,
        use_test_data=use_test_data,
        error_message=error,
    )


if __name__ == "__main__":
    # For local development. Vercel will use a WSGI server.
    app.run(debug=True, port=8080)
