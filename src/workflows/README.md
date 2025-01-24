# ComfyUI 工作流集合

本目录包含了各种用途的ComfyUI工作流文件，按功能分类组织。

## 目录结构

- `basic/` - 基础工作流
  - `basic.json` - 基础示例工作流
  
- `image_editing/` - 图像编辑工作流
  - `Local_redraw_SAM_course_workflow.json` - 使用SAM进行局部重绘的工作流
  
- `keying/` - 抠图相关工作流
  - `Keying_Workflow.json` - 多种抠图方法的综合工作流
  
- `instant_id/` - InstantID相关工作流
  - `InstantID_comprehensively_explains_workflow.json` - InstantID完整功能演示工作流

## 使用说明

1. 这些工作流文件可以直接导入到ComfyUI中使用
2. 每个工作流都针对特定的使用场景进行了优化
3. 部分工作流可能需要安装额外的节点或模型

## 注意事项

- 使用工作流前请确保已安装所需的所有依赖
- 部分工作流可能需要较大的GPU内存
- 建议先阅读每个工作流的具体说明再使用 