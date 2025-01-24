import logging
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.structure.graph import Graph
from gremlin_python.driver.serializer import GraphSONMessageSerializer
from gremlin_python.process.graph_traversal import __

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def check_database():
    """检查数据库中的内容"""
    try:
        # 连接数据库
        graph = Graph()
        conn = DriverRemoteConnection(
            'ws://localhost:8182/gremlin',
            'g',
            message_serializer=GraphSONMessageSerializer()
        )
        g = graph.traversal().withRemote(conn)
        logger.info("Connected to graph database")
        
        try:
            # 列出所有工作流及其结构
            logger.info("\n=== 工作流结构 ===")
            workflows = g.V().hasLabel('workflow').valueMap().toList()
            
            for wf in workflows:
                workflow_name = wf.get('name', [''])[0]
                logger.info(f"\n工作流: {workflow_name}")
                logger.info(f"文件路径: {wf.get('file_path', [''])[0]}")
                
                # 获取该工作流的所有节点
                nodes = g.V().hasLabel('node').has('workflow', workflow_name).valueMap().toList()
                logger.info(f"\n节点列表 ({len(nodes)} 个):")
                for node in nodes:
                    node_id = node.get('node_id', [''])[0]
                    node_type = node.get('type', [''])[0]
                    logger.info(f"- {node_type} (ID: {node_id})")
                    
                    # 获取该节点的输出连接
                    out_edges = g.V().hasLabel('node').has('workflow', workflow_name).has('node_id', node_id) \
                        .outE('connects_to').project('to', 'details') \
                        .by(__.inV().values('node_id')) \
                        .by(__.valueMap()).toList()
                    
                    if out_edges:
                        logger.info("  输出连接:")
                        for edge in out_edges:
                            details = edge['details']
                            logger.info(f"  -> 节点 {edge['to']}")
                            logger.info(f"     通过 {details.get('output_name', [''])[0]} -> {details.get('input_name', [''])[0]}")
                
                logger.info("\n" + "="*50)
            
        except Exception as e:
            logger.error(f"查询出错: {str(e)}")
            raise
            
    finally:
        conn.close()
        logger.info("\nClosed database connection")

if __name__ == '__main__':
    check_database() 