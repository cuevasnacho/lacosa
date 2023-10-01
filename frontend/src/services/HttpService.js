const SERVER_URI = ' http://127.0.0.1:8000/';

const parseJSONResponse = (response) => {
  return new Promise((resolve) => response.json()
    .then((json) => resolve({
      status: response.status,
      ok: response.ok,
      json,
    })));
}

async function httpRequest({ method, service, headers, payload }) {
  let route = SERVER_URI + service;

  const config = {
    method,
    headers: {
      'Content-Type': 'application/json',
      ...headers
    }
  };

  if (payload) {
    config.body = JSON.stringify(payload);
  }

  return new Promise((resolve, reject) => {
    fetch(route, config)
      .then(parseJSONResponse)
      .then((response) => {
        if (response.ok) {
          return resolve(response.json);
        }
        return reject(response.json);
      })
      .catch((error) => reject(error));
  });
}

export {
  httpRequest
};