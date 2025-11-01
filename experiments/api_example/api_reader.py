import requests
import pandas as pd


def get_kanye_quote():
    """
    Request to Kanye REST API, return 1 quote
    """
    url = "https://api.kanye.rest"
    try:
        resp = requests.get(url, timeout=5)  # GET-request, waiting time <= 5 sec
        resp.raise_for_status()  # generating exception, if response code >= 400
        data = resp.json()  # json -> dict
        return data.get("quote")  # return quote or None
    except requests.RequestException as e:  # catch exceptions and return None
        print(f"Request error: {e}")
        return None


def get_n_quotes(n=0):
    """
    Get n requests to Kanye REST API
    """
    quotes = []
    for i in range(n):
        quote = get_kanye_quote()
        if quote:  # if (not None) or (not empty string)
            quotes.append({"id": i + 1, "quote": quote})
    return pd.DataFrame(quotes)  # convert list to pandas.DataFrame


if __name__ == "__main__":
    df = get_n_quotes(10)
    print(df)
    df.to_csv("api_example\kanye_quotes.csv", index=False)
    print("\nKanye is happy.")
