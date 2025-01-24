import logging
import sys
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.structure.graph import Graph
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.traversal import P, Cardinality, Column, Order, Pop, Scope, T, Direction
import asyncio
import json
from pathlib import Path

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# Windows平台特定的事件循环策略
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

def analyze_basic_workflow_details():
    """详细分析 basic 工作流的所有节点和关系"""
    url = 'ws://localhost:8182/gremlin'
    
    try:
        # 连接图数据库
        graph = Graph()
        connection = DriverRemoteConnection(url, 'g')
        g = graph.traversal().withRemote(connection)
        
        try:
            # 1. 获取 basic 工作流的完整信息
            logger.info("\n=== Basic 工作流完整信息 ===")
            basic_workflow = g.V().has('workflow', 'name', 'basic').valueMap(True).next()
            logger.info(f"节点ID: {basic_workflow[T.id]}")
            logger.info(f"节点标签: {basic_workflow[T.label]}")
            logger.info("节点属性:")
            for key, value in basic_workflow.items():
                if key not in [T.id, T.label]:
                    logger.info(f"  - {key}: {value[0]}")

            # 2. 获取所有相关的边
            logger.info("\n=== 所有相关的边 ===")
            
            # 2.1 出边（从 basic 出发的边）
            logger.info("\n出边详情:")
            out_edges = g.V().has('workflow', 'name', 'basic').outE().project('label', 'inV_name').by(T.label).by(__.inV().values('name')).toList()
            for edge in out_edges:
                logger.info(f"- 边标签: {edge['label']}, 指向节点: {edge['inV_name']}")

            # 2.2 入边（指向 basic 的边）
            logger.info("\n入边详情:")
            in_edges = g.V().has('workflow', 'name', 'basic').inE().project('label', 'outV_name').by(T.label).by(__.outV().values('name')).toList()
            for edge in in_edges:
                logger.info(f"- 边标签: {edge['label']}, 来自节点: {edge['outV_name']}")

            # 3. 获取工作流文件内容
            logger.info("\n=== 工作流文件内容 ===")
            file_path = basic_workflow.get('file_path')
            if file_path:
                try:
                    file_path = Path(file_path)
                    if file_path.exists():
                        with open(file_path, 'r', encoding='utf-8') as f:
                            workflow_content = json.load(f)
                        logger.info(f"工作流JSON内容: {json.dumps(workflow_content, indent=2, ensure_ascii=False)}")
                    else:
                        logger.error(f"文件不存在: {file_path}")
                except Exception as e:
                    logger.error(f"无法读取工作流文件: {e}")

            # 4. 获取所有属性的统计信息
            logger.info("\n=== 属性统计 ===")
            property_keys = g.V().has('workflow', 'name', 'basic').properties().key().dedup().toList()
            logger.info(f"所有属性键: {property_keys}")

            # 5. 获取与该节点相关的所有可能路径
            logger.info("\n=== 相关路径 ===")
            paths = g.V().has('workflow', 'name', 'basic').both().path().by(elementMap()).toList()
            for path in paths:
                logger.info("\n路径详情:")
                for vertex in path:
                    if isinstance(vertex, dict):
                        logger.info(f"  节点类型: {vertex.get(T.label)}")
                        for k, v in vertex.items():
                            if k not in [T.id, T.label]:
                                logger.info(f"    - {k}: {v}")

            # 6. 获取相邻节点
            logger.info("\n相邻节点详情:")
            neighbors = g.V().has('workflow', 'name', 'basic').both().valueMap(True).toList()
            for neighbor in neighbors:
                logger.info(f"- 节点ID: {neighbor[T.id]}, 标签: {neighbor[T.label]}")
                for key, value in neighbor.items():
                    if key not in [T.id, T.label]:
                        logger.info(f"  {key}: {value[0]}")

        except Exception as e:
            logger.error(f"查询过程中出错: {e}")
            raise

    finally:
        logger.info(f"closing DriverRemoteConnection with url '{url}'")
        connection.close()
        logger.info(f"Closing Client with url '{url}'")

if __name__ == '__main__':
    analyze_basic_workflow_details() 