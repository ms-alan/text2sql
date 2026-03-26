# 导入依赖
from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 数据库配置
DB_PATH = "chinook.db"

# 自动创建测试数据库（无需手动下载）
db = SQLDatabase.from_uri(f"sqlite:///{DB_PATH}")

# 初始化大模型 - 使用阿里云 Qwen-Max
model = ChatOpenAI(
    model="qwen-max",
    temperature=0,
    openai_api_base=os.getenv("OPENAI_API_BASE"),
)

# 基础目录
base_dir = "./"


def create_sql_deep_agent():
    """
    创建 SQL Deep Agent
    
    Returns:
        配置好的 agent 实例
    """
    # 创建 SQL 工具集
    toolkit = SQLDatabaseToolkit(db=db, llm=model)
    sql_tools = toolkit.get_tools()
    
    # 显示可用的工具列表
    print("\n📚 已加载的 SQL 工具:")
    for i, tool in enumerate(sql_tools, 1):
        print(f"  {i}. {tool.name} - {tool.description[:50]}...")
    
    # 创建 Deep Agent
    agent = create_deep_agent(
        model=model,
        memory=["./AGENTS.md"],
        skills=[
            "./skills/query-writing",
            "./skills/schema-exploration"
        ],
        tools=sql_tools,
        subagents=[],
        backend=FilesystemBackend(root_dir=base_dir, virtual_mode=False)
    )
    return agent


def execute_query(agent, query: str) -> str:
    """
    执行自然语言查询
    
    Args:
        agent: agent 实例
        query: 用户的自然语言问题
        
    Returns:
        查询结果
    """
    result = agent.invoke({
        "messages": [
            {"role": "user", "content": query}
        ]
    })
    # 处理 AIMessage 对象
    if hasattr(result["messages"][-1], 'content'):
        return result["messages"][-1].content
    else:
        return result["messages"][-1]["content"]


# 启动测试
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Text-to-SQL Agent")
    parser.add_argument("--draw-graph", action="store_true", help="生成 LangGraph 可视化图")
    parser.add_argument("--output", type=str, default="agent_graph.png", help="输出图片文件名")
    args = parser.parse_args()
    
    print("=" * 60)
    print("🚀 Text-to-SQL Agent 启动中...")
    print("=" * 60)
    
    try:
        agent = create_sql_deep_agent()
        
        # 如果用户请求生成图表
        if args.draw_graph:
            print(f"\n🎨 正在生成 LangGraph 可视化图...")
            try:
                # 尝试使用 mermaid 绘制
                graph_image = agent.get_graph().draw_mermaid_png()
                with open(args.output, "wb") as f:
                    f.write(graph_image)
                print(f"✅ 图表已保存到：{args.output}")
                print("💡 提示：你也可以使用在线工具查看 mermaid 格式:")
                print("   https://mermaid.live/")
            except Exception as e:
                print(f"⚠️  PNG 生成失败，尝试输出 Mermaid 文本...")
                mermaid_code = agent.get_graph().draw_mermaid()
                print("\n📊 Mermaid 代码:")
                print(mermaid_code)
                print("\n💡 将上面的代码复制到 https://mermaid.live/ 即可查看图表")
            exit(0)
        
        print("\n✅ SQL Deep Agent 启动成功！")
        
        # 显示数据库信息
        print(f"\n💾 数据库：{DB_PATH}")
        print(f"📊 可用表数量：{len(db.get_usable_table_names())}")
        print(f"📋 表列表：{', '.join(db.get_usable_table_names())}")
        
        # 测试查询示例
        test_queries = [
            "查询总共有多少首歌曲？",
            "列出前 5 位艺术家的名字",
            "每个专辑有多少首歌曲？"
        ]
        
        print("\n" + "=" * 60)
        print("🧪 开始测试查询...")
        print("=" * 60)
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n❓ 测试 {i}: {query}")
            result = execute_query(agent, query)
            print(f"\n📊 结果:\n{result}")
            print("-" * 60)
        
        print("\n✨ 所有测试完成！")
        print("\n💡 使用提示：")
        print("  你可以在代码中调用 execute_query(agent, '你的问题') 来执行查询")
        print("  例如：execute_query(agent, '查询最畅销的专辑')")
        
    except Exception as e:
        print(f"\n❌ 启动失败：{str(e)}")
        print("\n💡 请检查:")
        print("  1. 是否安装了必要的依赖包")
        print("  2. OpenAI API 密钥是否正确配置")
        print("  3. 数据库文件是否存在")
        print("\n📊 生成 LangGraph 可视化图:")
        print("  python3 agent.py --draw-graph [--output graph.png]")