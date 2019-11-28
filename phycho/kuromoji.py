import esanpy

esanpy.start_server()

tokens = esanpy.analyzer("今日の天気はハレです。", analyzer="kuromoji")
print(tokens)

esanpy.stop_server()
