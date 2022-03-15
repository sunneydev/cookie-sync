interface CookieRequest {
  action: "get";
  cookies: string[];
  domain: string;
}

const neededCookies: string[] = [];
let ws: WebSocket;

const connect = () => {
  const _ws = new WebSocket("ws://localhost:3001/ws");
  ws = _ws;
  ws.onopen = () => {
    console.log("Connected! 👌");
  };

  ws.onmessage = async (event): Promise<void> => {
    const cookieReq: CookieRequest = JSON.parse(event.data);

    switch (cookieReq.action) {
      case "get":
        let retrievedCookies: { [key: string]: string }[] = [];

        if (cookieReq.cookies.length) {
          const promises = cookieReq.cookies.map((c) =>
            chrome.cookies
              .get({ name: c, url: cookieReq.domain })
              .then((c) => c && retrievedCookies.push({ [c.name]: c.value }))
          );

          await Promise.all(promises);
        } else {
          retrievedCookies = (await chrome.cookies.getAll({})).map((c) => ({
            [c.name]: c.value,
          }));
        }

        ws.send(JSON.stringify(retrievedCookies));
    }
  };

  ws.onclose = () => {
    console.log("Disconnected! 👎");
    setTimeout(connect, 10 * 1000);
  };

  ws.onerror = () => {
    console.log("Error! 💩");
    ws.close();
  };
};

connect();

chrome.cookies.onChanged.addListener((c) => {
  if (
    c.cause === "overwrite" &&
    (neededCookies.includes(c.cookie.name) || !neededCookies.length)
  ) {
    ws.send(JSON.stringify({ [c.cookie.name]: c.cookie.value }));
  }
});
