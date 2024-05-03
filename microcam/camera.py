import cv2



video_capture = cv2.VideoCapture('rtsp://192.168.0.118:554/user=admin_password=tlJwpbo6_channel=1_stream=1&amp;onvif=0.sdp?real_st')  # 0 for web camera live stream
#  for cctv camera'rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp'



def camera_stream():
     # Capture frame-by-frame
    ret, frame = video_capture.read()
    # Display the resulting frame in browser
    return cv2.imencode('.jpg', frame)[1].tobytes()
