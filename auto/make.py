def convert2std(text, name):
    prefix = '''
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>计算机视觉基础与实践</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333;  margin: 0 auto; padding: 20px; }
        .article-header { margin-bottom: 40px; }
        .article-title { font-size: 2.5em; }
        .article-meta { font-size: 0.9em; color: #666; }
        .meta-item { margin-right: 15px; }
        .article-summary { background-color: #f8f9fa; border-radius: 8px; padding: 20px; }
        .summary-title { font-size: 1.2em; }
        .row { display: flex; }
        .col-md-3 { flex: 0 0 25%; max-width: 25%; }
        .col-md-9 { flex: 0 0 75%; max-width: 75%; padding-left: 20px; }
        .toc-container { background-color: #f8f9fa; padding: 20px; border-radius: 8px; position: sticky; top: 20px; }
        .toc-title { font-size: 1.2em; margin-bottom: 10px; }
        .toc-list { list-style: none; padding: 0; }
        .toc-link { text-decoration: none; color: #007bff; display: block; margin-bottom: 5px; }
        .article-section { margin-bottom: 40px; }
        .section-title { font-size: 1.8em; border-bottom: 2px solid #eee; padding-bottom: 10px; }
        .subsection-title { font-size: 1.4em; margin-top: 20px; }
        .section-text { margin-bottom: 15px; }
        .section-list { margin-bottom: 15px; }
        .math-equation { background-color: #f8f9fa; padding: 10px; border-radius: 4px; text-align: center; font-style: italic; }
        .image-container { text-align: center; }
        .article-image { max-width: 100%; height: auto; border-radius: 8px; }
        .image-caption { font-style: italic; color: #666; margin-top: 5px; }
        .code-block { background-color: #f8f9fa; padding: 15px; border-radius: 4px; overflow-x: auto; }
        code { font-family: Consolas, monospace; }
        pre { margin: 0; }
        </style>
    </head>
    '''
    postfix = '''
    </html>
    '''
    htmlfile = prefix + text + postfix
    with open(name, 'w', encoding='utf-8') as file:
        file.write(htmlfile)
    
    return name