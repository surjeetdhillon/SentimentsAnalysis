# ha-20-Y_S

1. Pre-Requisites
    Python3.8
    macOS or Linux (Windows not officially supported, but might work)
    make sure you have dlib already installed with Python bindings
    
2. Installation
    Run following commands
        Navigate to the root folder of your project and create virtual environment
            python3 -m venv env
            source env/bin/activate

        pip install -r requirements.txt

3. Running App help
    To get help use python main.py --help
    
4. Running App

    Uses 1 : Webcam live preview
    python main.py --webcamview    ##This command will open the window and start the webcamera to identify the emotions. This will not generate any report as of now.
    Please note that if webcamview is chosen then the text reports and analysis will not be generated 
    
    Use Case 2: 
    python main.py --filename GMT20200627-193326_Surjeet-Dh_640x360.mp4 --liveporcessing ##This command will open saved video in media/recording folder and starts processing. --liveprocessing opens a window to show live processing of video otherwise the video is processed in background

    Use Case 3: Generating the text meeting Notes
    Meeting notes are always generated with every command example python main.py

    Use Case 4: Generating Text Sentimental Analysis
    python main.py --textsentiments ## This command will do analysis over the meeting notes and generate the sentiments.
    
5. Getting Reports
    Currently the reports are generated in the folder 'report'. Please navigate there to see the final reports. 
