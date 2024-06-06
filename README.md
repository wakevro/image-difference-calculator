# Image Difference Calculator

A Python project to calculate differences in pixel values between images.

## Description

This project calculates the difference in sum of squares of pixel values between a main image and multiple perturbation images. The calculations can be done synchronously, asynchronously, or in parallel using different Python modules.

## Features

- Synchronous, asynchronous, and parallel processing of images.
- Calculates differences between a main image and perturbation images.
- Results are saved to a CSV file.

## Requirements

- Python 3.7+
- numpy
- opencv-python

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/wakevro/image-difference-calculator.git
    cd image-difference-calculator
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Place your images in the `../fgsm` folder.
2. Run the main script:
    ```sh
    python main.py
    ```
3. Results will be saved in the `results` folder.

## Scripts

### main.py

This script runs the synchronous, asynchronous, and parallel versions of the image difference calculations.

### sync.py

Contains the synchronous processing logic.

### async.py

Contains the asynchronous processing logic.

### parallel.py

Contains the parallel processing logic using `ProcessPoolExecutor`.

## Contributing

Feel free to open issues or submit pull requests with improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
