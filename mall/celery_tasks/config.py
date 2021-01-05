# 我们使用redid做我们的中间人
# 中间人选择redis的14号库，执行结果保存到15号库
broker_url = "redis://127.0.0.1/14"
result_backend = "redis://127.0.0.1/15"