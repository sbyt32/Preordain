from preordain.utils.connections import send_response
import re


def get_scryfall_bulk():
    bulk_data_link = send_response("GET", "https://api.scryfall.com/bulk-data")

    for bulk_data_info in bulk_data_link["data"]:
        if bulk_data_info["type"] == "default_cards":
            regex_pattern = re.compile(
                r"[0-9]{4}-[0-9]{2}-[0-9]{2}.*[0-9]{2}:[0-9]{2}:[0-9]{2}", re.IGNORECASE
            )
            fetch_time = regex_pattern.search(bulk_data_info["updated_at"])

            if fetch_time:
                file_name = fetch_time.group()

                file_name = file_name.replace("T", "_")
                file_name = file_name.replace(":", "")

                return send_response("GET", bulk_data_info["download_uri"]), file_name
