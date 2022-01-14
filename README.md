# boarboardash-elasticsearch

## 目录结构

- /api.py：向外暴露api的服务端入口
- /config_example.py：配置文件的例子，不会加载
- /config.py：实际加载的配置文件
- /create_index.py：创建elasticsearch的索引，只需要执行一次
- /image_hash.py：计算图像hash的模块
- /init_database.py：初始化数据库，只需要执行一次
- /models.py：定义数据库的对象类型
- /search_images.py：搜索图片的模块
- /search_news.py：搜索新闻的模块
- /start-es.sh：启动elasticsearch的脚本
- /stop-es.sh：停止elasticsearch的脚本
- /enable-es.sh：设置开机自动启动elasticsearch的脚本
- /start-server.sh：启动服务器的脚本
- /conda_env.yaml：conda环境的依赖清单