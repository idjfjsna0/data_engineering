# Data_engineering
basic course
data set link: https://drive.google.com/file/d/1sStrkLT-LQ3sIPJD-rPY0LNCCk5l1lbg/view?usp=sharing
the dataset contains data on the spectrum of the transmission coefficient of an interference filter depending on the rotation angle

# Creating env (conda + poetry)
after installing conda, in command window:
1. conda create -n my_env python=3.13
2. conda activate my_env
3. pip install poetry
4. poetry new trying_de
5. cd trying_de
6. poetry add jupyter pandas matplotlib numpy wget
7. poetry install --no-root

# Result by starting data_loader.py script
<img width="1979" height="481" alt="изображение" src="https://github.com/user-attachments/assets/ce52d5e1-2e25-4acd-b289-6f9b1425a6cc" />
# Convert data to float64, save DataFrame to .csv
<img width="763" height="737" alt="изображение" src="https://github.com/user-attachments/assets/c37d6d33-7eb4-4ea1-a2b5-b756fa716549" />
