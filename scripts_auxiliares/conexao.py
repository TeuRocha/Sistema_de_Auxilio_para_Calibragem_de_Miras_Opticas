import cv2

# Substitua pelo endereço IP exibido no aplicativo de câmera IP do seu smartphone
url = "http://0.0.0.0:8080/video"

cap = cv2.VideoCapture(url)

if not cap.isOpened():
    print("Erro: Não foi possível conectar à câmera do celular.")
    print("Verifique se o IP está correto e se o celular está na mesma rede Wi-Fi.")
else:
    print("Conexão estabelecida! Pressione 'q' para fechar.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Teste Camera IP", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()