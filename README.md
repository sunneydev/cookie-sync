# cookie-sync

## About

This is a simple extension that allows you to sync cookies between Chrome and Python using the [websocket](https://en.wikipedia.org/wiki/WebSocket) protocol.

## Requirements

- Python >= 3.7
- [aiohttp](https://docs.aiohttp.org/en/stable)

## Usage

1. `pip install cookie-sync`

2. Download the and unarchive the extension from [releases](https://github.com/sunney-x/cookie-sync/releases)

3. Set `host_permissions` for the target website in `manifest.json`

4. Load the extension in Chrome

   - Go to `chrome://extensions`
   - Click `Load unpacked` and locate the extension folder

5. Quickstart example

```python
import aiohttp
from cookie_sync import run_server

session = aiohttp.ClientSession()

run_server(
    session=session,
    domain='https://google.com'
)
```

## Documentation

### **run_server** configuration options

```py
session: aiohttp.ClientSession
    - 'The session to keep cookies synced on'

domain: str
    - 'The domain to sync cookies for'

cookies: Optional[list] # Default []
    - 'List of cookies to sync, if empty, all cookies will be synced'

wait_for_cookies: Optional[bool] # Default True
    - 'If `False`, will not wait for the cookies to be synced'

timeout: Optional[int] # Default 30
    - 'Timeout in seconds to wait for `wait_for_cookies`'
```
