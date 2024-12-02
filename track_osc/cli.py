import argparse
import cv2
# https://docs.ultralytics.com/reference/engine/results/#ultralytics.engine.results.Results

from ultralytics import YOLO
import logging  # Import the logging module
from pythonosc import udp_client
import time

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

    #client.send_message("/object/created", [0, 0.1, 1.0])
    #time.sleep(1)
    #client.send_message("/object/movement", [0, 0.7,0.6])
    #time.sleep(1)
    #client.send_message("/object/deleted", [0])
    processVideo(client)

def processVideo(client):
    # Suppress YOLOv8 info-level logs by setting the logging level to WARNING
    logging.getLogger("ultralytics").setLevel(logging.WARNING)

    # Load the YOLOv11 model
    # This will download the model from the internet
    model = YOLO("yolo11n.pt")

    # Start the camera capture
    cap = cv2.VideoCapture(0)

    previous_object_ids = set()

    # Loop through the video frames
    while cap.isOpened():
        # Read a frame from the video
        success, frame = cap.read()

        if success:
            # Get the frame dimensions
            frame_height, frame_width = frame.shape[:2]

            # Run YOLOv11 tracking on the frame, persisting tracks between frames
            # documentation: https://docs.ultralytics.com/modes/predict/#inference-arguments
            # conf - Sets the minimum confidence threshold for detections.
            # https://docs.ultralytics.com/reference/engine/model/#ultralytics.engine.model.Model.track
            results = model.track(frame, persist=True, conf=0.5, tracker="bytetrack.yaml")

            #Results is a list which would correspond to multiple frames, if multiple frames were passed to track
            #In this case it will have only one element
            if results[0].boxes.id is not None:
                # results might give results for multiple frames, we only have one so it is in index 0
                # Get the bounding box coordinates (x1, y1, x2, y2)
                boxes_xyxy = results[0].boxes.xyxy.cpu().numpy().tolist()
                boxes_ids =  results[0].boxes.id.cpu().numpy().tolist() #results[0].boxes.id.cpu().numpy().tolist() if results[0].boxes.id is not None else [] 

                # Get the current object IDs from the results
                current_object_ids = set(boxes_ids)
                 # Find new objects that appeared
                new_objects = current_object_ids - previous_object_ids
                # Find objects that disappeared
                disappeared_objects = previous_object_ids - current_object_ids

                if len(boxes_ids) != len(boxes_xyxy):
                    print("len(boxes_ids) != len(boxes_xyxy): {len(boxes_ids)} {len(boxes_xyxy)}")

                def getCenter(box):
                    x1, y1, x2, y2 = box
                    center_x = (x1 + x2) / 2
                    center_y = (y1 + y2) / 2
                    return (center_x / frame_width, center_y / frame_height)
                
                centerPositions = map(getCenter, boxes_xyxy)
                
                 #if new_objects:
                #    print(f"New objects appeared: {new_objects}")
                #if disappeared_objects:
                #    print(f"Objects disappeared: {disappeared_objects}")

                #new_objects is subset of current_object_ids so can test here
                for center, id in zip(centerPositions, boxes_ids):
                    x,y = center
                    if id in new_objects:
                        client.send_message("/object/created", [int(id), float(x), float(y)])
                        print(f"/object/created {[int(id), float(x), float(y)]}")
                    else:
                        client.send_message("/object/movement", [int(id), float(x), float(y)])
                        #print(f"Object moving: { [id, x, y]}")

                for id in disappeared_objects:
                    client.send_message("/object/deleted", int(id))
                    print(f"/object/deleted { [id]}")
            else:
                #No objects were detected in this frame therefore we will send message asking them to be deleted.
                #print("no objects on this frame")
                current_object_ids = set()
                #if previous_object_ids:
                #    print(f"Objects disappeared: {disappeared_objects}")
                for id in previous_object_ids:
                    client.send_message("/object/deleted", int(id))
                    print(f"/object/deleted (no objects this frame) { [id]}")
            
            if previous_object_ids != current_object_ids:
                print(f"Objects have changed: {current_object_ids}")

            #Set the current objects to the previous objects variable for comparison in the next iteration
            previous_object_ids = current_object_ids

            # Visualize the results on the frame
            annotated_frame = results[0].plot()

            # Display the annotated frame
            cv2.imshow("YOLOv11 Tracking", annotated_frame)

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
