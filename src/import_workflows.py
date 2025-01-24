import json
import logging
from pathlib import Path
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.structure.graph import Graph
from gremlin_python.driver.serializer import GraphSONMessageSerializer
from gremlin_python.process.graph_traversal import __

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class WorkflowImporter:
    def __init__(self, gremlin_url='ws://localhost:8182/gremlin'):
        self.graph = Graph()
        # 使用 GraphSON 序列化
        self.conn = DriverRemoteConnection(
            gremlin_url,
            'g',
            message_serializer=GraphSONMessageSerializer()
        )
        self.g = self.graph.traversal().withRemote(self.conn)
        logger.info(f"Connected to graph database at {gremlin_url}")
    
    def close(self):
        if self.conn:
            self.conn.close()
            logger.info("Closed database connection")
    
    def clear_database(self):
        """清空数据库中的所有数据"""
        self.g.V().drop().iterate()
        logger.info("Database cleared")
    
    def import_workflow(self, json_path):
        """导入单个工作流文件到图数据库"""
        try:
            # 读取JSON文件
            with open(json_path, 'r', encoding='utf-8') as f:
                workflow_data = json.load(f)
            
            workflow_name = Path(json_path).stem
            logger.info(f"\n正在导入工作流: {workflow_name}")
            
            # 创建工作流节点
            workflow_vertex = self.g.addV('workflow') \
                .property('name', workflow_name) \
                .property('file_path', str(json_path)) \
                .next()
            
            # 创建所有节点
            node_vertices = {}
            for node in workflow_data.get('nodes', []):
                node_id = str(node['id'])
                node_type = node['type']
                
                # 创建基本节点
                vertex = self.g.addV('node') \
                    .property('workflow', workflow_name) \
                    .property('node_id', node_id) \
                    .property('type', node_type) \
                    .next()
                
                node_vertices[node_id] = vertex
                logger.info(f"创建节点: {node_type} (ID: {node_id})")
            
            # 创建节点间的连接
            for node in workflow_data.get('nodes', []):
                node_id = str(node['id'])
                for input_info in node.get('inputs', []):
                    if 'link' in input_info and input_info['link'] is not None:
                        link_id = str(input_info['link'])
                        
                        # 找到源节点
                        for source_node in workflow_data['nodes']:
                            for output in source_node.get('outputs', []):
                                if output.get('links') and input_info['link'] in output['links']:
                                    source_id = str(source_node['id'])
                                    # 创建连接边
                                    self.g.V(node_vertices[source_id]) \
                                        .addE('connects_to') \
                                        .property('link_id', link_id) \
                                        .property('input_name', input_info['name']) \
                                        .property('output_name', output['name']) \
                                        .to(__.V(node_vertices[node_id])) \
                                        .iterate()
                                    logger.info(f"创建连接: {source_id} -> {node_id} (link: {link_id})")
            
            logger.info(f"工作流 {workflow_name} 导入完成")
            return workflow_vertex
            
        except Exception as e:
            logger.error(f"导入工作流 {json_path} 时出错: {str(e)}")
            raise
    
    def import_all_workflows(self, workflows_dir):
        """导入指定目录下的所有工作流"""
        workflows_path = Path(workflows_dir)
        for workflow_dir in workflows_path.iterdir():
            if workflow_dir.is_dir():
                for json_file in workflow_dir.glob('*.json'):
                    self.import_workflow(json_file)

def main():
    importer = None
    try:
        importer = WorkflowImporter()
        
        # 清空数据库
        importer.clear_database()
        
        # 导入所有工作流
        importer.import_all_workflows('src/workflows')
        
    except Exception as e:
        logger.error(f"导入过程中出错: {str(e)}")
    finally:
        if importer:
            importer.close()

if __name__ == '__main__':
    main() 