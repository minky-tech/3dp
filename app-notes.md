

## Run FastAPI
### Basic python command line

        uvicorn main:app --reload

        uvicorn main:app --host 0.0.0.0 --port 8000


## Steps to Set Up a Systemd Service for Your FastAPI App:

### Create a Systemd Service File:
A systemd service file will define how your FastAPI app should run on startup.

        sudo nano /etc/systemd/system/fastapi-wishlist.service

### Configure the Service.
- Start the FastAPI app using uvicorn.
- Run under the pi user.
- Restart automatically if it fails.
- Be accessible on startup.

Paste the following content:

        [Unit]
        Description=FastAPI Wishlist App
        After=network.target

        [Service]
        User=pi
        WorkingDirectory=/path/to/your/app
        ExecStart=/usr/bin/python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
        Restart=always

        [Install]
        WantedBy=multi-user.target

        Replace /path/to/your/app with the directory where your FastAPI app is located.

### Enable and Start the Service:

    Enable the service so that it starts on boot:

        sudo systemctl enable fastapi-wishlist.service

    Start the service immediately:

        sudo systemctl start fastapi-wishlist.service

### Verify the Service:

    Check the status of the service to ensure it’s running:

        sudo systemctl status fastapi-wishlist.service


### Create a systemd service file
1) (e.g., /etc/systemd/system/wishlist.service):

        [Unit]
        Description=Wishlist FastAPI Service
        After=network.target

        [Service]
        User=print
        WorkingDirectory=/path/to/your/app
        ExecStart=/usr/bin/python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
        Restart=always

        [Install]
        WantedBy=multi-user.target

2) Enable and start the service:

        sudo systemctl enable wishlist.service
        sudo systemctl start wishlist.service

### add app to moonraker.conf

        [fastapi_wishlist]
        server: http://127.0.0.1:8000  # Path to your FastAPI app

## CORS / Middleware

        from fastapi.middleware.cors import CORSMiddleware

        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Adjust for production (use specific domains)
            allow_methods=["*"],
            allow_headers=["*"],
        )


## Redirect Static
- Serve the root URL (`/`) with the index.html file

        @app.get("/", response_class=HTMLResponse)
        async def serve_index():
            with open("static/index.html", "r") as file:
                return HTMLResponse(content=file.read())

- Redirect `/` to `/static/index.html`

        @app.get("/")
        async def root():
            return RedirectResponse(url="/static/index.html")


## fetch JSON files


## Spoolman-type with FastAPI

### Spoolman-like database

        from fastapi import FastAPI
        from pydantic import BaseModel
        from typing import List
        import sqlite3

        app = FastAPI()

        # Database setup
        DB_FILE = "spools.db"

        def init_db():
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS spools (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    material TEXT,
                    color TEXT,
                    weight REAL,
                    remaining REAL
                )
                """)
                conn.commit()

        # Initialize the database
        init_db()

        # Spool data model
        class Spool(BaseModel):
            material: str
            color: str
            weight: float
            remaining: float

        @app.get("/spools", response_model=List[Spool])
        def get_spools():
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT material, color, weight, remaining FROM spools")
                rows = cursor.fetchall()
                return [Spool(material=row[0], color=row[1], weight=row[2], remaining=row[3]) for row in rows]

        @app.post("/spools")
        def add_spool(spool: Spool):
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO spools (material, color, weight, remaining) VALUES (?, ?, ?, ?)",
                    (spool.material, spool.color, spool.weight, spool.remaining)
                )
                conn.commit()
                return {"message": "Spool added successfully"}

        @app.put("/spools/{spool_id}")
        def update_spool(spool_id: int, spool: Spool):
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE spools SET material = ?, color = ?, weight = ?, remaining = ? WHERE id = ?",
                    (spool.material, spool.color, spool.weight, spool.remaining, spool_id)
                )
                conn.commit()
                return {"message": "Spool updated successfully"}

### Integration with Moonraker's WebSocket API

        import websockets
        import asyncio

        async def monitor_moonraker():
            async with websockets.connect("ws://<your-pi-ip>:7125/websocket") as websocket:
                await websocket.send('{"jsonrpc":"2.0","method":"printer.objects.query","params":{"objects":["gcode_move"]},"id":1}')
                while True:
                    message = await websocket.recv()
                    print(message)

        asyncio.run(monitor_moonraker())
