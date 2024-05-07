import src
# import ssl
app = src.start()
# ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
# ssl_context.load_cert_chain('cert.pem', 'key.pem')
app.run(debug=True, host='0.0.0.0', port=3000)

# app.run(debug=True, port=3000)
