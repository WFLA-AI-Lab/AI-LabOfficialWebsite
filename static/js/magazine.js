document.addEventListener('DOMContentLoaded', function() {
    const magazineItems = document.querySelectorAll('.magazine-item');
    const viewportHeight = window.innerHeight || document.documentElement.clientHeight;

    magazineItems.forEach((item, index) => {
        const rect = item.getBoundingClientRect();
        const isInInitialViewport = rect.top <= viewportHeight+1200;

        if (isInInitialViewport) {
            // 视口内的元素：添加延迟动画（保持层次感）
            setTimeout(() => {
                item.classList.add('animate');
            }, index * 200); // 依次延迟200ms，避免同时弹出
        } else {
            // 不在视口内的元素：直接显示（无动画）
            item.style.opacity = '1';
            item.style.transform = 'translateX(0)';
        }
    });
});