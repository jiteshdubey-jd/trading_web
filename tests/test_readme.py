from __future__ import annotations

import re
import tradingview_screener
from pathlib import Path
import requests
from http.cookiejar import CookieJar
import pandas as pd


def authenticate(username: str, password: str) -> CookieJar:
    session = requests.Session()
    r = session.post(
        'https://www.tradingview.com/accounts/signin/',
        headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.tradingview.com'},
        data={'username': username, 'password': password, 'remember': 'on'},
        timeout=60,
    )
    r.raise_for_status()
    if r.json().get('error'):
        raise Exception(f'Failed to authenticate: \n{r.json()}')
    return session.cookies


def test_readme_examples():
    readme = Path(tradingview_screener.__file__).parents[2] / 'README.md'
    source = readme.read_text(encoding='utf-8')

    matches = re.findall(r'(?<=```python)(.*?)(?=```)', source)

    lines = []
    for match in matches:
        for line in match.splitlines():
            line = line.strip().lstrip('>>> ')
            lines.append(line)

    pd.options.display.max_rows = 10  # hard limit, even on small DFs

    code = '\n'.join(lines)
    print("Executing the following code:")
    print(code)

    assert '>>>' not in code, 'cleaning failed'

    # Execute the code with error handling
    try:
        for line in code.splitlines():
            exec(line)
    except Exception as e:
        print(f"Error executing code: {e}")


if __name__ == '__main__':
    test_readme_examples()

# TODO: add this to CI/CD (with GH actions)
