function getHost() {
    return fetch('../../host.json')
    .then(response => response.json())
    .then(data => JSON.parse(JSON.stringify(data)).hostname)
    .then(host => host.toString());
}

let host;
getHost().then(hostname => {
    host = hostname;
    console.log(host);
});