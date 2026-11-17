import numpy as np
import cv2
import glob

CHECKBOARD = (6,9)

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objp = np.zeros((CHECKBOARD[0] * CHECKBOARD[1], 3), np.float32)
objp[:,:2] = np.mgrid[0:CHECKBOARD[0], 0:CHECKBOARD[1]].T.reshape(-1, 2)

objpoints = []
imgpoints = []

print("Iniciando captura para calibração...")
print("Mostre o tabuleiro de xadrez em diferentes ângulos")
print("Pressione 'espaço' para capturar uma imagem")
print("Pressione 'q' para sair")

cap = cv2.VideoCapture(1)
img_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Coletando Imagens", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break
    elif key == ord(' '):
        ret_corners, corners = cv2.findChessboardCorners(gray, CHECKBOARD, None)

        if ret_corners == True:
            objpoints.append(objp)

            corners_refined = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
            imgpoints.append(corners_refined)

            cv2.drawChessboardCorners(frame, CHECKBOARD, corners_refined, ret_corners)

            img_name = f"calibracao/img_{img_count}.png"
            cv2.imwrite(img_name, frame)
            print(f"Imagem {img_name} capturada e salva")
            img_count += 1
        else:
            print("Cantos não detectados. Tente um ângulo melhor")

cap.release()
cv2.destroyAllWindows()

print(f"\nIniciando calibração com {len(objpoints)} imagens...")

if len(objpoints) < 5:
    print("Erro: Calibração requer pelo menos 5 imagens")
    exit()

ret_cal, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

if ret_cal:
    print("Calibração bem-sucedida")

    np.savez('calibracao_camera.npz', mtx=mtx, dist=dist)
    print("Resultados salvos em 'calibracao_camera.npz'")


    mean_error = 0
    for i in range(len(objpoints)):
        imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
        mean_error += error
    print(f"Erro médio de reprojeção total: {mean_error/len(objpoints)}")

else:
    print("Calibração falhou")