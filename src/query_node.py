import logging
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.structure.graph import Graph
from gremlin_python.driver.serializer import GraphSONMessageSerializer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyze_node(workflow_name, node_type):
    try:
        # 创建连接
        logger.info("Creating DriverRemoteConnection with url 'ws://localhost:8182/gremlin'")
        connection = DriverRemoteConnection('ws://localhost:8182/gremlin', 'g', 
                                          message_serializer=GraphSONMessageSerializer())
        logger.info("Creating Client with url 'ws://localhost:8182/gremlin'")
        logger.info("Creating GraphTraversalSource.")
        graph = Graph()
        g = graph.traversal().withRemote(connection)
        logger.info("Connected to graph database\n")

        # 查找指定工作流中的指定类型节点
        print(f"工作流: {workflow_name}")
        print(f"节点类型: {node_type}")
        
        # 使用正确的属性名称查询
        target_node = g.V().has('workflow', workflow_name).has('type', node_type).next()
        node_id = g.V(target_node).id_().next()
        print(f"\n目标节点ID: {node_id}")
        
        # 获取节点所有属性
        print("\n节点属性:")
        properties = g.V(target_node).valueMap().next()
        for key, value in properties.items():
            print(f"- {key}: {value[0]}")
        print()

        # 获取输入连接
        print("输入连接:")
        in_edges = g.V(target_node).inE('connects_to').as_('e').outV().as_('v').select('e','v').toList()
        if in_edges:
            for edge in in_edges:
                source_node = g.V(edge['v']).valueMap().next()
                print(f"\n- 从 {source_node.get('type', ['Unknown'])[0]} (ID: {g.V(edge['v']).id_().next()}) 节点")
                
                # 获取边的所有属性
                print("  边属性:")
                edge_element = g.E(edge['e'])
                edge_props = edge_element.elementMap().next()
                for key, value in edge_props.items():
                    if isinstance(key, str):  # 只打印字符串类型的键
                        print(f"  - {key}: {value}")
        else:
            print("- 无输入连接")
        print()

        # 获取输出连接
        print("输出连接:")
        out_edges = g.V(target_node).outE('connects_to').as_('e').inV().as_('v').select('e','v').toList()
        if out_edges:
            for edge in out_edges:
                target_node = g.V(edge['v']).valueMap().next()
                print(f"\n- 到 {target_node.get('type', ['Unknown'])[0]} (ID: {g.V(edge['v']).id_().next()}) 节点")
                
                # 获取边的所有属性
                print("  边属性:")
                edge_element = g.E(edge['e'])
                edge_props = edge_element.elementMap().next()
                for key, value in edge_props.items():
                    if isinstance(key, str):  # 只打印字符串类型的键
                        print(f"  - {key}: {value}")
        else:
            print("- 无输出连接")

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise
    finally:
        if 'connection' in locals():
            logger.info("\nclosing DriverRemoteConnection with url 'ws://localhost:8182/gremlin' ")
            logger.info("Closing Client with url 'ws://localhost:8182/gremlin'\n")
            connection.close()
            logger.info("Closed database connection")

if __name__ == "__main__":
    analyze_node("basic", "CheckpointLoaderSimple") 