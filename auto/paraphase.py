from openai import OpenAI
import os,random,datetime
def extract_magazine(aiAPIkey):
    # 随机选择一个作者
    authors_list = ['李睿远','王思成','黄子淳','杨其臻']
    author = random.choice(authors_list)

    source_list = 'https://www.kdnuggets.com/, https://www.marktechpost.com/, https://www.unite.ai/'


    article_type_list = ["AI小众概念轻科普","AI行业/开发者资讯"]
    article_type = random.choice(article_type_list)

    api_key  = os.environ.get('OPENAI_API_KEY')



    client = OpenAI(
        api_key=aiAPIkey,
        base_url="https://api.deepseek.com",
    )

    system_prompt_content = f'''
    你是一个正在编写AI Lab社团社刊的人，你需要从指定的网站中找到适合{article_type}的文章。
    1.访问{source_list}，解析最近三天文章内容，查看是否适合做成{article_type}，且paraphase后最多不超过1500字，并选定文章。
    2.访问http://ai-lab.club/magazine，查看最近的{article_type}文章，查看是否有重复。若重复则返回第一步
    3.将文章内容划分成最多8个部分
    4.用中文复述选定的文章内容，并生成为一个<body></body>标签，允许使用
            <div class="image-container mb-6">
            <img src="" alt="" class="article-image">
            <p class="image-caption"></p>
            </div>
            插入图片，
            使用
            <div class="math-equation mb-4">
            </div>
            插入标准latex公式，
            使用
            <div class="code-block mb-6">
            <pre><code class="language-python">import torch
            #python code here
            </div>
            插入不同语言的代码块，
            使用
            <ul class="section-list">
            <li></li>
            <li></li>
            <li></li>
            </ul>
            插入连续列举列表，
            使用
            <h3 class="subsection-title"></h3>
            插入小标题
            使用
            <p class="section-text"></p>
            插入正文
            使用
            <section id="" class="article-section mb-10"></section>
            插入目录对应的部分，
            使用
            <aside class="col-md-3 mb-8">
            <div class="toc-container sticky-top">
                <h3 class="toc-title">目录</h3>
                <ul class="toc-list">
                    <li><a href="#intro" class="toc-link">引言</a></li>
                    <li><a href="#cnn" class="toc-link">卷积神经网络</a></li>
                    <li><a href="#image-classification" class="toc-link">图像分类</a></li>
                    <li><a href="#object-detection" class="toc-link">目标检测</a></li>
                    <li><a href="#implementation" class="toc-link">代码实现</a></li>
                    <li><a href="#conclusion" class="toc-link">结论</a></li>
                </ul>
            </div>
            </aside>
            插入目录，并取一个英文开头的#链接。
    5.使用
        <header class="article-header mb-10 text-center">
        <h1 class="article-title mb-4">标题</h1>
        <div class="article-meta mb-6">
            <span id="published_at" class="meta-item">发布日期: 20XX年X月X日</span>
            <span id="author" class="meta-item">作者: XXX</span>
            <span id="read_time" class="meta-item">阅读时间: XX分钟</span>
        </div>
        <div class="article-summary max-w-3xl mx-auto p-4 bg-light rounded">
            <h3 class="summary-title mb-2">摘要</h3>
            <p>50字左右的摘要</p>
        </div>
        </header>
    插入文章简介信息，其中发布日期为{datetime.date.today()}，作者为{author}，阅读时间为可自己计算，标题和摘要自己取一个。


    '''
    system_prompt_answer_input = rf'''
    SAMPLE_OUTPUT:
    <body>

    <!-- 文章头部信息 -->
    <header class="article-header mb-10 text-center">
        <h1 class="article-title mb-4">计算机视觉基础与实践</h1>
        <div class="article-meta mb-6">
            <span id="published_at" class="meta-item">发布日期: 2025年8月7日</span>
            <span id="author" class="meta-item">作者: 黄梓淳</span>
            <span id="read_time" class="meta-item">阅读时间: 15分钟</span>
        </div>
        <div class="article-summary max-w-3xl mx-auto p-4 bg-light rounded">
            <h3 class="summary-title mb-2">摘要</h3>
            <p>本文介绍了计算机视觉的基础知识，包括卷积神经网络、图像分类和目标检测等，并通过实际代码示例展示了这些技术的应用。我们将探讨每种技术的原理、优缺点及适用场景，帮助读者快速掌握计算机视觉的核心概念和实践技能。本文还包含了代码实现示例，并补充了各技术的优缺点分析，以提供更全面的理解。</p>
        </div>
    </header>

    <div class="row">
        <!-- 左侧目录 -->
        <aside class="col-md-3 mb-8">
            <div class="toc-container sticky-top">
                <h3 class="toc-title">目录</h3>
                <ul class="toc-list">
                    <li><a href="#intro" class="toc-link">引言</a></li>
                    <li><a href="#cnn" class="toc-link">卷积神经网络</a></li>
                    <li><a href="#image-classification" class="toc-link">图像分类</a></li>
                    <li><a href="#object-detection" class="toc-link">目标检测</a></li>
                    <li><a href="#implementation" class="toc-link">代码实现</a></li>
                    <li><a href="#conclusion" class="toc-link">结论</a></li>
                </ul>
            </div>
        </aside>

        <!-- 右侧内容区 -->
        <article class="col-md-9 article-content">
            <!-- 引言部分 -->
            <section id="intro" class="article-section mb-10">
                <h2 class="section-title">引言</h2>
                <p class="section-text">计算机视觉是人工智能的一个关键领域，它使计算机能够“看到”和解释视觉世界。近年来，计算机视觉在自动驾驶、医疗成像和人脸识别等方面取得了显著进展。</p>
                <p class="section-text">本文将介绍计算机视觉的基础知识，包括：</p>
                <ul class="section-list">
                    <li>卷积神经网络 - 计算机视觉的核心架构</li>
                    <li>图像分类 - 如ResNet模型</li>
                    <li>目标检测 - 如YOLO模型</li>
                </ul>
                <p class="section-text">这些技术是理解更先进视觉系统（如扩散模型）的基础，掌握它们对于深入学习计算机视觉至关重要。</p>
            </section>

            <!-- 卷积神经网络部分 -->
            <section id="cnn" class="article-section mb-10">
                <h2 class="section-title">卷积神经网络</h2>
                <p class="section-text">卷积神经网络（CNN）是一种专为处理图像数据设计的神经网络架构。它通过卷积层、池化层和全连接层提取图像特征。卷积操作使用内核扫描图像以检测边缘、纹理等局部模式。</p>
                
                <h3 class="subsection-title">卷积操作</h3>
                <p class="section-text">卷积公式如下：</p>
                
                <div class="math-equation mb-4">
                    \( (f * g)(i,j) = \sum_{{m}} \sum_{{n}} f(m,n) g(i-m, j-n) \)
                </div>
                
                <p class="section-text">其中，\( f \)是输入图像，\( g \)是卷积核。</p>
                
                <!-- 优缺点 -->
                <h3 class="subsection-title">优缺点</h3>
                <ul class="section-list">
                    <li>优点：参数共享减少计算量，平移不变性强，层次化特征提取。</li>
                    <li>缺点：对旋转/缩放敏感，需要大量数据，解释性较差。</li>
                </ul>
                
                <div class="image-container mb-6">
                    <img src="https://picsum.photos/800/400?random=7" alt="CNN架构图" class="article-image">
                    <p class="image-caption">图1: 卷积神经网络的基本架构，显示了卷积和池化层</p>
                </div>
            </section>

            <!-- 图像分类部分 -->
            <section id="image-classification" class="article-section mb-10">
                <h2 class="section-title">图像分类</h2>
                <p class="section-text">图像分类是将图像分配到预定义类别的任务。ResNet等模型通过残差连接解决深度网络的梯度消失问题，提高了分类准确率。</p>
                
                <h3 class="subsection-title">残差块</h3>
                <p class="section-text">残差连接公式：</p>
                
                <div class="math-equation mb-4">
                    \( y = F(x) + x \)
                </div>
                
                <p class="section-text">其中，\( F(x) \)是残差函数，\( x \)是输入。</p>
                
                <div class="image-container mb-6">
                    <img src="https://picsum.photos/800/400?random=8" alt="ResNet残差块图" class="article-image">
                    <p class="image-caption">图2: ResNet中的残差块结构</p>
                </div>
                
                <!-- 优缺点 -->
                <h3 class="subsection-title">优缺点</h3>
                <ul class="section-list">
                    <li>优点：高准确率，易于训练深层网络，广泛应用。</li>
                    <li>缺点：计算密集，需标注数据，对小物体敏感。</li>
                </ul>
            </section>

            <!-- 目标检测部分 -->
            <section id="object-detection" class="article-section mb-10">
                <h2 class="section-title">目标检测</h2>
                <p class="section-text">目标检测不仅分类图像，还定位物体边界框。YOLO（You Only Look Once）是一种实时检测模型，将检测视为单一回归问题。</p>
                
                <h3 class="subsection-title">YOLO原理</h3>
                <p class="section-text">YOLO将图像分成网格，每个网格预测边界框和类概率。</p>
                
                <div class="math-equation mb-4">
                    \( \text{{Loss}} = \lambda_{{coord}} \sum (x_i - \hat{{x}}_i)^2 + \sum (p_i - \hat{{p}}_i)^2 + \dots \)
                </div>
                
                <p class="section-text">损失函数包括坐标误差、置信度误差和分类误差。</p>
                
                <!-- 优缺点 -->
                <h3 class="subsection-title">优缺点</h3>
                <ul class="section-list">
                    <li>优点：实时速度快，端到端训练，全局上下文。</li>
                    <li>缺点：小物体检测弱，重叠物体处理差，需平衡速度与精度。</li>
                </ul>
                
                <div class="image-container mb-6">
                    <img src="https://picsum.photos/800/400?random=9" alt="YOLO检测图" class="article-image">
                    <p class="image-caption">图3: YOLO目标检测示例，显示了边界框和类别</p>
                </div>
            </section>

            <!-- 代码实现部分 -->
            <section id="implementation" class="article-section mb-10">
                <h2 class="section-title">代码实现</h2>
                <p class="section-text">下面我们使用Python和PyTorch库实现上述技术。首先，我们需要导入必要的库（假设已安装torch和torchvision）：</p>
                
                <div class="code-block mb-6">
                    <pre><code class="language-python">import torch
    import torch.nn as nn
    import torchvision
    import torchvision.transforms as transforms
    from torchvision.models.detection import fasterrcnn_resnet50_fpn</code></pre>
                </div>
                
                <h3 class="subsection-title">简单CNN实现</h3>
                <p class="section-text">构建一个基本CNN用于图像分类：</p>
                
                <div class="code-block mb-6">
                    <pre><code class="language-python">class SimpleCNN(nn.Module):
        def __init__(self):
            super().__init__()
            self.conv1 = nn.Conv2d(3, 32, 3, padding=1)
            self.pool = nn.MaxPool2d(2, 2)
            self.fc1 = nn.Linear(32 * 16 * 16, 10)  # 假设32x32输入

        def forward(self, x):
            x = self.pool(torch.relu(self.conv1(x)))
            x = x.view(-1, 32 * 16 * 16)
            x = self.fc1(x)
            return x

    model = SimpleCNN()
    print(model)</code></pre>
                </div>
                
                <h3 class="subsection-title">图像分类实现</h3>
                <p class="section-text">使用预训练ResNet进行分类：</p>
                
                <div class="code-block mb-6">
                    <pre><code class="language-python"># 加载预训练模型
    model = torchvision.models.resnet18(pretrained=True)
    model.eval()

    # 示例输入
    transform = transforms.Compose([transforms.Resize(256), transforms.CenterCrop(224), transforms.ToTensor()])
    # 假设img是PIL图像
    # output = model(transform(img).unsqueeze(0))</code></pre>
                </div>
                
                <h3 class="subsection-title">目标检测实现</h3>
                <p class="section-text">使用Faster R-CNN进行目标检测：</p>
                
                <div class="code-block mb-6">
                    <pre><code class="language-python"># 加载预训练模型
    model = fasterrcnn_resnet50_fpn(pretrained=True)
    model.eval()

    # 示例输入
    # 假设images是张量列表
    # predictions = model(images)</code></pre>
                </div>
            </section>

            <!-- 结论部分 -->
            <section id="conclusion" class="article-section mb-10">
                <h2 class="section-title">结论</h2>
                <p class="section-text">本文介绍了计算机视觉的基础：卷积神经网络、图像分类和目标检测。这些技术在视觉任务中表现出色，是现代AI系统的基石。</p>
                <p class="section-text">每种技术都有其适用场景：</p>
                <ul class="section-list">
                    <li>CNN适用于特征提取，如边缘检测</li>
                    <li>图像分类适用于类别识别，如物种分类</li>
                    <li>目标检测适用于定位物体，如自动驾驶</li>
                </ul>
                <p class="section-text">在实际应用中，选择合适的模型并通过数据增强优化性能。建议读者通过实践代码进一步实验，并探索高级主题如GAN和视觉Transformer。</p>
            </section>
        </article>
    </div>

    </body>
    你需要严格遵守其中的类名和标签名，不能改变，直接输出body标签即可，外面不要套东西，图片需要是真实描述概念的图片，宁可不要图片也不要插入无关或随机图片，内容和目录自己生成。
    '''


    system_prompt = system_prompt_content + '\n' + system_prompt_answer_input

    user_prompt = "请获取一篇文章"

    messages = [{"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}]

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        # response_format={
        #     'type': 'json_object'
        # }
    )

    return response.choices[0].message.content