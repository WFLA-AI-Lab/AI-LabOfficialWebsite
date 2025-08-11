// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 初始化代码高亮
    hljs.highlightAll();
    
    // 获取后端传递的目录数据（如果有）
    const tocDataElement = document.getElementById('toc-data');
    let tocData = null;
    
    if (tocDataElement) {
        try {
            tocData = JSON.parse(tocDataElement.textContent);
            console.log('目录数据从页面加载成功:', tocData);
            // 使用目录数据更新UI
            updateTocUI(tocData);
        } catch (e) {
            console.error('目录数据解析错误:', e);
            // 如果页面中的目录数据解析失败，尝试从API获取
            fetchTocFromAPI();
        }
    } else {
        // 如果页面中没有目录数据，尝试从API获取
        fetchTocFromAPI();
    }
    
    // 从API获取目录数据
    function fetchTocFromAPI() {
        // 从URL中获取社刊ID
        const pathParts = window.location.pathname.split('/');
        const magazineId = pathParts[pathParts.length - 1];
        
        if (magazineId && !isNaN(magazineId)) {
            fetch(`/api/magazine/${magazineId}/toc`)
                .then(response => response.json())
                .then(data => {
                    if (data.success && data.toc) {
                        console.log('目录数据从API加载成功:', data.toc);
                        tocData = data.toc;
                        // 使用目录数据更新UI
                        updateTocUI(tocData);
                    } else {
                        console.warn('API返回错误:', data.error || '未知错误');
                    }
                })
                .catch(error => {
                    console.error('获取目录数据失败:', error);
                });
        }
    }
    
    // 使用目录数据更新UI
    function updateTocUI(tocData) {
        if (!tocData) return;
        
        // 这里可以根据需要更新UI
        // 例如，可以动态创建目录列表，或者增强现有的目录功能
        // 目前我们只是确保目录数据可用，不做额外的UI更新
    }
    
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
