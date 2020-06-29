import typer
from data_processing_app.processing import transcript_processing


def main(
    live_webcam_preview: bool = typer.Option(False, '--webcamview', help='Live webcam processing view'),
    live_processing_preview: bool = typer.Option(False, '--liveprocessing', help='Run video processing in preview mode'),
    video_file: str = typer.Option(None, '--filename', help='File name'),
    sentiments_from_text: bool = typer.Option(False, '--textsentiments', help='Enable sentiments based on text transcript')
    ):

    # if live_webcam_preview == False and video_file == None:
    #     typer.echo('If Web Camera preview is not selected --filename must be provided')
    #     raise typer.Exit()

    # typer.echo('Start Processing...')

    # from data_processing_app.processing import video_processing
    # video_processing.run(live_webcam_preview, live_processing_preview, video_file)
    
    if live_webcam_preview == False:
        transcript_processing.main(sentiments_from_text)

if __name__ == '__main__':
    typer.run(main)