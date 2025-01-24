import logging
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.structure.graph import Graph
from gremlin_python.driver.serializer import GraphSONMessageSerializer

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def test_basic_operations():
    """测试图数据库的基本操作"""
    try:
        # 连接图数据库,使用 GraphSON 序列化
        graph = Graph()
        conn = DriverRemoteConnection(
            'ws://localhost:8182/gremlin',
            'g',
            message_serializer=GraphSONMessageSerializer()
        )
        g = graph.traversal().withRemote(conn)
        logger.info("Connected to graph database")
        
        try:
            # 清空数据库
            g.V().drop().iterate()
            logger.info("Database cleared")
            
            # 创建一个工作流节点
            workflow = g.addV('workflow').property('name', 'test_workflow').next()
            logger.info(f"Created workflow node")
            
            # 创建两个节点
            node1 = g.addV('node').property('name', 'node1').property('type', 'test_type').next()
            node2 = g.addV('node').property('name', 'node2').property('type', 'test_type').next()
            logger.info(f"Created two nodes")
            
            # 创建一个连接
            g.V(node1).addE('connects_to').to(g.V(node2)).property('link_id', '1').iterate()
            logger.info(f"Created edge between nodes")
            
            # 验证节点是否创建成功
            nodes = g.V().hasLabel('node').valueMap().toList()
            logger.info("\nAll nodes in database:")
            for node in nodes:
                logger.info(f"Node properties: {node}")
            
            # 验证边是否创建成功
            edges = g.E().hasLabel('connects_to').valueMap().toList()
            logger.info("\nAll edges in database:")
            for edge in edges:
                logger.info(f"Edge properties: {edge}")
            
        except Exception as e:
            logger.error(f"Error during operations: {str(e)}")
            raise
            
    finally:
        logger.info("\nClosing connection")
        conn.close()

if __name__ == '__main__':
    test_basic_operations() 