from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os
import json
import logging

app = FastAPI()

# Allow frontend requests (CORS for development purposes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production (use specific domains)
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Define the directory where G-code files are stored
GCODE_DIRECTORY = os.path.expanduser("./gcodes")


def parse_gcode(file_path):
    """Parse G-code file to extract additional metadata."""
    info = {
        "print_time": None,
        "filament_type": None,
        "filament_length": None,
        "filament_weight": None,
        "layer_count": None,
        "bed_temp": None,
        "nozzle_temp": None
    }

    try:
        with open(file_path, "r") as file:
            for line in file:
                if "estimated printing time" in line:
                    info["print_time"] = line.split("=")[1].strip()
                elif "; filament_type" in line:
                    info["filament_type"] = line.split("=")[1].strip()
                elif "filament used [mm]" in line:
                    info["filament_length"] = line.split("=")[1].strip()
                elif "filament used [g]" in line:
                    info["filament_weight"] = line.split("=")[1].strip()
                elif "; total layer number:" in line:
                    info["layer_count"] = int(line.split(":")[1].strip())
                elif line.startswith("M140 S"):  # Bed temperature
                    info["bed_temp"] = int(line.split("S")[1].split(";")[0].strip())
                elif "; nozzle_temperature" in line: # Nozzle temperature
                    info["nozzle_temp"] = int(line.split("=")[1].strip())
    except Exception as e:
        logging.warning(f"Error parsing G-code file {file_path}: {e}")
    
    return info



def list_gcode_files():
    gcode_path = Path(GCODE_DIRECTORY)
    if not gcode_path.exists():
        return {"error": f"G-code directory does not exist: {GCODE_DIRECTORY}"}

    gcode_files = []
    for file in gcode_path.glob("*.gcode"):
        metadata = {
            "name": file.name,
            "size": file.stat().st_size,
            "created_at": file.stat().st_ctime,
            "modified_at": file.stat().st_mtime,
            "path": str(file.resolve())
        }
        # Add parsed G-code info
        metadata.update(parse_gcode(file))
        gcode_files.append(metadata)

    return gcode_files


# API endpoint to list G-code files
@app.get("/api/gcodes", response_class=JSONResponse)
async def get_gcodes():
    result = list_gcode_files()

    # Check for errors
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    if "message" in result:
        raise HTTPException(status_code=404, detail=result["message"])

    return result

# Serve the root URL (`/`) with the index.html file
@app.get("/", response_class=HTMLResponse)
async def serve_index():
    with open("static/index.html", "r") as file:
        return HTMLResponse(content=file.read())


# Load wish list data from JSON file
#def load_wishlist():
#    #file_path = os.path.join(os.path.dirname(__file__), "wishlist.json")
#    with open("data/wishlist.json", "r") as file:
#        return json.load(file)

# API endpoint to serve wish list data
#@app.get("/api/wishlist", response_class=JSONResponse)
#async def get_wishlist():
#    return load_wishlist()

# Serve the root URL (`/`) with the index.html file
#@app.get("/", response_class=HTMLResponse)
#async def serve_index():
#    with open("static/index.html", "r") as file:
#        return HTMLResponse(content=file.read())
