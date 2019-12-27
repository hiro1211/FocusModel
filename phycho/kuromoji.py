import esanpy

print("hello,world")
esanpy.start_server()
print("server start...")

tokens = esanpy.analyzer("今日の天気はハレです。", analyzer="kuromoji")
print(tokens)

esanpy.stop_server()
