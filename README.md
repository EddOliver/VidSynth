# VidSynth: Real Time AI Video Generator

<img src="https://i.ibb.co/PCWKPdj/VidSynth.png" width="1000">

# Problem
 
There is a lack of photo and video cameras that really use powerful AI algorithms, from segmentation to stable diffusion. There are several solutions right now that use AI to improve the image but not much to analyze it or to make changes in REAL TIME.

# Materials:

Hardware:
- NVIDIA Jetson Nano Orin.                                x1.
https://developer.nvidia.com/embedded/learn/get-started-jetson-orin-nano-devkit

Software:
- Docker:
https://www.docker.com/
- JetPack 5.1.3:
https://developer.nvidia.com/embedded/jetpack-sdk-513
- Stable Diffusion:
https://huggingface.co/CompVis/stable-diffusion-v1-4
- OpenCV:
https://opencv.org/
- VScode:
https://code.visualstudio.com/

# Introduction:

En el mundo cada vez más digital, el consumo de contenido en video se ha vuelto una parte fundamental de nuestra rutina diaria. Muchas plataformas han transformado la forma en que consumimos información, entretenimiento y educación, ofreciendo una amplia gama de contenido que va desde tutoriales y vlogs hasta series y películas. 

<img src="https://i.ibb.co/cLxJHTj/Image.png" width="1000">

Sin emabargo con el avance de las GAI (generative artificial intelligence), ha permitido una revolucion en la forma de genera contenido, ya que ahora es posible generar imagenes, audios y videos de alta calidad desde la comodidad de tu hogar. Esto no solo democratiza la creación de contenido, permitiendo a personas con menos recursos acceder a herramientas de producción de alta calidad, sino que también abre nuevas posibilidades creativas al desafiar los límites de lo que es posible generar de manera automatizada. 

<img src="https://i.ibb.co/9yqv3Ww/image.png" width="1000">

Por eso hoy te presento VidSynth: Real Time AI Video Generator.

# Solution:

Realice una pequeña workstation mediante CLI que nos permite de forma sencilla realizar el proceso de pasar todas las images de un video en un modelo de stable diffusion como el SD-1.4.

<img src="https://i.ibb.co/mhG5sxC/image.png" width="1000">

A su vez con OpenCV es posible realizar denuevo la composicion del video orginal una vez ha pasado por la red de stable diffusion.

<img src="https://i.ibb.co/HtQwbFf/Image.png" width="1000">

# General Scheme:

<img src="https://i.ibb.co/2NjLjpk/Scheme-Vid-Synth.png" width="1000">

- La funcion principal de la Jetson Orin Nano es ser el procesador CPU y GPU de mi proyecto.

- Como sistema operativo de la board utilice Jetpack 5.1.3, explicare mas adelante porque esta version.

- Utilice el orquestador de contenedores nativo de Docker, Docker Compose Plugin.

- Finalmente los contenedores que utilice fueron Stable Diffusion y OpenCV, los cuales estan compilados ya para la Jetson Nano Orin.

# Board Setup:

Primero vamos a realizar el setup de la board y workspace para hacer funcionar correctamente los contenedores.

## NVME SSD:

Uno de lo requisitos previos a desplegar este prpyecto es realizar el setup de una SSD NVME en la Jetson Nano, debido a que mejorara el rendimiento de la trajeta.

<img src="https://i.ibb.co/6ZsZfRQ/20240330-190849.jpg" width="1000">

La NVME tiene que ir colocada en el puerto correcto, igualmente puedes usar una trajeta NVME mini, pero su precio es bastante mas elevado que los SSD NVME tradicionales.

<img src="https://i.ibb.co/nDYSJMH/20240330-190910.jpg" width="1000">

Recuerda Revisar que el puerto sea de tipo M, cualquier otro tipo de puerto, no va a funcionar.

<img src="https://i.ibb.co/nQmVXPR/20240330-190939.jpg" width="1000">

## OS Setup and Flash:

Como primer paso tendremos que poner un jumper en el puerto FC y GND de los headers traseros d ela trajeta, esto con el fin de que nos permita relizar correctamente el flash del OS.

<img src="https://i.ibb.co/1Mk1zqK/20240330-191009.jpg" width="1000">

Se uso el SDK Manager de Nvidia para faicilitar la instalacion del OS. Sin embargo este proceso debe de ser echo en una maquina linux, asi que recomiendo utilizar una maquina virtual con Ubuntu para realizar este proceso, **utilice VMware debido a que Virtual Box no funciono para este proceso**.

<img src="https://i.ibb.co/6Zxspkz/Screenshot-2024-03-14-190814.png" width="1000">

Es importante que este instalado el runtime de contenedores, sin el no podremos hacer funcionar el proyecto, ademas que el configurarlo manualmente puede ser muy complicado.

<img src="https://i.ibb.co/s1FnXd0/Image-13.png" width="1000">

## Software Setup:

Lo primero que tenemos que hacer una vez tenemos el sistema listo, es conectarnos por SSH a la board, particularmente con VScode manipular los contenedores de forma grafica es muy sencillo.

<img src="https://i.ibb.co/dfYhd2S/image.png" width="1000">

Ahora realizaremos la descarga e instalacion de los scripts necesarios para el funcionamiento de los contenedores.

    sudo apt-get update && sudo apt-get install git python3-pip
    git clone --depth=1 https://github.com/dusty-nv/jetson-containers
    cd jetson-containers
    pip3 install -r requirements.txt

Debido al tamaño de los modelos de Stable Diffusion, tendremos que crear una memoria swap con los siguientes comandos.

    sudo systemctl disable nvzramconfig
    sudo fallocate -l 16G /mnt/16GB.swap
    sudo mkswap /mnt/16GB.swap
    sudo swapon /mnt/16GB.swap

Ahora, en Jetpack 5.1.3 tenemos el problema que Docker no provee el script de Docker Compose, asi que tendremos que instalarlo manualmete.

- Instalamos los keyrings oficiales de docker.

        sudo mkdir -p /etc/apt/keyrings
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

- Agreamos docker al gestor de paquetes apt.

        sudo echo  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

- Finalmente instalamos el plugin de docker compose.

        sudo apt update
        sudo apt install -y docker-compose-plugin

Por ultimo, tendremos que agregar Docker a los User Group para evitar la necesidad de `sudo` al usar docker.

    sudo usermod -aG docker $USER

## Containers Download and Run:

Es bastante sencillo bajar los contenedores al correr el siguiente comando.

    cd jetson-containers
    ./run.sh $(./autotag opencv)

Gracias a este comando bajaremos el contenedor de OpenCV.

<img src="https://i.ibb.co/8sXSvLC/image.png" width="1000">

Y de la misma forma bajaremos el contenedor de Stable Diffusion.

    cd jetson-containers
    ./run.sh $(./autotag stable-diffusion)

Ya despues de estos comandos ya podremos utilizar las herramientas de Stable Diffusion y OpenCV sin problema.

<img src="https://i.ibb.co/vwyTmd4/image.png" width="1000">

# Video Creation:

Lo primero que tendremos que hacer para realizar la edicion de un video, sera bajar la carpeta [server](./server/) de este repositorio y pegarla en la Jetson Orin Nano.

<img src="https://i.ibb.co/7NJvN9w/Image.png" width="700">

En esta carpeta ya tendremos todos los archivos necesarios para utilizar el proyecto, unicamente tendremos que entrar a la carpeta server y ejecutar el comando. Recomendaria revisar el archivo [docker-compose.yml](./server/docker-compose.yml) para revisar los detalles de ejecucion.

    docker compose up -d

Este comando ejecutara los dos contenedores de OpenCV y Stable-Diffusion con todo configurado y listo para funcionar.

<img src="https://i.ibb.co/hFyFstH/image.png" width="1000">

Ya con ambos contenedores funcionando y conectados, vamos a realizar primero la conversion de un video a imagenes mediante OpenCV, dentro de la carpeta de input pondremos el video a editar, en este caso un vuelo de un drone. 

<img src="https://i.ibb.co/WH3t26M/image.png" width="1000">

La conversion de video a imagenes se realiza con e siguiente comando.

    python3 video2imgs.py

Una vez ejecutado el comando todos los frames de el video estaran ahor en la carpeta framesin

<img src="https://i.ibb.co/SJphMn8/image.png" width="1000">

Ahora que tenemos el video en frames, en el contenedor de Stable Diffusion ejecutaremos el siguiente comando, el cual iniciara el proceso de conversion de cada frame con el modelo de stable diffusion.

    python3 img2img.py --n_samples 1 --n_iter 1 --ddim_steps 40 --init-path /framesin --outdir /framesout --prompt "flying space ship, starwars, speed, racer, drone, space, cyberpunk, cyber, masterpiece,best quality,ultra high res,raw photo,beautiful lighting, realistic, photo-realistic, illustration, ultra-detailed, photorealistic, sharp focus, highly detailed, professional lighting, colorful details, iridescent colors, intricate details, 8k uhd, high quality, dramatic, cinematic" --strength 0.3 --seed 10000 --increase 0 &

En este caso los invito a modificar los parametros de el comando para mejorar resultados, especialmente strength y prompt.

<img src="https://i.ibb.co/gFC9dkD/image.png" width="1000">

Segun el modelo de jetson que tengas este proceso puede tardar mucho, recomendamos la Jetson Orin AGX como base para trabajar estos archivos de video.

Una vez terminado el procesamiento, iremos denuevo al contenedor de OpenCV para realizar el procesamiento final de las imagenes generadas a un video.

    python3 imgs2video.py

Y como resultado final obtenemos el siguiente video.

Video: Click on the image
[![Video](https://i.ibb.co/PCWKPdj/VidSynth.png)](https://youtu.be/UIQUbunxXQQ)

En este caso variando los parametros de conversion, el modelo e incluso la seed modificaremos el resultado del video generado, mejorandolo o empeorandolo, asi que modifica los parametros con el fin de obtener mejores resultados.

### Epic DEMO:

Video: Click on the image
[![Video](https://i.ibb.co/PCWKPdj/VidSynth.png)](pending...)

Sorry github does not allow embed videos.

# Commentary:

Este proyecto muestra la idea base de usar los modelos de stable diffusion para la creacion de videos, con modelos mejores como SD 2.0 o una tarjeta de desarrollo mejor, este proyecto puede funcionar mucho mejor debido al intenso procesamiento de GPU que requiere.

## References:

Links:

(1) https://www.jetson-ai-lab.com/tutorial_stable-diffusion.html

(2) https://github.com/dusty-nv/jetson-containers

(3) https://huggingface.co/CompVis/stable-diffusion-v1-4
