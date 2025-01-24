import os
import json
import logging
import asyncio
import sys
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.structure.graph import Graph
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.traversal import T, P

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Windows平台特定的事件循环策略
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class WorkflowGraphImporter:
    def __init__(self, url='ws://localhost:8182/gremlin'):
        """初始化图数据库连接"""
        self.graph = Graph()
        self.connection = DriverRemoteConnection(url, 'g')
        self.g = self.graph.traversal().withRemote(self.connection)
        logger.info("已连接到JanusGraph数据库")

    def __del__(self):
        """析构函数，确保连接被正确关闭"""
        if hasattr(self, 'connection'):
            try:
                self.connection.close()
            except Exception as e:
                logger.warning(f"关闭连接时出现警告（可以忽略）: {str(e)}")

    def clear_graph(self):
        """清空图数据库"""
        self.g.V().drop().iterate()
        logger.info("已清空图数据库")

    def create_category_vertex(self, category_name, description):
        """创建类别顶点"""
        vertex = (self.g.addV('category')
                 .property('name', category_name)
                 .property('description', description)
                 .next())
        logger.info(f"创建类别: {category_name}")
        return vertex

    def create_workflow_vertex(self, workflow_name, file_path, description=""):
        """创建工作流顶点"""
        vertex = (self.g.addV('workflow')
                 .property('name', workflow_name)
                 .property('file_path', file_path)
                 .property('description', description)
                 .next())
        logger.info(f"创建工作流: {workflow_name}")
        return vertex

    def create_belongs_to_edge(self, workflow_vertex, category_vertex):
        """创建从工作流到类别的边"""
        self.g.V(workflow_vertex).addE('belongs_to').to(category_vertex).iterate()
        logger.info(f"创建关系: {workflow_vertex} -> {category_vertex}")

    def import_workflows(self):
        """导入工作流数据"""
        try:
            # 清空现有数据
            self.clear_graph()

            # 创建类别
            categories = {
                'basic': self.create_category_vertex('basic', '基础工作流'),
                'image_editing': self.create_category_vertex('image_editing', '图像编辑工作流'),
                'keying': self.create_category_vertex('keying', '抠图相关工作流'),
                'instant_id': self.create_category_vertex('instant_id', 'InstantID相关工作流')
            }

            # 创建工作流并建立关系
            workflows = [
                {
                    'name': 'basic',
                    'file_path': 'src/workflows/basic/basic.json',
                    'description': '基础示例工作流',
                    'category': 'basic'
                },
                {
                    'name': 'Local_redraw_SAM',
                    'file_path': 'src/workflows/image_editing/Local_redraw_SAM_course_workflow.json',
                    'description': '使用SAM进行局部重绘的工作流',
                    'category': 'image_editing'
                },
                {
                    'name': 'Keying',
                    'file_path': 'src/workflows/keying/Keying_Workflow.json',
                    'description': '多种抠图方法的综合工作流',
                    'category': 'keying'
                },
                {
                    'name': 'InstantID',
                    'file_path': 'src/workflows/instant_id/InstantID_comprehensively_explains_workflow.json',
                    'description': 'InstantID完整功能演示工作流',
                    'category': 'instant_id'
                }
            ]

            for workflow in workflows:
                # 创建工作流顶点
                workflow_vertex = self.create_workflow_vertex(
                    workflow['name'],
                    workflow['file_path'],
                    workflow['description']
                )
                # 创建与类别的关系
                self.create_belongs_to_edge(workflow_vertex, categories[workflow['category']])

            logger.info("所有工作流数据导入完成")

        except Exception as e:
            logger.error(f"导入过程中出错: {str(e)}")
            raise

def main():
    importer = None
    try:
        importer = WorkflowGraphImporter()
        importer.import_workflows()
    finally:
        if importer is not None:
            del importer

if __name__ == '__main__':
    main() 