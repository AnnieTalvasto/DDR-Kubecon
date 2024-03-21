import cv2
import pytesseract
import time

# Function to preprocess the frame
def preprocess(frame):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Apply adaptive thresholding to create a binary image
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 4)
    
    return thresh

# Function to perform OCR on the preprocessed frame
def perform_ocr(frame):
    # Perform OCR using pytesseract
    text = pytesseract.image_to_string(frame)
    return text

# Function to determine the winning player
def determine_winner(numbers):
    if not numbers:
        return None
    max_number = max(numbers)
    winning_player = numbers.index(max_number) + 1  # Assuming player numbers start from 1
    return winning_player

# Main function
def main():
    # Open the video capture device
    cap = cv2.VideoCapture(0)  # Use 0 for the default webcam

    # Initialize variables to store the detected numbers and the time of the last winner announcement
    detected_numbers = []
    last_announcement_time = time.time()

    while True:
        # Read a frame from the video feed
        ret, frame = cap.read()
        
        if not ret:
            break

        # Preprocess the frame
        preprocessed_frame = preprocess(frame)

        # Perform OCR on the preprocessed frame
        text = perform_ocr(preprocessed_frame)

        # Split the detected text into individual numbers
        numbers = [int(num) for num in text.split() if num.isdigit()]

        # Update the detected numbers
        detected_numbers = numbers

        # Check if it's time to announce the winner
        current_time = time.time()
        if current_time - last_announcement_time >= 10:
            winner = determine_winner(detected_numbers)
            if winner is not None:
                print(f"Player {winner} is currently winning")
            else:
                print("No numbers detected")
            last_announcement_time = current_time

        # Display the preprocessed frame
        cv2.imshow('Preprocessed Frame', preprocessed_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture device and close all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
