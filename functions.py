# 라이브러리 로드
import cv2
import numpy as np


# 1. 문서 영역 자동 추출 + 투시 변환
# 엣지 검출(Canny) -> 큰 외곽선(Contour) 중 사각형(4변)을 찾기 -> 투시변환(Perspective Transform)

def detect_document_contour(image):
  # 1) 그레이 + 블러 + 엣지
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  blurred = cv2.GaussianBlur(gray, (5, 5), 0)
  edged = cv2.Canny(blurred, 75, 200)

  # 2) 외곽선 찾기
  contours, _ = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
  contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]

  for c in contours:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)

    if len(approx) == 4:
      return approx.reshape(4, 2)
    
  return None



# 2. 4개의 점을 좌상/우상/우하/좌하 순서로 정렬 -> 원하는 크기의 직사각형으로 warp

def order_points(pts):
  rect = np.zeros((4, 2), dtype="float32")

  s = pts.sum(axis=1)
  diff = np.diff(pts, axis=1)

  rect[0] = pts[np.argmin(s)]  # 좌상
  rect[2] = pts[np.argmax(s)]  # 우하
  rect[1] = pts[np.argmin(diff)]  # 우상
  rect[3] = pts[np.argmax(diff)]  # 좌하

  return rect


def four_point_transform(image, pts):
  rect = order_points(pts)
  (tl, tr, br, bl) = rect

  widthA = np.linalg.norm(br - bl)
  widthB = np.linalg.norm(tr - tl)
  maxWidth = max(int(widthA), int(widthB))

  heightA = np.linalg.norm(tr - br)
  heightB = np.linalg.norm(tl - bl)
  maxHeight = max(int(heightA), int(heightB))

  dst = np.array([
      [0, 0],
      [maxWidth - 1, 0],
      [maxWidth - 1, maxHeight - 1],
      [0, maxHeight - 1]], dtype="float32")

  M = cv2.getPerspectiveTransform(rect, dst)
  warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

  return warped



# 3. 그림자 / 조명 보정
# 3-1. 컬러 그림자 제거용 간단 함수
def remove_shadow_color(image):
  rgb_planes = cv2.split(image)
  result_norm_planes = []

  for plane in rgb_planes:
    dilated = cv2.dilate(plane, np.ones((7,7), np.uint8))
    bg = cv2.medianBlur(dilated, 21)
    diff = 255 - cv2.absdiff(plane, bg)
    result_norm_planes.append(diff)

  result = cv2.merge(result_norm_planes)
  return result


# 3-2. 흑백 문서용(조명 보정 + 대비 향상)
def remove_shadow_gray(image):
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  bg = cv2.medianBlur(gray, 21)
  corrected = cv2.divide(gray, bg, scale=255)

  clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
  enhanced = clahe.apply(corrected)

  return enhanced


# 4. Onix / Magic Color 효과
# color : 그림자 제거 + 색/대비 보정
# gray : 좋은 회색 스캔
# bw : 강한 이진화 문서모드(프린트물)
# onix : gray + 강한 sharpen + 톤 조절

def enhance_document(image, mode='onix'):

  shadow_free = remove_shadow_color(image)

  if mode == 'color':

    lab = cv2.cvtColor(shadow_free, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    cl = clahe.apply(l)
    limg = cv2.merge((cl,a,b))
    result = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    return result
  
  gray = cv2.cvtColor(shadow_free, cv2.COLOR_BGR2GRAY)

  if mode == 'gray':
    return gray
  
  if mode == 'bw':
    bw = cv2.adaptiveThreshold(gray, 
                               255, 
                               cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY,
                               25, 15
                                )
    return bw
  
  if mode == 'onix':
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    cl = clahe.apply(gray)

    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    sharp = cv2.filter2D(cl, -1, kernel)

    return sharp
  
  return shadow_free



# 5. 필기 제거 기능(컬러 필기 / 형광펜 위주)

def remove_colored_writing(image):
  hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
  h, s, v = cv2.split(hsv)

  mask = (s > 60) & (v < 230)
  mask = mask.astype(np.uint8) * 255

  kernal = np.ones((3,3), np.uint8)
  mask = cv2.dilate(mask, kernal, iterations=1)
  mask = cv2.medianBlur(mask, 5)

  cleaned = cv2.inpaint(image, mask, 3, cv2.INPAINT_TELEA)
  return cleaned, mask



# 6. 전체 파이프라인 함수

def scan_document(image,
                  mode='onix',
                  auto_crop=True,
                  remove_colored_nptes=False,
                  ):
  
    """
    image: BGR(OpenCV) 이미지
    mode: 'onix', 'color', 'gray', 'bw'
    auto_crop: 문서 윤곽 자동 검출 + 투시 보정 여부
    remove_colored_notes: 컬러 필기 제거 여부
    """
  
    doc = image.copy()

    # 1) 문서 윤곽 자동 검출 + 투시 변환
    if auto_crop:
      cnt = detect_document_contour(doc)
      if cnt is not None:
        doc = four_point_transform(doc, cnt)

    # 2) 컬러 필기 제거
    mask = None
    if remove_colored_nptes:
      doc, mask = remove_colored_writing(doc)

    # 3) Onix /gray/bw/color 효과
    result = enhance_document(doc, mode=mode)

    return result, doc, mask