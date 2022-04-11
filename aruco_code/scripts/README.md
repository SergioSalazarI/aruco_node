# Aruco node
El nodo correspondiente a la detección de arucos es el archivo aruco_receiver.py.
El nodo se subscribe a un tópico cuyo contenido es una imagen de la cámara. El nombre del tópico es '/cam1'.
El nodo encargado de publicar la imagen en el tópico es aruco_streamer.py.
