from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp import ClientSession
import asyncio

async def test_mcp_direct():
    print("Testing MCP server directly...")
    
    server_params = StdioServerParameters(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-everything"],
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # セッションを初期化
            await session.initialize()
            
            print("✅ MCP Session initialized")
            
            # 利用可能なツールをリスト
            tools = await session.list_tools()
            print(f"\nAvailable tools: {[tool.name for tool in tools.tools]}")
            
            # getTinyImageを呼び出し
            print("\nCalling getTinyImage...")
            result = await session.call_tool("getTinyImage", arguments={})
            
            print(f"\n{'='*70}")
            print(f"Result type: {type(result)}")
            print(f"{'='*70}")
            
            # 結果の属性を確認
            if hasattr(result, '__dict__'):
                print("\nResult attributes:")
                for key, value in result.__dict__.items():
                    print(f"\n--- {key} ---")
                    print(f"Type: {type(value)}")
                    
                    if isinstance(value, list):
                        print(f"List length: {len(value)}")
                        for i, item in enumerate(value):
                            print(f"\n  Item {i}:")
                            print(f"  Type: {type(item)}")
                            if hasattr(item, '__dict__'):
                                for k, v in item.__dict__.items():
                                    v_str = str(v)
                                    if len(v_str) > 200:
                                        print(f"    {k}: (length={len(v_str)}) {v_str[:100]}...{v_str[-100:]}")
                                    else:
                                        print(f"    {k}: {v}")
                            else:
                                print(f"  Value: {item}")
                    else:
                        value_str = str(value)
                        if len(value_str) > 200:
                            print(f"Length: {len(value_str)}")
                            print(f"First 100: {value_str[:100]}")
                            print(f"Last 100: {value_str[-100:]}")
                        else:
                            print(f"Value: {value}")
            
            print(f"\n{'='*70}")
            
            return result

# 実行
try:
    result = asyncio.run(test_mcp_direct())
    print("\n✅ Test completed successfully!")
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()