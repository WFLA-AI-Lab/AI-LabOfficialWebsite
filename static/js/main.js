// 打字效果实现
document.addEventListener('DOMContentLoaded', function() {
    const textElement = document.querySelector('.typing-text');
    const text = "我们是世外首个专注于 AI 的学术社团。我们致力于传授使用、调试和开发的知识与经验，涵盖大模型与 Agent、神经网络、计算机视觉、传统机器学习等主题。活动包括知识讲座、项目实践、模型比赛等，配合社团联动，让 AI 成为你的创新工具。";
    let index = 0;
    let isDeleting = false;
    let isEnd = false;
    
    function typeEffect() {
        let randInterval = Math.random();
        const speed = isDeleting ? randInterval*50 : randInterval*100;
        
        if (isDeleting) {
            textElement.textContent = text.substring(0, index - 1);
            index--;
        } else {
            textElement.textContent = text.substring(0, index + 1);
            index++;
        }
        
        // 如果删除完了
        if (isDeleting && index === 0) {
            isDeleting = false;
            isEnd = false;
        } 
        // 如果打完了
        else if (!isDeleting && index === text.length) {
            isEnd = true;
            isDeleting = true;
            setTimeout(typeEffect, 2500); // 停留2.5秒
            return;
        }
        
        // 如果不是最后一次，继续打字
        if (!isEnd) {
            setTimeout(typeEffect, speed);
        }
    }
    
    // 开始打字效果

    setTimeout(typeEffect, 500);
});

// 为卡片添加鼠标悬停动画
document.querySelectorAll('.card-hover').forEach(card => {
    card.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-5px)';
        this.style.boxShadow = '0 10px 20px rgba(0, 0, 0, 0.1)';
    });
    
    card.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0)';
        this.style.boxShadow = '0 5px 15px rgba(0, 0, 0, 0.05)';
    });
});