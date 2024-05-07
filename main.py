import src
app = src.start()
# ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
# ssl_context.load_cert_chain('cert.pem', 'key.pem')
# app.run(host='0.0.0.0', port=5000, ssl_context=ssl_context)

app.run(debug=True, host="0.0.0.0", port=3000)
# app.run(debug=True, port=3000)
