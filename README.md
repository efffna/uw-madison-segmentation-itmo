# Training & Inference

Здесь представлены ноутбуки для обучения и инференса моделей в соревновании [UW-Madison GI Tract Image Segmentation](https://www.kaggle.com/competitions/uw-madison-gi-tract-image-segmentation/).

## Description

Цель соревнования: сегментировать на изображении (слайс DICOM) целевые метки - желудок, тонкая и толстая кишка.

Весь пайплайн разделен на 2 части, так как в качестве submission файла на платформу загружается ноутбук с созданием submission.csv, по которому происходит расчет итогового скора. При этом при инференсе необязательно иметь цикл обучения модели, но при этом нужно иметь возможность импортировать библиотеки и загружать веса модели без интернета. 

Для инференса и отправки решения необходимо загрузить ноутбук на платформу Kaggle и добавить в него следующие данные:
* uw-madison-gi-tract-image-segmentation
* pytorch-segmentation-models-lib
* uwmgi-mask-dataset
* uwgaifullin

Добавление происходит путем нажатия на кнопку `Add data` в правом верхнем углу.
