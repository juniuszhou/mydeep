# deepagent

## buildin tools
deepagent 包含一些 buildin tools，比如 “ls, find” 这些。
它需要配合backend，普通的state backend，它不会写文件到本地硬盘。
需要使用FileSystem这种backend才行，而且需要知道可以更改的根目录。

## RAG as Tool
deepagents 支持 RAG，但主要方式是“把 retriever 当 tool 挂进去