import json
import requests

def main(sheet_url):
    """
    args:
        sheet_url: str => Google Sheet link
    returns:
        header: list[str] => strings of sheet headers
        rows: list[list[str]] => list of rows. each row represent values in sheet
    """
    sheet_json = get_sheet(sheet_url)
    rows = []
    for i in sheet_json:
        title = i["title"]["$t"]
        col_names, col_values = split_contents(i["content"]["$t"])
        if len(rows) == 0:
            header = ["title"] + col_names
        rows.append([title] + col_values)
    return header, rows

def get_sheet(url):
    r = requests.get(url)
    sheet_text = r.text
    sheet_json = json.loads(sheet_text)["feed"]["entry"]
    return sheet_json

def split_contents(content_str):
    columns = content_str.strip().split(",")
    col_names = []
    col_values = []
    for i in columns:
        col_content = i.split(":", 1)
        col_names.append(col_content[0].strip())
        col_values.append(col_content[1].strip())
    return col_names, col_values

if __name__ == "__main__":
    main()