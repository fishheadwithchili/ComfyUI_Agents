import logging
import sys
import asyncio
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.structure.graph import Graph

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Windows平台特定的事件循环策略
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class WorkflowImporter:
    def __init__(self, host='localhost', port=8182):
        self.url = f'ws://{host}:{port}/gremlin'
        self.connection = None
        self.g = None

    def connect(self):
        """连接到JanusGraph"""
        try:
            graph = Graph()
            self.connection = DriverRemoteConnection(self.url, 'g')
            self.g = graph.traversal().withRemote(self.connection)
            logger.info("已连接到JanusGraph")
            return True
        except Exception as e:
            logger.error(f"连接失败: {str(e)}")
            return False

    def import_workflow(self, name, description, category_name, file_path):
        """导入工作流"""
        try:
            # 检查类别是否存在
            category = self.g.V().hasLabel('category').has('name', category_name).next()
            logger.info(f"找到类别: {category_name}")

            # 检查工作流是否已存在
            existing = self.g.V().hasLabel('workflow').has('name', name).toList()
            if existing:
                logger.info(f"工作流 {name} 已存在，跳过导入")
                return True

            # 创建工作流顶点并直接添加关系
            self.g.addV('workflow').property('name', name) \
                .property('description', description) \
                .property('file_path', file_path) \
                .addE('belongs_to').to(category).iterate()
                
            logger.info(f"创建工作流和关系: {name} -> {category_name}")
            return True
        except Exception as e:
            logger.error(f"导入工作流失败: {str(e)}")
            return False

    def close(self):
        """关闭连接"""
        if self.connection:
            self.connection.close()

def main():
    # 创建一个新的工作流
    new_workflow = {
        'name': 'text2img_face_hand_redraw',
        'description': '使用ControlNet进行人脸和手部重绘的工作流',
        'category': 'image_editing',
        'file_path': 'src/test_output/text2img_face_hand_redraw_workflow.json'
    }

    importer = WorkflowImporter()
    try:
        if importer.connect():
            success = importer.import_workflow(
                new_workflow['name'],
                new_workflow['description'],
                new_workflow['category'],
                new_workflow['file_path']
            )
            if success:
                logger.info("工作流导入成功")
            else:
                logger.error("工作流导入失败")
    finally:
        importer.close()

if __name__ == '__main__':
    main() 