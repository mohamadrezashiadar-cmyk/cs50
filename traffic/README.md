# Traffic

A convolutional neural network (CNN) that classifies road signs from the
[German Traffic Sign Recognition Benchmark (GTSRB)](https://benchmark.ini.rub.de/) dataset.
The model is built with TensorFlow/Keras, and images are loaded and resized with OpenCV.

## Dataset

The dataset is **not included in this repository** because of its size. To run the project:

1. Download the GTSRB dataset from the
   [CS50 AI Project 5 page](https://cs50.harvard.edu/ai/2020/projects/5/traffic)
   (link: "Download the data set").
2. Unzip it and place the resulting `gtsrb` folder next to `traffic.py`.

The folder must contain 43 subdirectories named `0` to `42`, one per sign category,
each holding the images for that category. `gtsrb/` is listed in `.gitignore`.

## Usage

```
pip install -r requirements.txt
python traffic.py gtsrb              # train and evaluate
python traffic.py gtsrb model.h5     # train, evaluate and save the model
```

## Implementation

### `load_data(data_dir)`

- Iterates over the category folders `0` to `NUM_CATEGORIES - 1`.
- Reads every image with `cv2.imread`, skips files OpenCV cannot read, and resizes
  each image to `IMG_WIDTH x IMG_HEIGHT` (30 x 30) so the network receives a fixed input shape.
- Builds paths with `os.path.join`, so the code works on Windows, macOS and Linux.
- Returns `(images, labels)`: a list of `(30, 30, 3)` NumPy arrays and a list of integer labels.

### `get_model()`

| Layer | Details |
| --- | --- |
| Input | `(IMG_WIDTH, IMG_HEIGHT, 3)` |
| Rescaling | pixel values scaled from `0-255` to `0-1` |
| Conv2D | 32 filters, 3x3, ReLU |
| MaxPooling2D | 2x2 |
| Conv2D | 64 filters, 3x3, ReLU |
| MaxPooling2D | 2x2 |
| Flatten | |
| Dense | 128 units, ReLU |
| Dropout | rate 0.5 |
| Dense (output) | `NUM_CATEGORIES` (43) units, softmax |

The model is compiled with the Adam optimizer, categorical cross-entropy loss
(labels are one-hot encoded in `main`), and accuracy as the metric.

## Design decisions

- **Convolution + pooling.** Road signs are defined by local visual patterns such as edges,
  shapes and symbols. Convolutional layers detect these patterns wherever they appear in the
  image, with far fewer parameters than a fully connected network on raw pixels.
  Max pooling shrinks the feature maps, which reduces computation and makes the model
  less sensitive to small shifts of the sign.
- **Two convolutional blocks, with more filters in the second.** The first layer learns simple
  features (edges, colors), and the second combines them into more complex ones
  (shapes, parts of symbols), so it benefits from more filters.
- **Input rescaling.** Neural networks train more stably when inputs are small values.
  Dividing by 255 keeps the loss well behaved and helps the model converge faster.
- **Dropout (0.5) after the hidden dense layer.** The dense layer holds most of the
  parameters and is the most prone to overfitting. Randomly disabling half of its units during
  training forces the network not to rely on any single unit.
- **Softmax output with categorical cross-entropy.** This is the standard setup for
  single-label multi-class classification: the output is a probability distribution over
  the 43 categories.

## Experimentation

> The first row is from a real run of the final model (10 epochs, 40% of the data held out for testing).
> The remaining rows are still to be filled in with your own results.

| Configuration | Train accuracy | Test accuracy | Notes |
| --- | --- | --- | --- |
| Final model (described above) | 93.81% (epoch 10) | 98.68% | Test loss 0.0545, 10 epochs |
| Without Dropout | _TBD_ | _TBD_ | |
| One convolutional block instead of two | _TBD_ | _TBD_ | |
| 3x3 vs 5x5 filters | _TBD_ | _TBD_ | |
| Hidden layer of 64 vs 128 vs 256 units | _TBD_ | _TBD_ | |
| Image size 30x30 vs 40x40 | _TBD_ | _TBD_ | |

Questions to answer after running the experiments:

- What did you try, and what worked well?
- What did not work well?
- How large is the gap between training and test accuracy, and what does that say about overfitting?
- What effect did removing or changing Dropout have?

## Project structure

```
traffic/
├── traffic.py
├── requirements.txt
├── README.md
├── .gitignore
└── gtsrb/        # not tracked by git: download it separately
```

## Acknowledgements

Data provided by J. Stallkamp, M. Schlipsing, J. Salmen and C. Igel.
*The German Traffic Sign Recognition Benchmark: A multi-class classification competition.*
In Proceedings of the IEEE International Joint Conference on Neural Networks, pages 1453-1460, 2011.
