import numpy as np
from load_data import AnalisisPlano

guatape = AnalisisPlano("Datasets\\Guatape.csv", 'Guatape')
df_guatape = guatape.basic_reports()

elBagre = AnalisisPlano("Datasets\\Elbagre.csv", 'ElBagre')
df_elBagre = elBagre.basic_reports()

arvi = AnalisisPlano("Datasets\\Arvi.csv", 'Arvi')
df_arvi = arvi.basic_reports()

zungo = AnalisisPlano("Datasets\\Zungo.csv", 'Zungo')
df_zungo = zungo.basic_reports()

