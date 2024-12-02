import argparse
import cv2
# https://docs.ultralytics.com/reference/engine/results/#ultralytics.engine.results.Results

from ultralytics import YOLO
import logging  # Import the logging module
from pythonosc import udp_client

#def process_file(file, number, verbose):
def process_file():
    #print(f"Processing file: {file}")

    # Print the number with its default value if not provided
    #print(f"Number used for processing: {number}")

    # Handle verbose flag with default set to False
    #if verbose:
    #    print("Verbose mode is enabled.")

    # https://docs.ultralytics.com/modes/track/#tracker-selection

    # Create an OSC client
    ip_address = "127.0.0.1"  # The IP address of the OSC server
    port = 8000  # The port the OSC server is listening on
    client = udp_client.SimpleUDPClient(ip_address, port)

    # Suppress YOLOv8 info-level logs by setting the logging level to WARNING
    logging.getLogger("ultralytics").setLevel(logging.WARNING)

    # Load the YOLOv8 model
    # This will download the model from the internet
    model = YOLO("yolo11n.pt")

    # Open the video file
    #video_path = "path/to/video.mp4"
    #cap = cv2.VideoCapture(video_path)
    cap = cv2.VideoCapture(0)

    previous_object_ids = set()

    # Loop through the video frames
    while cap.isOpened():
        # Read a frame from the video
        success, frame = cap.read()

        if success:

            # Get the frame dimensions
            frame_height, frame_width = frame.shape[:2]

            # Run YOLOv8 tracking on the frame, persisting tracks between frames
            # documentation: https://docs.ultralytics.com/modes/predict/#inference-arguments
            results = model.track(frame, persist=True)

            if results[0].boxes.id is None:
                print("we have results")
                # results might give results for multiple frames, we only have one so it is in index 0
                # Get the bounding box coordinates (x1, y1, x2, y2)
                boxes_xyxy = results[0].boxes.xyxy.cpu().numpy().tolist()
                boxes_ids =  results[0].boxes.id.cpu().numpy().tolist() #results[0].boxes.id.cpu().numpy().tolist() if results[0].boxes.id is not None else [] 

                # Loop through each box to compute and send the normalized center
                for box, id in zip(boxes_xyxy, boxes_ids):
                    x1, y1, x2, y2 = box  # Unpack box coordinates
                    center_x = (x1 + x2) / 2
                    center_y = (y1 + y2) / 2

                    # Normalize the center coordinates
                    norm_center_x = center_x / frame_width
                    norm_center_y = center_y / frame_height

                #client.send_message("/object/movement", [norm_center_x, norm_center_y])

                # Get the current object IDs from the results
                current_object_ids = set(results[0].boxes.id.cpu().numpy().tolist())

                # Find new objects that appeared
                new_objects = current_object_ids - previous_object_ids
                #if new_objects:
                #    print(f"New objects appeared: {new_objects}")

                # Find objects that disappeared
                disappeared_objects = previous_object_ids - current_object_ids
                #if disappeared_objects:
                #    print(f"Objects disappeared: {disappeared_objects}")

                for id in new_objects:
                    client.send_message("/object/created", int(id))

                for id in disappeared_objects:
                    client.send_message("/object/deleted", int(id))

                # Update the previous_object_ids with the current IDs for the next iteration
                
            else:
                print("no objects on this frame")
                current_object_ids = set()

            previous_object_ids = current_object_ids
            print(f"current_object_ids: {current_object_ids}")

            # Visualize the results on the frame
            annotated_frame = results[0].plot()

            # Display the annotated frame
            cv2.imshow("YOLOv8 Tracking", annotated_frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            # Break the loop if the end of the video is reached
            break

    # Release the video capture object and close the display window
    cap.release()
    cv2.destroyAllWindows()

def main():
    #parser = argparse.ArgumentParser(description="MyTool File Processor Utility")

    # Required argument: main file
    #parser.add_argument("file", type=str, help="Path to the main file to be processed")

    # Optional argument: number with a default value
    #parser.add_argument("--number", type=int, default=1, help="An integer number to use during processing (default: 1)")

    # Boolean flag: verbose with default set to False
    #parser.add_argument("--verbose", action="store_true", help="Enable verbose output (default: False)")

    # Parse the arguments
    #args = parser.parse_args()

    # Execute the main function
    process_file()

if __name__ == "__main__":
    main()
