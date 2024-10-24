# auto minecraft optimizer with fabric mods

this is a little utility for lazy people!

given a minecraft version as first command line argument, automatically installs mods that optimize the game such as sodium, lithium, iris...

you will have to configure your modirinth token in a .env file

**here's how to do that:**

`echo "TOKEN=YOUR_TOKEN_HERE" > .env`

you can configure the mods that it will download in the downloader.py file (the variable name is MODS)

**installing dependencies:**

`python -m pip install -r requirements.txt`

**usage:**

`python downloader.py <mc_version>`
