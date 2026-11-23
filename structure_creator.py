import json
import os
from pathlib import Path

def create_file_structure_from_json(json_data_path: str, base_output_dir: str):
    """
    Reads a JSON file defining a project structure and creates the corresponding
    directory and file structure on the specified system path.

    Args:
        json_data_path (str): The path to the input JSON file.
        base_output_dir (str): The root directory where the new structure will be created.
    """
    print(f"--- Starting File Structure Creation ---")

    # 1. Load the JSON data
    try:
        with open(json_data_path, 'r') as f:
            data = json.load(f)
        print(f"Successfully loaded structure from: {json_data_path}")
    except FileNotFoundError:
        print(f"ERROR: JSON file not found at {json_data_path}")
        return
    except json.JSONDecodeError:
        print(f"ERROR: Could not decode JSON from {json_data_path}. Check file format.")
        return
    except Exception as e:
        print(f"An unexpected error occurred during file loading: {e}")
        return

    # Ensure the base output directory exists
    output_path = Path(base_output_dir)
    try:
        output_path.mkdir(parents=True, exist_ok=True)
        print(f"Base output directory ensured: {output_path.resolve()}")
    except Exception as e:
        print(f"ERROR: Could not create base directory {base_output_dir}: {e}")
        return

    # 2. Process the structure
    for key, value in data.items():
        if key == "file_structure":
            structure = value
            
            # Create the main 'src' directory
            src_path = output_path / "src"
            src_path.mkdir(parents=True, exist_ok=True)
            print(f"Created directory: src/")

            # Iterate through components within 'src'
            for component_key, component_data in structure.get("components", {}).items():
                component_dir = src_path / component_key
                component_dir.mkdir(parents=True, exist_ok=True)
                print(f"  -> Created component directory: {component_key}/")

                # Iterate through files within the component
                for file_name in component_data.get("files", []):
                    file_path = component_dir / file_name
                    # Create the empty file
                    file_path.touch()
                    print(f"    Created file: {file_name}")

            # Process other top-level keys (like 'styles', 'public', 'scripts')
            if key in ["styles", "public", "scripts"]:
                key_path = output_path / key
                key_path.mkdir(parents=True, exist_ok=True)
                print(f"Created directory: {key}")
                
                # Handle specific file creation for 'public' example
                if key == "public" and "index.html" in value.get("index.html", []):
                    (key_path / "index.html").touch()
                    print("    Created public/index.html")


    print("\n--- File Structure Creation Complete! ---")
    print(f"All files and folders have been created under: {output_path.resolve()}")


# --- Configuration ---
if __name__ == "__main__":
    # 1. Define the path to your JSON file
    INPUT_JSON_FILE = "project_structure.json"
    
    # 2. Define where you want the structure to be created on your system
    # !!! CHANGE THIS PATH to a safe location on your computer !!!
    OUTPUT_ROOT_DIRECTORY = "./BrowserTouchDesignerClone_Output" 

    # --- Setup: Create a dummy JSON file for testing if it doesn't exist ---
    if not os.path.exists(INPUT_JSON_FILE):
        print(f"Creating dummy JSON file: {INPUT_JSON_FILE} for testing...")
        dummy_json_content = {
          "project_name": "BrowserTouchDesignerClone",
          "description": "Modular structure for a browser-based visual programming environment.",
          "technology_stack_assumed": [
            "React/Vue (Frontend UI)",
            "Three.js/Babylon.js (Rendering)",
            "TypeScript (Language)",
            "WebGL/WebGPU (Shader execution)"
          ],
          "file_structure": {
            "components": {
              "ui": {
                "description": "Main component for the node graph editor (drag-and-drop, node placement).",
                "files": [
                  "NodeCanvas.jsx",
                  "NodeEditor.jsx",
                  "ConnectionLine.jsx"
                ]
              },
              "Node": {
                "description": "Reusable component for individual nodes (e.g., Tops, Chops, Output).",
                "files": [
                  "BaseNode.jsx",
                  "TopNode.jsx",
                  "ChopNode.jsx"
                ]
              },
              "Inspector": {
                "description": "Panel for configuring node properties.",
                "files": [
                  "InspectorPanel.jsx"
                ]
              }
            },
            "engine": {
              "runtime": {
                "description": "Core logic for interpreting the node graph and executing computations.",
                "files": [
                  "RuntimeEngine.js",
                  "NodeGraphParser.js",
                  "ExecutionContext.js"
                ]
              },
              "stateManagement": {
                "description": "Handles the state of the current graph and node connections.",
                "files": [
                  "GraphState.js",
                  "ConnectionManager.js"
                ]
              }
            },
            "rendering": {
              "renderer": {
                "description": "Handles the WebGL/WebGPU setup and shader compilation.",
                "files": [
                  "WebGLRenderer.js",
                  "SceneManager.js"
                ]
              },
              "shaders": {
                "description": "Storage for all GLSL/WGSL shader code.",
                "files": [
                  "main_render.glsl",
                  "uv_debug_shader.glsl"
                ]
              }
            },
            "utils": {
              "math": {
                "files": [
                  "VectorMath.js",
                  "MatrixUtils.js"
                ]
              },
              "helpers": {
                "files": [
                  "ColorUtils.js"
                ]
              }
            }
          },
          "styles": {
            "css": [
              "App.css",
              "NodeCanvas.css"
            ]
          },
          "public": {
            "index.html": "Main entry point for the browser application.",
            "assets": {
              "models": "path/to/3d_models/",
              "shaders": "path/to/shaders/"
            }
          },
          "scripts": {
            "build": "build.js",
            "dev": "start_dev.js"
          }
        }
      }
        with open(INPUT_JSON_FILE, 'w') as f:
            json.dump(dummy_json_content, f, indent=2)
        print(f"Dummy JSON file '{INPUT_JSON_FILE}' created successfully.")
    # --- End Setup ---


    # Run the main function
    create_file_structure_from_json(INPUT_JSON_FILE, OUTPUT_ROOT_DIRECTORY)