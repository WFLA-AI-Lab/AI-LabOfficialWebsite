// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 初始化代码高亮
    hljs.highlightAll();
    
    // 平滑滚动处理
    document.querySelectorAll('.toc-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 100, // 减去导航栏高度
                    behavior: 'smooth'
                });
                
                // 高亮当前激活的目录项
                document.querySelectorAll('.toc-link').forEach(item => {
                    item.classList.remove('toc-active');
                });
                this.classList.add('toc-active');
            }
        });
    });
    
    // 监听滚动，高亮当前可见的章节对应的目录项
    window.addEventListener('scroll', function() {
        const sections = document.querySelectorAll('.article-section');
        const scrollPosition = window.scrollY + 120; // 加上偏移量
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionId = section.getAttribute('id');
            const tocLink = document.querySelector(`.toc-link[href="#${sectionId}"]`);
            
            if (tocLink) {
                // 检查当前部分是否在视口中
                if (sectionTop <= scrollPosition && sectionTop + section.offsetHeight > scrollPosition) {
                    document.querySelectorAll('.toc-link').forEach(item => {
                        item.classList.remove('toc-active');
                    });
                    tocLink.classList.add('toc-active');
                }
            }
        });
    });
    
    // 初始化MathJax
    if (window.MathJax) {
        MathJax.typesetPromise().catch(err => {
            console.error('MathJax初始化错误:', err);
        });
    }
});
