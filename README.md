# latexAutoBuild

使用WatchDog监听文件夹，当有新生成的tex文件时，使用`latexmk -xelatex`生成PDF。

---

```shell
# 在项目目录中
docker build -t [你的镜像名称] .
```

```shell
docker run -itd -v [宿主机路径]:/root/autolatex/file  [你的镜像名称]
```



在宿主机创建或修改tex文件，会自动在同目录下编译PDF。
