DELETE FROM magazine WHERE id = 1;
INSERT INTO magazine (id, title , description, content_path, published_at, author, read_time, issue)
VALUES (
    1,
    'AI周刊：第20期',
    '本周AI领域热点汇总',
    'magazine_contents/1.html',
    '2025年8月4日',
    'AILab编辑部',
    '5分钟',
    '2024-20'
);