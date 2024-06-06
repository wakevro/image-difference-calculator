import numpy as np
import cv2
import os
import time
import csv
from concurrent.futures import ProcessPoolExecutor


def calculate_differences(main_image_path, perturbation_paths):
    """
    Calculate the difference in sum of squares of pixel values between the main image
    and each of the perturbation images.

    Parameters:
    main_image_path (str): The file path of the main image.
    perturbation_paths (list of str): List of file paths of the perturbation images.

    Returns:
    list of tuple: A list of tuples where each tuple contains the perturbation image filename
                   and the calculated difference.
    """
    main_image = cv2.imread(main_image_path)
    if main_image is None:
        raise FileNotFoundError(f"Main image not found at path: {main_image_path}")

    mean_main = np.mean(main_image)
    main_ssq = np.sum((main_image - mean_main) ** 2)

    results = []
    for perturbation_path in perturbation_paths:
        perturbation = cv2.imread(perturbation_path)
        if perturbation is not None:
            mean_perturbation = np.mean(perturbation)
            perturbation_ssq = np.sum((perturbation - mean_perturbation) ** 2)
            difference = round(main_ssq - perturbation_ssq, 14)
            results.append((os.path.basename(perturbation_path), difference))

    return results


def process_image(main_image_path, perturbation_paths):
    """
    Process a main image and its perturbations, calculating differences in a separate process.

    Parameters:
    main_image_path (str): The file path of the main image.
    perturbation_paths (list of str): List of file paths of the perturbation images.

    Returns:
    tuple: A tuple containing the main image ID, the calculated differences, and the elapsed time.
    """
    start_time = time.time()
    results = calculate_differences(main_image_path, perturbation_paths)
    end_time = time.time()
    elapsed_time = end_time - start_time
    main_image_id = os.path.basename(main_image_path).split("-")[-1]

    return main_image_id, results, elapsed_time


def create_results_directory(directory="results"):
    """
    Create a directory to store results if it does not already exist.

    Parameters:
    directory (str): The directory path to create. Defaults to 'results'.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_main_image_paths(folder, pattern="fgsm-eps0.00-id"):
    """
    Get a list of main image paths from a specified folder that match a given pattern.

    Parameters:
    folder (str): The folder containing the main images.
    pattern (str): The pattern to match filenames. Defaults to 'fgsm-eps0.00-id'.

    Returns:
    list of str: List of file paths that match the pattern.
    """
    return [
        os.path.join(folder, filename)
        for filename in os.listdir(folder)
        if pattern in filename
    ]


def main():
    # Create the results directory
    create_results_directory()

    # Define the folder containing the main images
    main_image_folder = "../fgsm"
    main_image_paths = get_main_image_paths(main_image_folder)

    # Define the CSV filename to store the results
    csv_filename = "results/parallel-results.csv"

    with open(csv_filename, mode="w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Processing Type", "Parallel"])
        csv_writer.writerow(["ID", "Difference", "Time Taken (s)"])

        total_start_time = time.time()

        all_results = []

        with ProcessPoolExecutor() as executor:
            futures = []
            for main_image_path in main_image_paths:
                perturbation_paths = [
                    os.path.join(
                        main_image_folder,
                        f"fgsm-eps0.{eps}-"
                        + os.path.basename(main_image_path).split("-")[-1],
                    )
                    for eps in ["00", "01", "02", "05", "10", "20"]
                ]
                futures.append(
                    executor.submit(process_image, main_image_path, perturbation_paths)
                )

            for future in futures:
                main_image_id, result, elapsed_time = future.result()
                sorted_results = sorted(result)  # Sort results by ID
                csv_writer.writerows(
                    [(main_image_id, diff, elapsed_time) for _, diff in sorted_results]
                )
                all_results.extend(
                    [
                        (main_image_id, _, diff, elapsed_time)
                        for _, diff in sorted_results
                    ]
                )

                print(f"Main Image: {main_image_id}")
                print(f"Elapsed time for calculations: {elapsed_time:.2f} seconds")
                print("Results:")
                for res in sorted_results:
                    print(res)

        total_end_time = time.time()
        total_elapsed_time = total_end_time - total_start_time
        print(
            f"Total elapsed time for all calculations: {total_elapsed_time:.2f} seconds"
        )

        # Add a row for the total time at the end
        csv_writer.writerow(["Total Time", "", total_elapsed_time])

    print(f"Results saved to {csv_filename}")


if __name__ == "__main__":
    main()
