from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.tool_context import ToolContext
from mcp import StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp import ClientSession
from google.api_core import retry
import base64
import os
import tempfile
import shutil
from datetime import datetime

print("✅ ADK components imported successfully.")

retry_config = retry.Retry(
    initial=1.0,
    maximum=10.0,
    multiplier=2.0,
    deadline=60.0,
)

# 非同期関数として定義（ADK FunctionToolは非同期関数をサポート）
async def get_tiny_image_to_file(tool_context: ToolContext) -> dict:
    """Connect to MCP server and get image, save to temp file."""
    try:
        print("Connecting to MCP server...")
        
        server_params = StdioServerParameters(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-everything"],
        )
        
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                print("✅ MCP session initialized")
                
                result = await session.call_tool("getTinyImage", arguments={})
                
                # ImageContentを探す
                base64_data = None
                if hasattr(result, 'content') and isinstance(result.content, list):
                    for item in result.content:
                        if hasattr(item, 'type') and item.type == 'image':
                            base64_data = item.data
                            print(f"✅ Found image data, length: {len(base64_data)}")
                            break
                
                if not base64_data:
                    return {"status": "error", "message": "No image data found in MCP response"}
                
                # base64デコード
                if "data:image" in base64_data:
                    base64_data = base64_data.split(",", 1)[1]
                
                base64_data = base64_data.strip()
                missing_padding = len(base64_data) % 4
                if missing_padding:
                    base64_data += "=" * (4 - missing_padding)
                
                image_bytes = base64.b64decode(base64_data)
                print(f"✅ Decoded image: {len(image_bytes)} bytes")
                
                # 一時ファイルに保存
                temp_dir = tempfile.gettempdir()
                temp_path = os.path.join(temp_dir, f"mcp_image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
                
                with open(temp_path, "wb") as f:
                    f.write(image_bytes)
                
                print(f"✅ Saved to temp file: {temp_path}")
                
                return {
                    "status": "success",
                    "message": "Image retrieved and saved to temporary file",
                    "temp_file_path": temp_path,
                    "size_bytes": len(image_bytes)
                }
                
    except Exception as e:
        import traceback
        print(f"❌ Error: {e}")
        traceback.print_exc()
        return {
            "status": "error",
            "message": str(e),
            "traceback": traceback.format_exc()
        }

# 非同期関数として定義
async def save_temp_file_to_output(tool_context: ToolContext, temp_file_path: str) -> dict:
    """Copy temporary file to output directory."""
    try:
        if not os.path.exists(temp_file_path):
            return {"status": "error", "message": f"Temporary file not found: {temp_file_path}"}
        
        output_dir = "generated_images"
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"{output_dir}/tiny_image_{timestamp}.png"
        
        shutil.copy2(temp_file_path, output_path)
        print(f"✅ Copied to: {output_path}")
        
        # 一時ファイルを削除
        os.remove(temp_file_path)
        print(f"✅ Removed temp file")
        
        return {
            "status": "success",
            "message": f"Image saved successfully to {output_path}",
            "filepath": output_path
        }
        
    except Exception as e:
        import traceback
        return {
            "status": "error",
            "message": str(e),
            "traceback": traceback.format_exc()
        }

get_image_tool = FunctionTool(func=get_tiny_image_to_file)
save_file_tool = FunctionTool(func=save_temp_file_to_output)

print("✅ Tools created")

root_agent = LlmAgent(
    name="mcp1",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=retry_config
    ),
    description="An agent that can generate tiny images using MCP servers",
    instruction="""When the user requests an image:
1. Call get_tiny_image_to_file - it will connect to the MCP server and return a temp_file_path
2. Call save_temp_file_to_output with the temp_file_path to save it to generated_images/
3. Tell the user where the image was saved""",
    tools=[get_image_tool, save_file_tool],
)

print("✅ Root Agent defined.")