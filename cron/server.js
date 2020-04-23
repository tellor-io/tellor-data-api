const request = require('request');

const poll = {
    pollB: function() {
        var options = {
          url: process.env.API_UPDATE_URL,
          auth: {
            user: process.env.BACKEND_USERNAME,
            password: process.env.BACKEND_PASSWORD
          }
        }
        request(options)
        .on('response', (res) => {
            const statusCode  = res.statusCode;

            let error;
            if (statusCode !== 200) {
                error = new Error(`Request Failed.\n` +
                    `Status Code: ${statusCode}`);
            }

            setTimeout(poll.pollB, process.env.POLL_INTERVAL * 1000); // request again in 10 secs

        })
        .on('error', (e) => {
            console.error(`Got error: ${e.message}`);
            setTimeout(poll.pollB, process.env.POLL_INTERVAL * 2 * 1000); // request again in 10 secs
        });
    }
}

poll.pollB();
