# 数据库迁移和社刊目录提取脚本

本目录包含用于数据库迁移和社刊目录提取的脚本。

## 文件说明

- `magazine_toc.sql`: SQL脚本，用于向Magazine表添加toc字段
- `migrate_db.py`: Python脚本，用于执行SQL迁移脚本
- `extract_magazine_toc.py`: Python脚本，用于从社刊HTML文件中提取目录并更新到数据库

## 使用方法

### 1. 更新数据库结构

运行以下命令来更新数据库结构，添加toc字段：

```bash
python sql_scripts/migrate_db.py
```

### 2. 提取社刊目录并更新到数据库

运行以下命令来从社刊HTML文件中提取目录并更新到数据库：

```bash
python sql_scripts/extract_magazine_toc.py
```

## 依赖项

这些脚本依赖以下Python库：

- BeautifulSoup4: 用于解析HTML文件

可以使用以下命令安装：

```bash
pip install beautifulsoup4
```

## 注意事项

- 确保在运行脚本之前备份数据库文件
- 脚本假设社刊HTML文件位于 `templates/magazine/magazine_contents/` 目录下，文件名为 `{id}.html`
- 脚本假设数据库文件位于 `instance/ailab.db`