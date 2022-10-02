# GameCodinBackend

The (current) goal of this repo is to receive the code from the users, execute it and return the result.

# Overview

- Whats planned?
- What still needs to happen?
- How is it planned?

Check it [here](https://excalidraw.com/#json=VAclpcNvHgU1IEO3uDhSk,uvj6jSL_QFl0PyonWV3qmQ) or join our [discord](https://discord.gg/k4hMTjcz3g).

# Setup
### required .env variables

Create a .env file, in the GameCodin/env folder with the following values:

```
DATABASE_CONNECTION_STRING=mongodb_connection_string
```


### Add test data
Run the test_data.py file.

This will fill your database with test objects (doesn't represent real data => everything is fictional).

```bash
python3 test_data.py
```


### How to run it?

Open a terminal and run

```bash
python3 -m GameCodin
```