import logging
import asyncio
import sys
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.structure.graph import Graph
import time

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Windows平台特定的事件循环策略
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

def test_connection(host='localhost', port=8182, max_retries=10, retry_interval=30):
    """测试与JanusGraph的连接并执行简单查询"""
    url = f'ws://{host}:{port}/gremlin'
    connection = None
    
    for attempt in range(max_retries):
        try:
            logger.info("开始测试与JanusGraph的连接...")
            graph = Graph()
            connection = DriverRemoteConnection(url, 'g')
            g = graph.traversal().withRemote(connection)
            
            # 基本连接测试
            vertex_count = g.V().count().next()
            logger.info(f"连接成功！当前图中有 {vertex_count} 个顶点。")
            
            # 查询所有类别
            logger.info("\n查询所有工作流类别:")
            categories = g.V().hasLabel('category').valueMap().toList()
            for category in categories:
                logger.info(f"类别: {category.get('name', [''])[0]} - {category.get('description', [''])[0]}")
            
            # 查询所有工作流
            logger.info("\n查询所有工作流:")
            workflows = g.V().hasLabel('workflow').valueMap().toList()
            for workflow in workflows:
                logger.info(f"工作流: {workflow.get('name', [''])[0]} - {workflow.get('description', [''])[0]}")
                
            # 查询工作流与类别的关系
            logger.info("\n查询工作流与类别的关系:")
            relations = g.V().hasLabel('workflow').as_('w').out('belongs_to').as_('c').select('w', 'c').by('name').toList()
            for relation in relations:
                logger.info(f"工作流 '{relation['w']}' 属于类别 '{relation['c']}'")
            
            return True
            
        except Exception as e:
            logger.error(f"连接尝试 {attempt + 1}/{max_retries} 失败: {str(e)}")
            if attempt < max_retries - 1:
                logger.info(f"等待 {retry_interval} 秒后重试...")
                time.sleep(retry_interval)
            else:
                logger.error("无法连接到JanusGraph")
                raise
        finally:
            if connection is not None:
                try:
                    connection.close()
                except Exception as e:
                    logger.warning(f"关闭连接时出现警告（可以忽略）: {str(e)}")

if __name__ == '__main__':
    test_connection() 