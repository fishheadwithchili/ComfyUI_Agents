from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.structure.graph import Graph
import asyncio
import sys
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Windows平台特定的事件循环策略
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

def example_operations():
    """展示数据库基本操作的示例"""
    # 连接到数据库
    url = 'ws://localhost:8182/gremlin'
    graph = Graph()
    connection = DriverRemoteConnection(url, 'g')
    g = graph.traversal().withRemote(connection)
    
    try:
        # 1. 添加新类别
        logger.info("创建新类别...")
        new_category = g.addV('category')\
            .property('name', 'advanced_techniques')\
            .property('description', '高级技术工作流程')\
            .next()
        
        # 2. 添加新工作流
        logger.info("创建新工作流...")
        new_workflow = g.addV('workflow')\
            .property('name', 'super_resolution')\
            .property('description', '超分辨率工作流程')\
            .property('created_date', '2024-01-24')\
            .next()
        
        # 3. 建立关系
        logger.info("建立工作流与类别的关系...")
        g.V(new_workflow)\
            .addE('belongs_to')\
            .to(g.V(new_category))\
            .next()
        
        # 4. 查询示例
        logger.info("\n=== 查询示例 ===")
        
        # 4.1 按类别查询工作流
        logger.info("\n按类别查询工作流:")
        category_workflows = g.V()\
            .hasLabel('category')\
            .has('name', 'advanced_techniques')\
            .in_('belongs_to')\
            .valueMap()\
            .toList()
        
        for workflow in category_workflows:
            logger.info(f"找到工作流: {workflow.get('name', [''])[0]}")
        
        # 4.2 搜索特定工作流
        logger.info("\n搜索特定工作流:")
        specific_workflow = g.V()\
            .hasLabel('workflow')\
            .has('name', 'super_resolution')\
            .valueMap()\
            .next()
        
        logger.info(f"工作流详情: {specific_workflow}")
        
        # 4.3 统计信息
        workflow_count = g.V().hasLabel('workflow').count().next()
        category_count = g.V().hasLabel('category').count().next()
        logger.info(f"\n数据库统计:")
        logger.info(f"工作流总数: {workflow_count}")
        logger.info(f"类别总数: {category_count}")
        
    finally:
        connection.close()

if __name__ == '__main__':
    example_operations() 